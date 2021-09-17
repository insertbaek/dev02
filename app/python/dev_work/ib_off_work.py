#!/usr/local/bin/python3.9
import subprocess, sys, os, datetime
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import pymysql
from inspect import currentframe, getframeinfo
from config import ib_config as cfg
from config import ib_function as fn

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
strCurrentDate = datetime.datetime.now().strftime('%Y-%m-%d')
strProcessRunTime = "".join([datetime.datetime.now().strftime('%Y%m%d'), '_', datetime.datetime.now().strftime('%H')])
strSysLogFileName = "".join([strProcessRunTime, '_', CFilePath.alias, '_', strLogAlias, '.log'])
CibLogSys = fn.CibLog(CFilePath.python_syslog, str(strSysLogFileName), strLogAlias)

# init databases
CDev02MasterDbconn = pymysql.connect(host=CDev02dbMaster.host, user=CDev02dbMaster.user, password=CDev02dbMaster.password, db=CDev02dbMaster.db, port=CDev02dbMaster.port, charset='utf8')

try:
	with CDev02MasterDbconn.cursor(pymysql.cursors.DictCursor) as CDev02MasterDbconnCurs:
		rgBulkTableInfo = [CDev02dbMaster.db]
		qryTableInfo = "SELECT table_name FROM information_schema.tables WHERE table_schema=%s"
		CDev02MasterDbconnCurs.execute(qryTableInfo, rgBulkTableInfo)
		rstTableInfoList = CDev02MasterDbconnCurs.fetchall()

		strDumpTableInfo = " ".join([rgTableInfo['TABLE_NAME'] for rgTableInfo in rstTableInfoList])

		if not os.path.exists(CFilePath.database):
			os.makedirs(CFilePath.database)

		strUserAlias = subprocess.check_output(" ".join(['git', 'config', '--list', '|', 'grep', '-i', 'name']), shell=True, universal_newlines=True).strip().split('\n')[0].split('=')

		subprocess.call(" ".join(['mysqldump', '-u' + CDev02dbMaster.user, '-p' + CDev02dbMaster.password, '-h' + CDev02dbMaster.host, '--single-transaction', '--default-character-set=utf8', '--skip-lock-tables', '--no-data', CDev02dbMaster.db, strDumpTableInfo, '>', CFilePath.database + '/' + strProcessRunTime + '_' + CDev02dbMaster.db + '_schema_' + strUserAlias[1] + '.sql']), shell=True)
		subprocess.call(" ".join(['mysqldump', '-u' + CDev02dbMaster.user, '-p' + CDev02dbMaster.password, '-h' + CDev02dbMaster.host, '--single-transaction', '--default-character-set=utf8', '--skip-lock-tables', '-t', CDev02dbMaster.db, strDumpTableInfo, '>', CFilePath.database + '/' + strProcessRunTime+ '_' + CDev02dbMaster.db + '_data_' + strUserAlias[1] + '.sql']), shell=True)

		os.chdir(CFilePath.root)
		subprocess.call(" ".join(['git', 'pull']))
		subprocess.call(" ".join(['git', 'add', '.']))
		subprocess.call(" ".join(['git', 'commit', '-m"' + strCurrentDate + ' ' + strUserAlias + ' MySQL 데이터 백업"']))
		subprocess.call(" ".join(['git', 'push', '-u', 'origin', 'master']))
		

		if len(rstTableInfoList) < 1:
			raise Exception('테이블이 존재하지 않습니다.')
except Exception as e:
	if Cvalidate.isEmpty(e) == False:
		CibLogSys.error('심각한 오류가 발생하였습니다.')
	else:
		CibLogSys.error(e)

	sys.exit()
finally:
	CibLogSys.debug(qryTableInfo + ' [result : ' + str(strDumpTableInfo)  + ']')
	del CDev02MasterDbconnCurs, rgBulkTableInfo, qryTableInfo, rstTableInfoList, strDumpTableInfo


#print(strProcessRunTime)
#print(CFilePath.python)
#print(CDev02dbMaster.host)
