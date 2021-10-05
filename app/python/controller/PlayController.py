'''
 @title	 미로게임 게임부분 컨트롤러
 @author 오진솔
 @date	 2021-10-05
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

class PlayGameController:

    # reconnect databases
    def DBconn(self):
        CDev02MasterDbconn = pymysql.connect(host=CDev02dbMaster.host, user=CDev02dbMaster.user, password=CDev02dbMaster.password, db=CDev02dbMaster.db, port=CDev02dbMaster.port, charset='utf8')
        return CDev02MasterDbconn.cursor(pymysql.cursors.DictCursor)

    def getGameInfo (self, nGameSeq):
        try:
            # 필수 항목이 존재하는지 체크
            if not nGameSeq:
                raise Exception('필수 데이터가 비어있습니다.')

            with self.DBconn() as CDev02MasterDbconn:
                if (CDev02MasterDbconn.connection.open != True):
                    raise Exception('서비스 상태를 확인해주세요.')

                with CDev02MasterDbconn.cursor(pymysql.cursors.DictCursor) as CDev02MasterDbconnCurs:
                    qryGameInfo = "SELECT * FROM ib_dev02_01.maze_gameinfo WHERE seq= %s"
                    rstGameInfo = CDev02MasterDbconnCurs.execute(qryGameInfo, nGameSeq)

                    if rstGameInfo  == -1:
                        raise Exception('해당 항목에 대한 결과를 찾지 못하였습니다.')
                    rgResult = CDev02MasterDbconnCurs.fetchall()
                    strResult = json.dumps(rgResult, ensure_ascii = False)
            return strResult
        except Exception as e:
            return str(e)

    def setGame (self, rgGameInfo):

        try:
            # 필수 항목이 존재하는지 체크
            if not rgGameInfo:
                raise Exception('필수 데이터가 비어있습니다.')
            with self.DBconn() as CDev02MasterDbconn:
                if (CDev02MasterDbconn.connection.open != True):
                    raise Exception('서비스 상태를 확인해주세요.')

                qryGameInfo = "INSERT INTO ib_dev02_01.maze_play_log_2021 SET player1_no = %s, player1_point = %s, player2_no = %s, player2_point = %s, reg_date = now()"             
                rstGameInfo = CDev02MasterDbconn.execute(qryGameInfo, rgGameInfo['player1_no'],rgGameInfo['player1_point'],rgGameInfo['player2_no'],rgGameInfo['player2_point'])

                if rstGameInfo  != 1:
                        CDev02MasterDbconn.rollback()
                        raise Exception('게임정보를 등록하지 못하였습니다..')
                CDev02MasterDbconn.commit()
            return True
        except Exception as e:
            return str(e)

