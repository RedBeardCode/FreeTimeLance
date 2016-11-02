from django import template

register = template.Library()

@register.filter()
def hour(value):
    return "{0:.1f}".format(value.total_seconds()/3600.0)