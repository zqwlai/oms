# -*- coding: UTF-8 -*-


from django import template
register = template.Library()


@register.filter
def utc2local(text):

    temp = text.split('T')
    date_string = temp[0]
    time_string = temp[1].split('+')[0]

    return '%s %s'%(date_string, time_string)
