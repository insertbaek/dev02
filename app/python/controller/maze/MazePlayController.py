'''
 @title	 미로게임 게임부분 컨트롤러 테스트
 @author 오진솔
 @date	 2021-10-06
 @update
 @description
'''

import sys, os, datetime, pymysql, json
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config import ib_config as cfg
from config import ib_function as fn


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

class MazePlayController:

    # List  to Dic / list의 값이 value로 생성됨. 키는 0부터 rgList 개수만큼
    def ListToDic(rgList):
        
        if not rgList:
            return False 

        if type(rgList) != "<class 'list'>":
            return False
        
        rgDic = {i : rgList[i] for i in range(len(rgList))}
        return rgDic

    # SELECT
    def getGameInfo (self, nGameSeq):
        try:
            # 필수 항목이 존재하는지 체크
            if not nGameSeq:
                raise Exception('필수 데이터가 비어있습니다.')
            with pymysql.connect(host=CDev02dbMaster.host, user=CDev02dbMaster.user, password=CDev02dbMaster.password, db=CDev02dbMaster.db, port=CDev02dbMaster.port, charset='utf8') as CDev02MasterDbconn:
                with CDev02MasterDbconn.cursor(pymysql.cursors.DictCursor) as CDev02MasterCursor:
                    if (CDev02MasterDbconn.open != True):
                        raise Exception('서비스 상태를 확인해주세요.')
                
                    qryGameInfo = "SELECT * FROM ib_dev02_01.maze_play_log_2021 WHERE seq= %s"
                    print(qryGameInfo)
                    rstGameInfo = CDev02MasterCursor.execute(qryGameInfo, nGameSeq)
                    if rstGameInfo  == -1:
                        raise Exception('해당 항목에 대한 결과를 찾지 못하였습니다.')
                    rgResult = CDev02MasterCursor.fetchall()

                    #JSON 형식으로 변환하여 출력
                    strResult = json.dumps(rgResult, ensure_ascii = False)
            return strResult
        except Exception as e:
            CibLogSys.error(e)
            return str(e)

    # INSERT
    def setGame (self, rgGameInfo):

        try:
            # 필수 항목이 존재하는지 체크
            if not rgGameInfo:
                raise Exception('필수 데이터가 비어있습니다.')
            with pymysql.connect(host=CDev02dbMaster.host, user=CDev02dbMaster.user, password=CDev02dbMaster.password, db=CDev02dbMaster.db, port=CDev02dbMaster.port, charset='utf8') as CDev02MasterDbconn:
                with CDev02MasterDbconn.cursor(pymysql.cursors.DictCursor) as CDev02MasterCursor:
                    if (CDev02MasterDbconn.open != True):
                        raise Exception('서비스 상태를 확인해주세요.')

                    qryGameInfo = "INSERT INTO ib_dev02_01.test_tbl_1 SET data1 = %(data1)s, data2 = %(data2)s"
                    rstGameInfo = CDev02MasterCursor.execute(qryGameInfo, rgGameInfo)
                    if rstGameInfo  != 1:
                        CDev02MasterDbconn.rollback()
                        raise Exception('게임정보를 등록하지 못하였습니다..')
                    CDev02MasterDbconn.commit()
            return CDev02MasterCursor.lastrowid
        except Exception as e:
            CibLogSys.error(e)
            return str(e)

    # UPDATE  
    def setResult (self, rgGameInfo):

        try:
            # 필수 항목이 존재하는지 체크
            if not rgGameInfo:
                raise Exception('필수 데이터가 비어있습니다.')

            with pymysql.connect(host=CDev02dbMaster.host, user=CDev02dbMaster.user, password=CDev02dbMaster.password, db=CDev02dbMaster.db, port=CDev02dbMaster.port, charset='utf8') as CDev02MasterDbconn:
                with CDev02MasterDbconn.cursor(pymysql.cursors.DictCursor) as CDev02MasterCursor:
                    if (CDev02MasterDbconn.open != True):
                        raise Exception('서비스 상태를 확인해주세요.')

                    qryGameInfo = "UPDATE ib_dev02_01.maze_play_log_2021 SET winner = %s, loser = %s, end_time = now()"             
                    rstGameInfo = CDev02MasterCursor.execute(qryGameInfo, rgGameInfo)

                    if rstGameInfo  != 1:
                        CDev02MasterDbconn.rollback()
                        raise Exception('게임정보를 갱신하지 못하였습니다..')
                CDev02MasterDbconn.commit()
            return True
        except Exception as e:
            CibLogSys.error(e)
            return str(e)

    # DELETE
    def setDelGame (self, nGameSeq):

        try:
            # 필수 항목이 존재하는지 체크
            if not nGameSeq:
                raise Exception('필수 데이터가 비어있습니다.')

            with pymysql.connect(host=CDev02dbMaster.host, user=CDev02dbMaster.user, password=CDev02dbMaster.password, db=CDev02dbMaster.db, port=CDev02dbMaster.port, charset='utf8') as CDev02MasterDbconn:
                with CDev02MasterDbconn.cursor(pymysql.cursors.DictCursor) as CDev02MasterCursor:
                    if (CDev02MasterDbconn.open != True):
                        raise Exception('서비스 상태를 확인해주세요.')

                    qryGameInfo = "DELETE FROM ib_dev02_01.maze_play_log_2021 WHERE seq = %s"             
                    rstGameInfo = CDev02MasterCursor.execute(qryGameInfo, nGameSeq)

                    if rstGameInfo  != 1:
                        CDev02MasterDbconn.rollback()
                        raise Exception('게임정보를 삭제하지 못하였습니다..')
                    CDev02MasterDbconn.commit()
            return True
        except Exception as e:
            CibLogSys.error(e)
            return str(e)

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