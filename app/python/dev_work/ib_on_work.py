#!/usr/local/bin/python3.9
import subprocess, sys, os, datetime
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import pymysql
from inspect import currentframe, getframeinfo
from config import ib_config as cfg
from config import ib_function as fn

# init classes
CArray = fn.CArray()
CValidate = fn.CValidate()
CFilePath = cfg.CFilepathInfo()
CDevRepairdbMaster = cfg.CDevRepairdbMaster()

try:
	for oConfig in [CFilePath, CDevRepairdbMaster]:
		bResult = CValidate.isDictEmpty(oConfig.__dict__)

		if not bResult:
			raise Exception(CValidate.getDictEmpty())
except Exception as e:
	print('환경설정 중' + str(e) + '항목 정의가 올바르지 않습니다.')
	sys.exit()
finally:
	del oConfig, bResult

# init variables
strLogAlias = "mysql_restore"
dtToday = datetime.datetime.now()
strProcessRunTime = "".join([dtToday.strftime('%Y%m%d'), '_', dtToday.strftime('%H')])
strSysLogFileName = "".join([strProcessRunTime, '_', CFilePath.alias, '_', strLogAlias, '.log'])
CibLogSys = fn.CibLog(CFilePath.python_syslog, str(strSysLogFileName), strLogAlias)
dtYesterday = dtToday - datetime.timedelta(1)

# init databases
CDevRepairMasterDbconn = pymysql.connect(host=CDevRepairdbMaster.host, user=CDevRepairdbMaster.user, password=CDevRepairdbMaster.password, db=CDevRepairdbMaster.db, port=CDevRepairdbMaster.port, charset='utf8')

try:
    if not os.path.exists(CFilePath.database):
        os.makedirs(CFilePath.database)

    os.chdir(CFilePath.root)
    subprocess.call(" ".join(['git', 'pull']), shell=True)

    rgBackupFiles = os.listdir(CFilePath.database)
    rgTextMatchBackupFiles = CArray.inMatch('schema', rgBackupFiles)
    rgMatchBackupFiles = CArray.inMatch(dtYesterday.strftime('%Y%m%d'), rgTextMatchBackupFiles)

    
except Exception as e:
	if CValidate.isEmpty(e) == False:
		CibLogSys.error('심각한 오류가 발생하였습니다.')
	else:
		CibLogSys.error(e)

	sys.exit()
finally:
    #CibLogSys.debug(qryTableInfo + ' [result : ' + str(strDumpTableInfo)  + ']')
	del rgBackupFiles, rgTextMatchBackupFiles, rgMatchBackupFiles



#print(strProcessRunTime)
#print(CFilePath.python)
#print(CDev02dbMaster.host)
