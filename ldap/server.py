from zope.interface import implementer
from twisted.internet import reactor, defer
from twisted.internet.protocol import Factory
from ldaptor.protocols.ldap import ldapserver, ldapsyntax, distinguishedname, ldaperrors
from ldaptor import interfaces, entry
from django.contrib.auth import get_user_model, authenticate
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()

@implementer(interfaces.IConnectedLDAPEntry)
class DjangoUserEntry:
    def __init__(self, user):
        self.dn = distinguishedname.DistinguishedName('cn={},dc=kumidc'.format(user.username))
        self.attributes = {'cn': [user.username,], 'email': [user.email,]}

    def search(self, filterObject, attributes=None):
        # This ignores the filter and always returns the authenticated user
        # This LDAP server is only meant to be used for authentication, not as a directory service
        return defer.succeed([self])

    def lookup(self):
        return defer.succeed(self)

    def bind(self, password):
        username = self.dn.split(',')[0].split('=')[1]
        user = authenticate(username=username, password=password)

        if user is not None:
            self.__init__(user)
            return defer.succeed(self)
        else:
            return defer.fail()

class LDAPServer(ldapserver.LDAPServer):
    def handle_LDAP_BIND_REQUEST(self, request, controls, reply):
        if request.dn:
            user_dn = str(request.dn)
            try:
                username = user_dn.split(',')[0].split('=')[1]
                user = User.objects.get(username=username)
                e = DjangoUserEntry(user)
            except ObjectDoesNotExist:
                return defer.fail(ldaperrors.LDAPInvalidCredentials())

            d = e.bind(request.auth)
            d.addCallbacks(reply, reply.handle_LDAPError)
            return d

        elif request.sasl:
            if request.sasl.mechanism == "PLAIN":
                authzid, authcid, password = request.sasl.credentials.split('\x00')
                e = DjangoUserEntry(user)
                d = defer.succeed(e)
                d.addCallbacks(reply, reply.handle_LDAPError)
                return d
            else:
                return defer.fail(ldaperrors.LDAPInvalidCredentials())
        else:
            return defer.fail(ldaperrors.LDAPInvalidCredentials())

    def handle_LDAP_SEARCH_REQUEST(self, request, reply):
        if not self.boundUser:
            return defer.fail(ldaperrors.LDAPUnwillingToPerform())

        search_filter = request.filter
        f = request.filter.asText()

        try:
            user = User.objects.get(username=self.boundUser)
            e = DjangoUserEntry(user)
        except ObjectDoesNotExist:
            return defer.fail(ldaperrors.LDAPNoSuchObject())

        if search_filter.present("objectClass") and request.scope == ldapclient.SCOPE_BASE:
            entries = [e]
        else:
            entries = []

        reply(entries)
        return defer.succeed(())



    def handleUnknown(self, op):
        # Ignore requests we don't support
        return defer.succeed(None)