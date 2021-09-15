#!/usr/local/bin/python3.9
import subprocess, sys, os, datetime
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import ib_config as cfg
import ib_function as fn
import pymysql
from inspect import currentframe, getframeinfo

# init class
Cvalidate = fn.CValidate()
CFilePath = cfg.CFilepathInfo()
CDev02dbMaster = cfg.CDev02dbMaster()

try:
    for CConfig in [CFilePath, CBackupdbInfo, CReplicationRule, CGeneral]:
        bResult = Cvalidate.isDictEmpty(CConfig.__dict__)

        if not bResult:
            raise Exception(Cvalidate.getDictEmpty())
except Exception as e:
    sys.exit()
finally:
    del CConfig, bResult

print(bResult)