# -*- coding: utf-8 -*-
import os
import sys
import re

import pandas as pd

from ipylib.idebug import *

from dataengineer import config
from dataengineer.database import *
from dataengineer.collection import *
from dataengineer.models import *



class CollNameParser:

    def __init__(self, collName=None):
        if collName is not None:
            self.parse(collName)

    def parse(self, collName):
        pat = f'(_Schema_|_Test_|_Sample_)*([a-zA-Z]+-)*([a-zA-Z가-힣0-9\s]+)_*([a-z\d가-힣\.\(\)]+)*$'
        m = re.search(pat, collName)
        # print(m.groups(), name)
        collType, modelCate, modelName, param = m[1], m[2], m[3], m[4]

        self.collName = collName
        self.collType = 'Real' if collType is None else collType.replace('_','')
        self.collMode = self.collType.lower()
        self.modelName = modelName if modelCate is None else f"{modelCate}{modelName}"
        self.modelCate = None if modelCate is None else modelCate.replace('-','')
        self.param = param

        # if parser.collType == 'Real': collMode = 'real'
        # elif parser.collType == 'Test': collMode = 'test'
        # elif parser.collType == 'Sample': collMode = 'sample'

        return self

class CollectionList(DataModel):

    def __init__(self):
        super().__init__('CollectionList')
        self.parser = CollNameParser()

    @funcIdentity
    def create(self):
        mc = ModelCreator('CollectionList')
        mc.create_schema()
        names = db.list_collection_names(filter=None)
        data = self._collName_parser(names)
        self.drop()
        self.insert_many(data)

    def _collName_parser(self, names):
        # 컬렉션명 리스트를 데이타 구조화한다
        pat = f'(_Schema_|_Test_|_Sample_)*([a-zA-Z]+-)*([a-zA-Z가-힣0-9\s]+)_*([a-z\d가-힣\.\(\)]+)*$'
        data = []
        for name in names:
            # SectionGubun(name)
            self.parser.parse(name)
            d = {'collType':self.parser.collType,
                'modelCate':self.parser.modelCate,
                'modelName':self.parser.modelName,
                'param':self.parser.param,
                'collName':self.parser.collName}
            data.append(d)
        return data
    @classmethod
    def search(self, filter=None, **kw):
        model = DataModel('CollectionList')
        data = model.load(filter, {'_id':0}, **kw)
        df = pd.DataFrame(data)

        # 요약보고
        logger.info(f"len: {len(df)} | filter: {filter}")
        if len(df) > 0:
            collTypes = list(df.collType.unique())
            modelCates = list(df.modelCate.unique())
            modelNames = list(df.modelName.unique())
            params = list(df.param.unique())
            msg1 = f'collTypes: {collTypes}'
            msg2 = f'modelCates: {modelCates}'
            msg3 = f'len(modelNames): {len(modelNames)}'
            msg4 = f'len(params): {len(params)}'
            logger.info(f'요약보고-->\n{msg1}\n{msg2}\n{msg3}\n{msg4}')
            return df.sort_values(['collType','modelCate','modelName','param']).reset_index(drop=True)
        else:
            return df
