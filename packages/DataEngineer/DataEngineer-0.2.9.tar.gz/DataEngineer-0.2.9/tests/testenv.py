# -*- coding: utf-8 -*-
from idevenv import Syspath
sp = Syspath('DataEngineer')
sp.add_uninstall_packages(['ipylib','idebug','DataEngineer'])

import sys
import unittest
from time import sleep
from datetime import datetime, date, time, timedelta

from idebug import *

from dataengineer.conf import *
ProjectInfo.set('ProjectName', 'DataEngineer')
Database.set('name', 'DataEngineer')
show()


class UnitTester(unittest.TestCase):

    def run_test(self, testList=None):
        if testList is None:
            self.testList = [a for a in dir(self) if re.search('^test\d+', a) is not None]
        elif isinstance(testList, int):
            self.testList = [f'test{str(n).zfill(2)}' for n in [testList]]
        elif isinstance(testList, list):
            self.testList = [f'test{str(n).zfill(2)}' for n in testList]
        dbg.dict(self)

        for func in self.testList:
            getattr(self, func)()
        logger.info(f'{self} | Done.')


if __name__ == '__main__':
    sp.view()

    PartGubun('메인시작')
    pp.pprint(dir())

    tester = UnitTester()
    view_dir(tester)
