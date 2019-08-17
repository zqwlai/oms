# -*- coding: UTF-8 -*-
from django import template
register = template.Library()


@register.filter
def index_reverse(offset, text):
    return text[int(offset)-1]
