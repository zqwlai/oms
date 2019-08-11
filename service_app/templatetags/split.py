# -*- coding: UTF-8 -*-
from django import template
register = template.Library()


@register.filter
def split(text,  separation):
    return text.split(separation)
