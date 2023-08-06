# -*- coding: utf-8 -*-
from datetime import datetime

from ipylib.idebug import *


__all__ = [
    'BaseClass',
]

class BaseClass:

    def info(self):
        dbg.dict(self)
        return self
