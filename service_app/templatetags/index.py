# -*- coding: UTF-8 -*-
from django import template
register = template.Library()


@register.filter
def index(text, offset):
    return text[int(offset)]
