# KumiDC

KumiDC is a simple Django-based OpenID Connect identity provider.

At its core, it uses [Django OpenID Connect Provider](https://github.com/juanifioren/django-oidc-provider) by [Juan Ignacio Fiorentino](https://github.com/juanifioren) to provide the actual OIDC functionality, and adds a few fancy things on top.

* "Pretty" [AdminLTE](https://github.com/ColorlibHQ/AdminLTE) user interface
* Time-based One-Time Passwords for Two Factor Authentication
* Requirement to re-authenticate or enter 2FA token every five minutes

As it stands, this project is not complete. It works as an OIDC provider, although its security has not been tested to any extent.

We currently use it, in conjunction with [oauth2-proxy](https://github.com/oauth2-proxy/oauth2-proxy), to add an authentication layer to applications on our internal network where protection against unauthorized access is not directly implemented, and not critical.