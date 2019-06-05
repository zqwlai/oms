# -*- coding: UTF-8 -*-
from django import template
register = template.Library()


@register.filter
def is_active(template_name,curM):
    if template_name == curM:
        return 'active'
    else:
        return ''
