# -*- coding: UTF-8 -*-
from django import template
register = template.Library()


@register.filter
def unicode2utf8(data):
    return data.decode('unicode_escape')
