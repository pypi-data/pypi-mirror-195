# -*- coding: utf-8 -*-
import os
import re
import csv
import json

from ipylib.idebug import *
from ipylib.ifile import get_filenames
from ipylib.ipath import clean_path
from ipylib.idatetime import DatetimeParser
from ipylib.inumber import *

from dataengineer import conf as cf


__all__ = [
    'FileReader',
    'FileWriter',
    'DataFileHandler',
    'DataFileManager',
]

class FileReader:

    @classmethod
    def _clean(self, data):
        for d in data:
            for k,v in d.copy().items():
                if isinstance(v, str) and len(v.strip()) == 0: del d[k]
        return data
    @classmethod
    def read_text(self, file):
        try:
            f = open(file, mode='r', encoding='utf-8')
            text = f.read()
            f.close()
        except Exception as e:
            logger.error(f'{self} | {e} | TEXT파일이 존재하지 않는다. {file}')
        else:
            logger.info(f'{self} | FilePath--> {file}')
            return text.strip()
    @classmethod
    def read_csv(self, file):
        try:
            data = []
            with open(file, newline='\n', encoding='utf8') as f:
                reader = csv.DictReader(f, delimiter=',')
                for row in reader: data.append(row)
                f.close()
        except Exception as e:
            logger.error(f'{self} | {e} | CSV파일이 존재하지 않는다. {file}')
        else:
            logger.info(f'{self} | FilePath--> {file}')
            return self._clean(data)
    @classmethod
    def read_json(self, file):
        try:
            f = open(file, 'r', encoding='utf8')
            data = []
            for line in f:
                js = json.loads(line.strip())
                data.append(js)
        except Exception as e:
            logger.error(f'{self} | {e} | {file}')
            return []
        else:
            logger.info(f'{self} | FilePath--> {file}')
            return self._clean(data)

class FileWriter:

    @classmethod
    def write_csv(self, file, fields, data):
        self._makedir(file)
        try:
            with open(file, 'w', newline='\n', encoding='utf8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fields)
                writer.writeheader()
                for d in data: writer.writerow(d)
            self.State('파일쓰기완료. 파일경로-->', file)
        except Exception as e:
            logger.error(e)
            raise
    @classmethod
    def write_json(self, file, data, colseq=None):
        self._makedir(file)
        try:
            with open(file, 'w', encoding='utf8') as f:
                for d in data:
                    if colseq is None: pass
                    else: d = {c:d[c] for c in colseq if c in d}
                    js = json.dumps(d, ensure_ascii=False)
                    f.write(f'{js}\n')
                f.close()
            self.State('파일쓰기완료. 파일경로-->', file)
        except Exception as e:
            logger.error(e)
            raise
    @classmethod
    def _makedir(self, file):
        try: os.makedirs(os.path.dirname(file))
        except Exception as e: pass
    @classmethod
    @stateFunc
    def State(self, *args): pass

class DataFileHandler:

    def __init__(self, modelName, schemaFileExt='.csv', dataFileExt='.json', descFileExt='.txt'):
        self.modelName = modelName
        self._schemaFileExt = schemaFileExt
        self._dataFileExt = dataFileExt
        self._descFileExt = descFileExt
        self.autosearch()
        dbg.dict(self)
    @property
    def DataDir(self): return cf.DataPath.DataDir
    @property
    def BackupDataDir(self): return cf.DataPath.BackupDataDir
    def autosearch(self):
        for root, dirs, files in os.walk(top=self.DataDir, topdown=True):
            for name in files:
                f, ext = os.path.splitext(name)
                if f == self.modelName:
                    filepath = os.path.join(root, name)
                    if ext == self._schemaFileExt: self.schemaFile = filepath
                    elif ext == self._dataFileExt: self.dataFile = filepath
                    elif ext == self._descFileExt: self.descFile = filepath

    def read_descFile(self): return FileReader.read_text(self.descFile)
    def read_schemaFile(self): return FileReader.read_csv(self.schemaFile)
    def read_dataFile(self): return FileReader.read_json(self.dataFile)
    def write_schemaFile(self, fields, data=[]):
        if hasattr(self, 'schemaFile'): file = self.schemaFile
        else: file = clean_path(f'{self.DataDir}/Schema/{self.modelName}.csv')
        FileWriter.write_csv(file, fields, data)
        self.autosearch()

class DataFileManager:
    @property
    def DataDir(self): return cf.DataPath.DataDir
    @property
    def BackupDataDir(self): return cf.DataPath.BackupDataDir
    @property
    def JSONFileList(self):
        jsonfiles = []
        for root, dirs, files in os.walk(top=self.DataDir, topdown=True):
            for name in files:
                f, ext = os.path.splitext(name)
                if ext == '.json': jsonfiles.append(name)
        return sorted(jsonfiles)
    @property
    def TextFileList(self):
        txtfiles = []
        for root, dirs, files in os.walk(top=self.DataDir, topdown=True):
            for name in files:
                f, ext = os.path.splitext(name)
                if ext == '.txt': txtfiles.append(name)
        return sorted(txtfiles)
