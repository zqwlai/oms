# -*- coding: UTF-8 -*-
from django import template
register = template.Library()


@register.filter
def in_list(data_string,data_list):
    return data_string in data_list
