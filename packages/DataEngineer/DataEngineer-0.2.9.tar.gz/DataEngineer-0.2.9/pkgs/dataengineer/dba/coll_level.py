# -*- coding: utf-8 -*-
import os
import sys
import re

import pandas as pd

from ipylib.idebug import *
from ipylib.idatetime import *

from dataengineer.dba.db_level import *
from dataengineer.database import *
from dataengineer.models import *


__all__ = [
    'modify_database',
    'modify_collection',
    'postparse_data',
    'drop_duplicates',
    'view_TR_rawdata',
    'inspect_DataModel',
    'analyze_RealFID',
]


def modify_database(n):
    if n == 1:
        names = db.list_collection_names(filter={'name':{'$regex':'_Schema_op', '$options':'i'}})
        for name in names:
            db[name].drop()


def modify_collection(n):
    if n == 1:
        filter = {'colName':'input'}
        update = {'$set':{'colName':'id'}}
        SchemaModel('TRInput').update_one(filter, update)
    elif n == 2:
        update = {'$set':{'updated_dt':datetime(2021,5,4).astimezone()}}
        db.Company.update_many({}, update)


def postparse_data(model):
    cursor = model.find()
    data = model.schema.parse_data(list(cursor))
    for d in data:
        try:
            filter = {'_id':d['_id']}
            update = {'$set':d}
            model.update_one(filter, update)
        except Exception as e:
            logger.error(e)
            pp.pprint(d)
    print('Done')


def drop_duplicates(modelName):
    model = DataModel(modelName)
    keycols = model.schema.distinct('colName', {'role':{'$in':['key']}})
    projection = {k:1 for k in keycols}
    data = model.load(None, projection)
    df = pd.DataFrame(data)
    print(len(df))
    # return df
    TF = df.duplicated(subset=keycols, keep=False)
    print(len(df[TF]))
    # return df[TF]
    TF = df.duplicated(subset=keycols, keep='last')
    print(len(df[TF]))
    # return df[TF]

    if len(df[TF]) > 0:
        ids = list(df[TF]._id)
        model.delete_many({'_id':{'$in':ids}})


def view_TR_rawdata(trcode):
    filter = {'input':{'$regex':trcode, '$options':'i'}}
    projection = {'input':1, 'output':1}
    cursor = db.TRList.find(filter, projection)
    for d in list(cursor):
        for k,v in d.items():
            if k == 'input':
                for line in v.splitlines():
                    print(line)
            else:
                print(v)


def inspect_DataModel(modelName):
    pretty_title(modelName)
    model = DataModel(modelName)
    dbg.dict(model.schema)
    model.schema.view()
    dbg.dict(model)
    model.view()


def analyze_RealFID():
    PartGubun('analyze_RealFID')

    data = DataModel('RealFID').load(None, {'_id':0})
    df = pd.DataFrame(data)

    # RealFID 분석
    df['cnt'] = df.realtypes.apply(lambda x: len(x))
    df['realtype'] = df.realtypes.apply(lambda x: x[0] if len(x) == 1 else '_None')
    # df = df.sort_values('cnt')
    _df1 = df.query('cnt == 1')
    _df2 = df.query('cnt > 1')

    pretty_title('1개의 Realtype에만 존재하는 FIDs')
    _df1.info()
    _df1 = _df1.sort_values(['name','fid']).reset_index(drop=True)
    print(_df1[:60])
    if len(_df1) > 60: print(_df2[-60:])

    pretty_title('2개 이상의 Realtype에 존재하는 FIDs')
    _df2.info()
    _df2 = _df2.sort_values(['cnt','name','fid'], ascending=False).reset_index(drop=True)
    print(_df2[:60])
    if len(_df2) > 60: print(_df2[-60:])

    return df
