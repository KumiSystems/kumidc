from django.contrib.auth import authenticate, get_user_model

from pyrad import dictionary, packet, server

from radius.models import (
    RadiusAccountingSession,
    RadiusUser,
    RadiusAccountingEvent,
    RadiusWebAuthentication,
)
from authentication.helpers.otp import has_otp
from authentication.models import TOTPSecret

import uuid


class RadiusServer(server.Server):
    def HandleAuthPacket(self, pkt):
        """Handle an authentication packet

        Args:
            pkt (packet.Packet): The packet to handle
        """
        if state:
            # Handle the challenge response
            if self.validate_challenge_response(packet):
                # Consider the challenge successfully passed
                reply = self.CreateReplyPacket(pkt)
                reply.code = packet.AccessAccept
            else:
                # Challenge failed
                reply = self.CreateReplyPacket(pkt)
                reply.code = packet.AccessReject
            self.SendReplyPacket(pkt.fd, reply)
            return

        # No state implies this may be the first packet for authentication
        # So we need to generate a challenge if necessary

        # First check if the user exists
        user = authenticate(username=username, password=password)

        if user is None:
            # User does not exist or password is incorrect
            reply = self.CreateReplyPacket(pkt)
            reply.code = packet.AccessReject
            self.SendReplyPacket(pkt.fd, reply)
            return

        if user.radiususer.challenge == "none":
            # No challenge is required
            reply = self.CreateReplyPacket(pkt)
            reply.code = packet.AccessAccept
            self.SendReplyPacket(pkt.fd, reply)
            return

        # Generate a challenge

        state = str(uuid.uuid4())

        if user.radiususer.challenge == "totp":
            if not has_otp(user):
                # This user is not configured for TOTP...? # TODO: Make sure this is handled in the admin
                reply = self.CreateReplyPacket(pkt)
                reply.code = packet.AccessReject
                self.SendReplyPacket(pkt.fd, reply)
                return

            challenge_reply = self.CreateReplyPacket(
                pkt,
                **{"State": state, "Reply-Message": "Please enter your TOTP token."}
            )

            challenge_reply.code = packet.AccessChallenge
            self.SendReplyPacket(pkt.fd, challenge_reply)
            return

        if user.radiususer.challenge == "web":
            challenge_reply = self.CreateReplyPacket(
                pkt,
                **{
                    "State": state,
                    "Reply-Message": "Please visit http://kumidc.local/auth to authenticate.",  # TODO: Replace with a URL to our authentication page
                }
            )
            challenge_reply.code = packet.AccessChallenge
            self.SendReplyPacket(pkt.fd, challenge_reply)
            return

        # We should never get here. If we do, something has gone wrong.
        reply = self.CreateReplyPacket(pkt)
        reply.code = packet.AccessReject
        self.SendReplyPacket(pkt.fd, reply)

    def validate_challenge_response(self, packet, password):
        state = packet["State"][0]
        username = packet["User-Name"][0]
        challenge_response = packet.get("User-Password", [None])[0]

        user = get_user_model().objects.get(username=username)

        if not user:
            # This user... doesn't exist?
            return False

        if not user.radiususer.challenge:
            # This user is not configured for challenge-response. Where did this response come from?
            return False

        if user.radiususer.challenge == "totp":
            if not has_otp(user):
                # This user is not configured for TOTP...
                return False

            totp = TOTPSecret.objects.get(user=user)

            return totp.verify(
                challenge_response
            )  # Returns True if the token is valid, False otherwise

        if user.radiususer.challenge == "web":
            ip = packet["NAS-IP-Address"][0]
            auth = RadiusWebAuthentication.objects.filter(
                user=user, ip=ip, expiry__gte=datetime.now()
            )
            auth.delete()  # Delete any existing authentication sessions for this user
            return True

    def HandleAcctPacket(self, pkt: packet.Packet):
        """Handle an accounting packet

        Args:
            pkt (packet.Packet): The packet to handle
        """
        status_type = pkt["Acct-Status-Type"][0]
        username = pkt["User-Name"][0]
        session_id = pkt["Acct-Session-Id"][0]

        user = RadiusUser.objects.get(user__username=username)

        session, created = RadiusAccountingSession.objects.get_or_create(
            id=session_id,
            defaults={
                user: user,
            },
        )

        if status_type == "Start":
            session.start()
        elif status_type == "Stop":
            session.stop()

        RadiusAccountingEvent.objects.create(
            session=session, event_type=status_type, raw_data=pkt.packet
        )

        acct.save()
