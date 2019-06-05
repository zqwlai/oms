
import os

from conf.default import *

ENVIRONMENT = os.environ.get('OMS_ENV', 'development')
conf_module = 'conf.settings_%s' % ENVIRONMENT
try:
    module = __import__(conf_module, globals(), locals(), ['*'])
except ImportError as e:
    raise ImportError("Could not import conf '%s' (Is it on sys.path?): %s" % (conf_module, e))


for setting in dir(module):
    locals()[setting] = getattr(module, setting)



