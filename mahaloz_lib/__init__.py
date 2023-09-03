__version__ = "1.0.0"

#
# logging
#

import logging
logging.getLogger("mahaloz_lib").addHandler(logging.NullHandler())
from .logger import Loggers
loggers = Loggers()
del Loggers
del logging
