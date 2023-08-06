# -*- coding: utf-8 -*-
import re

from ipylib.idebug import *
from ipylib.ipath import clean_path

__all__ = [
    'ProjectInfo',
    'Database',
    'DataPath',
    'show',
]

class BaseObject:
    @classmethod
    def set(self, k, v): setattr(self, k, v)
    @classmethod
    def repr(self):
        ComponentName = self().__class__.__name__
        pretty_title(f'DataEngineer.Configuration.{ComponentName}')
        attrs = sorted(self.__dict__)
        for k in attrs: print(k, ':', getattr(self(), k))

class ProjectInfo(BaseObject):
    def __init__(self): super().__init__()

class Database(BaseObject):
    host = 'localhost'
    port = 27017
    document_class = dict
    tz_aware = True
    connect = True
    maxPoolSize = None
    minPoolSize = 100
    connectTimeoutMS = 60000
    waitQueueMultiple = None
    retryWrites = True

    @classmethod
    def params(self):
        li = ['host','port','document_class','tz_aware','connect','maxPoolSize','minPoolSize',
        'connectTimeoutMS','waitQueueMultiple','retryWrites']
        return {a:getattr(self, a) for a in li}

class DataPath(BaseObject):
    def __init__(self): super().__init__()
    @property
    def DataDir(self): return clean_path(f'C:\pypjts\{ProjectInfo.ProjectName}\Data')
    @property
    def BackupDataDir(self): return clean_path(f'D:\BackupData\MongoDB\{ProjectInfo.ProjectName}')


DataPath = DataPath()

def show():
    ProjectInfo.repr()
    Database.repr()
    DataPath.repr()
