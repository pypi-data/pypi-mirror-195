# -*- coding: utf-8 -*-
from ipylib.idebug import *
from ipylib.idatetime import *

from dataengineer.models import *

__all__ = [
    'WorkerSchedule',
]

class WorkerSchedule(DataModel):

    def __init__(self):
        super().__init__(self.__class__.__name__, 'real')
        self.schema.view()
    @funcIdentity
    def set_intraday_schedule(self, t='08:30:00'):
        dt = datetime.strptime(t, '%H:%M:%S')
        delta = timedelta(seconds=5)
        trnames = ['당일거래량상위','거래량급증','거래대금상위','예수금상세현황요청','계좌평가잔고내역요청','계좌평가현황요청']
        at_times = []
        for i in range(len(trnames)):
            at_times.append(dt.isoformat(timespec='seconds').split('T')[1])
            dt = dt + delta

        for trname, at in zip(trnames, at_times):
            self.update_one({'trname':trname}, {'$set':{'start_dt':at}})
    @funcIdentity
    def set_daily_schedule(self, t='07:00'):
        self.update_many({'type':'Daily', 'worker':{'$ne':None}}, {'$set':{'at_times':[t]}})
