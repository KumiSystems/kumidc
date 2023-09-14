from django.core.management.base import BaseCommand
from django.conf import settings

from ldap.server import LDAPServer

from twisted.internet.protocol import Factory
from twisted.internet import reactor

class Command(BaseCommand):
    help = 'Provides a simple LDAP server'

    def handle(self, *args, **kwargs):
        factory = Factory()
        factory.protocol = LDAPServer
        reactor.listenTCP(10389, factory)
        reactor.run()
