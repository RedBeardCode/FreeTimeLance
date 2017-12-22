# -*- coding: utf-8 -*-
"""
User defined templates tags and filters
"""
from django import template

register = template.Library()


@register.filter()
def hour(value):
    """
    Filter to format timedelta to 0.00h string
    """
    return "{0:.1f}".format(value.total_seconds() / 3600.0)
