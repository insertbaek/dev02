'''
 @title	 미로게임 게임부분 컨트롤러 테스트
 @author 오진솔
 @date	 2021-10-06
 @update
 @description
'''

import sys, os, datetime, pymysql, json
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from config import ib_config as cfg
from config import ib_function as fn
from config import ib_dbconnection as dbc

# init classes
Cvalidate = fn.CValidate()
CFilePath = cfg.CFilepathInfo()
CDev02dbMaster = cfg.CDev02dbMaster()

# init variables
strLogAlias = "MazePlayController"
dtToday = datetime.datetime.now()
strProcessRunTime = "".join([dtToday.strftime('%Y%m%d'), '_', dtToday.strftime('%H')])
strSysLogFileName = "".join([strProcessRunTime, '_', CFilePath.alias, '_', strLogAlias, '.log'])
CibLogSys = fn.CibLog(CFilePath.python_syslog, str(strSysLogFileName), strLogAlias)

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

# List  to Dic / list의 값이 value로 생성됨. 키는 0부터 rgList 개수만큼
def ListToDic(rgList):
    
    if not rgList:
        return False 
    if type(rgList) != "<class 'list'>":
        return False
    
    rgDic = {i : rgList[i] for i in range(len(rgList))}
    return rgDic


class MazePlayController:

    # SELECT
    def fnGetGameInfo (nGameSeq):
     
        try:
            # 필수 항목이 존재하는지 체크
            if not nGameSeq:
                raise Exception('필수 데이터가 비어있습니다.')

            CDev02MasterDbconn = dbc.DbConnection('dbDev02')
            if (CDev02MasterDbconn.Connection(isAutoCommitType=True, isDictType=True) == False):
                raise Exception('DB 연결에 실패하였습니다.')

            rstList = CDev02MasterDbconn.Execute('SELECT * FROM ib_dev02_01.maze_play_log_2021 WHERE seq= %s', [nGameSeq])
            if (rstList[0] == False):
                raise Exception('해당 항목에 대한 결과를 찾지 못하였습니다.')
            
            #JSON 형식으로 변환하여 출력
            strResult = json.dumps(rstList[1], ensure_ascii = False)
            print(strResult)

            return strResult
        except Exception as e:
            CibLogSys.error(e)
            return str(e)
        finally :
            CDev02MasterDbconn.DisConnection()

    # INSERT
    def fnSetGame (self, rgGameInfo):
        try:
            # 필수 항목이 존재하는지 체크
            if not rgGameInfo:
                raise Exception('필수 데이터가 비어있습니다.')

            CDev02MasterDbconn = dbc.DbConnection('dbDev02')
            if (CDev02MasterDbconn.Connection(isAutoCommitType=False, isDictType=True) == False):
                raise Exception('DB 연결에 실패하였습니다.')

            rstGameInfo = CDev02MasterDbconn.Execute("INSERT INTO ib_dev02_01.test_tbl_1 SET data1 = %(data1)s, data2 = %(data2)s", rgGameInfo)
            
            if (rstGameInfo[0] == False):
                raise Exception('해당 항목에 대한 결과를 찾지 못하였습니다.')
            
            CDev02MasterDbconn.TransactionCommit()

            return CDev02MasterDbconn.InsertLastId()
        except Exception as e:
            CibLogSys.error(e)
            return str(e)
        finally :
            CDev02MasterDbconn.DisConnection()

    # UPDATE  
    def fnSetResult (self, rgGameInfo):
        try:
            # 필수 항목이 존재하는지 체크
            if not rgGameInfo:
                raise Exception('필수 데이터가 비어있습니다.')

            CDev02MasterDbconn = dbc.DbConnection('dbDev02')
            if (CDev02MasterDbconn.Connection(isAutoCommitType=False, isDictType=True) == False):
                raise Exception('DB 연결에 실패하였습니다.')

            rstGameInfo = CDev02MasterDbconn.Execute("UPDATE ib_dev02_01.maze_play_log_2021 SET winner = %s, loser = %s, end_time = now()", rgGameInfo)
            
            if (rstGameInfo[0] == False):
                raise Exception('해당 항목에 대한 결과를 찾지 못하였습니다.')
            
            CDev02MasterDbconn.TransactionCommit()

            return True
        except Exception as e:
            CibLogSys.error(e)
            return str(e)
        finally :
            CDev02MasterDbconn.DisConnection()

    # DELETE
    def fnSetDelGame (self, nGameSeq):
        try:
            # 필수 항목이 존재하는지 체크
            if not nGameSeq:
                raise Exception('필수 데이터가 비어있습니다.')

            CDev02MasterDbconn = dbc.DbConnection('dbDev02')
            if (CDev02MasterDbconn.Connection(isAutoCommitType=False, isDictType=True) == False):
                raise Exception('DB 연결에 실패하였습니다.')

            rstGameInfo = CDev02MasterDbconn.Execute("DELETE FROM ib_dev02_01.maze_play_log_2021 WHERE seq = %s", nGameSeq)

            if (rstGameInfo[0] == False):
                raise Exception('해당 항목에 대한 결과를 찾지 못하였습니다.')
            
            CDev02MasterDbconn.TransactionCommit()

            return True
        except Exception as e:
            CibLogSys.error(e)
            return str(e)
        finally :
            CDev02MasterDbconn.DisConnection()

    # JSON to DIC
    def getJsonData(self, strJson):
        try:
            if str(type(strJson)) != "<class 'str'>":
                raise Exception ('올바른 형식의 데이터가 아닙니다.')

            strConvJson = json.loads(strJson)

            return strConvJson
        except Exception as e:
            CibLogSys.error(e)
            return str(e)

    def PostTest (var1, var2, var3, var4):
        print("input OK : "+var1+var2+var3+var4)
