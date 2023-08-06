# -*- coding: utf-8 -*-
import re

from bson.objectid import ObjectId

from ipylib.idebug import *
from ipylib.idatetime import DatetimeParser, timedelta, datetime


from dataengineer import models


__all__ = [
    'AutoFilter',
    'AutoFilterV2',
]


class AutoFilter:

    def __init__(self, schema):
        self.schema = schema
        self.filter = {}
        # CollectionColumns
        self.collcols = list(set(self.schema.distinct('column') + ['_id']))
        self.strcols = self.schema.distinct('column', {'dtype':'str'})
        self.dtcols = self.schema.dtcols
        self.boolcols = self.schema.distinct('column', {'dtype':'boolean'})

    def clear(self):
        self.filter.clear()
        return self
    def _autoclean(self, f):
        # 스키마컬럼에 없는 필터조건을 제거한다
        return {c:f[c] for c in self.collcols if c in f}
    def _set(self, f):
        f = self._autoclean(f)
        self.clear()
        self.filter.update(f)
        return self
    def search(self, filter):
        # MongoDB 검색 오퍼레이션을 최대한 사용하라.
        # 데이타 타입 자동변환만 사용하되, ipylib 를 먼저 활용하라
        # -> 더 직관적이고, MongoDB 를 더 잘 이해할 수 있다
        f = {} if filter is None else filter
        return self._set(f)
    def today(self):
        self.clear()
        t = datetime.today().astimezone()
        t = t.replace(hour=0, minute=0, second=0, microsecond=0)
        filters = []
        for c in self.dtcols:
            filters.append({c:{'$gte':t}})
        if len(filters) > 0:
            self.filter.update({'$or':filters})
        return self
    def oneday(self, **kw):
        self.clear()
        for k,v in kw.items():
            if k in self.dtcols:
                fromdt = self.schema.parse_value(k, v)
                todt = fromdt + timedelta(days=+1)
                self.filter.update({k:{'$gte':fromdt, '$lt':todt}})
        return self
    def period(self, fromdt, todt):
        self.clear()
        fromdt = DatetimeParser(fromdt)
        todt = DatetimeParser(todt)
        filters = []
        for c in self.dtcols:
            filters.append({c:{'$gte':fromdt, '$lt':todt}})
        if len(filters) > 0:
            self.filter.update({'$or':filters})
        return self
    def lastday(self):
        self.clear()
        filters = []
        for c in self.dtcols:
            filters.append({c:{'$gte':datetime.today().astimezone()}})
        if len(filters) > 0:
            self.filter.update({'$or':filters})
        return self

class AutoFilterV2(AutoFilter):

    def __init__(self, modelName):
        schema = modelsV2.SchemaModel(modelName)
        super().__init__(schema)
