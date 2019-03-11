from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def index(l, i):
    return l[int(i)]

@register.filter
def range(num):
    return range(num)