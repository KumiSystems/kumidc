from radius.server import RadiusServer

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Run the RADIUS server"

    def handle(self, *args, **kwargs):
        # Set up and run the RADIUS server
        srv = RadiusServer()
        srv.Run()