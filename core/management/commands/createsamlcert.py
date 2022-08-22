from django.core.management.base import BaseCommand
from django.conf import settings

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography import x509
from cryptography.x509.oid import NameOID

from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Generates self-signed certificate for SAML IdP'
  
    def add_arguments(self, parser):
        parser.add_argument('-f', '--force', action='store_true', help="Force re-creation of certificates if the files already exist")
        parser.add_argument('--commonname', type=str, help="Common Name to use for certificate, default: KumiDC", default="KumiDC")
        parser.add_argument('--country', type=str, help="Country Code to use for the certificate, default: US", default="US")
        parser.add_argument('--state', type=str, help="State name to use for the certificate, default: New York", default="New York")
        parser.add_argument('--locality', type=str, help="Locality name to use for the certificate, default: New York City", default="New York City")
        parser.add_argument('--organization', type=str, help="Organization name to use for the certificate, default: KumiDC", default="KumiDC")
        parser.add_argument('--validity-days', type=int, help="How many days the certificate should be \"valid\" for, default: 3650", default=3650)

    def handle(self, *args, **kwargs):
        if (settings.CERTIFICATE_DIR / "saml.key").exists() or (settings.CERTIFICATE_DIR / "saml.crt").exists():
            if not kwargs["force"]:
                print(f"Error: saml.crt and/or saml.key already in CERTIFICATE_DIR ({settings.CERTIFICATE_DIR}). Add --force to create new key pair.")

        key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

        subject = issuer = x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, kwargs["commonname"]),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, kwargs["state"]),
            x509.NameAttribute(NameOID.COUNTRY_NAME, kwargs["country"]),
            x509.NameAttribute(NameOID.LOCALITY_NAME, kwargs["locality"]),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, kwargs["organization"]),
        ])

        cert = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer).public_key(key.public_key()).serial_number(x509.random_serial_number()).not_valid_before(datetime.utcnow()).not_valid_after(datetime.utcnow() + timedelta(days=3650)).add_extension(x509.SubjectAlternativeName([x509.DNSName(name) for name in settings.ALLOWED_HOSTS]), critical=False).sign(key, hashes.SHA256())

        settings.CERTIFICATE_DIR.mkdir(exist_ok=True)

        with open(settings.CERTIFICATE_DIR / "saml.key", "wb") as keyfile:
            keyfile.write(key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.TraditionalOpenSSL, serialization.NoEncryption()))

        with open(settings.CERTIFICATE_DIR / "saml.crt", "wb") as certfile:
            certfile.write(cert.public_bytes(serialization.Encoding.PEM))