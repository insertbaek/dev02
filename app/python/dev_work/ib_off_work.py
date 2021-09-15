#!/usr/local/bin/python3.9
import subprocess, sys, os, datetime
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from config import ib_config as cfg
from config import ib_function as fn
import pymysql
from inspect import currentframe, getframeinfo

# init classes
Cvalidate = fn.CValidate()
CFilePath = cfg.CFilepathInfo()
CDev02dbMaster = cfg.CDev02dbMaster()

try:
	for oConfig in [CFilePath, CDev02dbMaster]:
		bResult = Cvalidate.isDictEmpty(oConfig.__dict__)

		if not bResult:
			raise Exception(Cvalidate.getDictEmpty())
except Exception as e:
	print('환경설정 중' + str(e) + '항목 정의가 올바르지 않습니다.')
	sys.exit()
finally:
	del oConfig, bResult

# init variables
strLogAlias = "mysqldump"
strProcessRunTime = "".join([datetime.datetime.now().strftime('%Y%m%d'), '_', datetime.datetime.now().strftime('%H')])
strSysLogFileName = "".join([strProcessRunTime, '_', CFilePath.alias, '_', strLogAlias, '.log'])
CibLogSys = fn.CibLog(CFilePath.backup_syslog, str(strSysLogFileName), strLogAlias)

# init databases
CDev02MasterDbconn = pymysql.connect(host=CDev02dbMaster.host, user=CDev02dbMaster.user, password=CDev02dbMaster.password, db=CDev02dbMaster.db, port=CDev02dbMaster.port, charset='utf8')

try:
	with CDev02MasterDbconn.cursor(pymysql.cursors.DictCursor) as CDev02MasterDbconnCurs:
		qryTableInfo = "SHOW TABLES;"
		CDev02MasterDbconnCurs.execute(qryTableInfo)
		rstTableInfoList = CDev02MasterDbconnCurs.fetchall()

		print(rstTableInfoList)

		if len(rstTableInfoList) < 1:
			raise Exception('테이블이 존재하지 않습니다.')
except Exception as e:
	if Cvalidate.isEmpty(e) == False:
		CibLogSys.error('심각한 오류가 발생하였습니다.')
	else:
		CibLogSys.error(e)
	sys.exit()
finally:
	CibLogSys.info(qryTableInfo + ' [result : ' + str(qryTableInfo)  + ']')
	CibLogSys.debug(qryTableInfo)
	del CDev02MasterDbconnCurs, qryTableInfo


print(strProcessRunTime)
print(CFilePath.python)
print(CDev02dbMaster.host)
