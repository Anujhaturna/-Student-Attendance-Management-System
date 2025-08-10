from django import template
from django.urls import NoReverseMatch, reverse

register = template.Library()


@register.filter
def url_exists(url_name):
    try:
        reverse(url_name)
        return True
    except NoReverseMatch:
        return False
