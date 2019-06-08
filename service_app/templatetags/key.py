# -*- coding: UTF-8 -*-
from django import template
register = template.Library()


@register.filter
def key(dict_ret,k):
    return dict_ret.get(k, '')
