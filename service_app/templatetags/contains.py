# -*- coding: UTF-8 -*-
from django import template
register = template.Library()


@register.filter
def contains(text, data):
    if data.find(text) == 0:
        return 'active'
    else:
        return ''
