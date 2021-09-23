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
CDevRepairdbMaster = cfg.CDevRepairdbMaster()

try:
	for oConfig in [CFilePath, CDevRepairdbMaster]:
		bResult = Cvalidate.isDictEmpty(oConfig.__dict__)

		if not bResult:
			raise Exception(Cvalidate.getDictEmpty())
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

    os.chdir(CFilePath.database)
    rgBackupFiles = subprocess.check_output(CFilePath.findfiles + ' ' + dtYesterday.strftime('%Y%m%d') + '*schema*.sql', shell=True, universal_newlines=True).strip().split('\n')

    print(rgBackupFiles)

    '''
	with CDevRepairMasterDbconn.cursor(pymysql.cursors.DictCursor) as CDevRepairMasterDbconnCurs:
		rgBulkTableInfo = [CDevRepairdbMaster.db]
		qryTableInfo = "SELECT table_name FROM information_schema.tables WHERE table_schema=%s"
		CDevRepairMasterDbconnCurs.execute(qryTableInfo, rgBulkTableInfo)
		rstTableInfoList = CDevRepairMasterDbconnCurs.fetchall()

		strDumpTableInfo = " ".join([rgTableInfo['TABLE_NAME'] for rgTableInfo in rstTableInfoList])

		strUserAlias = subprocess.check_output(" ".join(['git', 'config', '--list', '|', 'grep', '-i', 'name']), shell=True, universal_newlines=True).strip().split('\n')[0].split('=')

		subprocess.call(" ".join(['mysqldump', '-u' + CDevRepairdbMaster.user, '-p' + CDevRepairdbMaster.password, '-h' + CDevRepairdbMaster.host, '--single-transaction', '--default-character-set=utf8', '--skip-lock-tables', '--no-data', CDevRepairdbMaster.db, strDumpTableInfo, '>', CFilePath.database + '/' + strProcessRunTime + '_' + CDevRepairdbMaster.db + '_schema_' + strUserAlias[1] + '.sql']), shell=True)
		subprocess.call(" ".join(['mysqldump', '-u' + CDevRepairdbMaster.user, '-p' + CDevRepairdbMaster.password, '-h' + CDevRepairdbMaster.host, '--single-transaction', '--default-character-set=utf8', '--skip-lock-tables', '-t', CDevRepairdbMaster.db, strDumpTableInfo, '>', CFilePath.database + '/' + strProcessRunTime+ '_' + CDevRepairdbMaster.db + '_data_' + strUserAlias[1] + '.sql']), shell=True)

		subprocess.call(" ".join(['git', 'add', '.']), shell=True)
		subprocess.call(" ".join(['git', 'commit', '-am', '"' + str(dtToday.strftime('%Y-%m-%d')) + ' ' + str(strUserAlias[1]) + ' MySQL 데이터 백업''"']), shell=True)
		subprocess.call(" ".join(['git', 'push', '-u', 'origin', 'master']), shell=True)

		if len(rstTableInfoList) < 1:
			raise Exception('테이블이 존재하지 않습니다.')
    '''
except Exception as e:
	if Cvalidate.isEmpty(e) == False:
		CibLogSys.error('심각한 오류가 발생하였습니다.')
	else:
		CibLogSys.error(e)

	sys.exit()
finally:
    print('success')
    '''
	CibLogSys.debug(qryTableInfo + ' [result : ' + str(strDumpTableInfo)  + ']')
	del CDevRepairMasterDbconnCurs, rgBulkTableInfo, qryTableInfo, rstTableInfoList, strDumpTableInfo
    '''


#print(strProcessRunTime)
#print(CFilePath.python)
#print(CDev02dbMaster.host)
