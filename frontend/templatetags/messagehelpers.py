from django import template


register = template.Library()

@register.simple_tag()
def message_to_bootstrap_level(msglevel):
    if msglevel == "error":
        return "danger"

    return "secondary"