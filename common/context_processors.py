# -*- coding: utf-8 -*-

from oms import settings

def mysetting(request):
    return {
        'STATIC_URL': settings.STATIC_URL,
    }
