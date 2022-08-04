import pyqrcode

from django import template


register = template.Library()

@register.simple_tag()
def url_to_qrcode(url):
    return "data:image/png;base64," + pyqrcode.QRCode(url).png_as_base64_str()