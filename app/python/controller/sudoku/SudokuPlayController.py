'''
 @title	 스도쿠 게임부분 컨트롤러 테스트
 @author 오진솔
 @date	 2021-10-06
 @update
 @description
'''

import sys, os, datetime, pymysql, json, random
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

class SudokuPlayController:

    def __init__(self):
        self.origin_board = [[0 for j in range(0,9)] for i in range(0,9)]
        self.board = [[0 for j in range(0,9)] for i in range(0,9)]
        self.row = [[0 for j in range(0,10)] for i in range(0,10)]
        self.col = [[0 for j in range(0,10)] for i in range(0,10)]
        self.diag = [[0 for j in range(0,10)] for i in range(0,10)]
        self.terminate_flag = False
    # connect databases
    def DBconn(self):
        CDev02MasterDbconn = pymysql.connect(host=CDev02dbMaster.host, user=CDev02dbMaster.user, password=CDev02dbMaster.password, db=CDev02dbMaster.db, port=CDev02dbMaster.port, charset='utf8')
        return CDev02MasterDbconn

    # SELECT
    def getGameInfo (self, nGameSeq):
        try:
            # 필수 항목이 존재하는지 체크
            if not nGameSeq:
                raise Exception('필수 데이터가 비어있습니다.')
            
            with self.DBconn() as CDev02MasterDbconn:

                CDev02MasterCursor = CDev02MasterDbconn.cursor(pymysql.cursors.DictCursor)
                if (CDev02MasterDbconn.open != True):
                    raise Exception('서비스 상태를 확인해주세요.')
                
                qryGameInfo = "SELECT * FROM ib_dev02_01.sudoku_play_log_2021 WHERE seq= %s"
                print(qryGameInfo)
                rstGameInfo = CDev02MasterCursor.execute(qryGameInfo, nGameSeq)
                if rstGameInfo  == -1:
                    raise Exception('해당 항목에 대한 결과를 찾지 못하였습니다.')
                rgResult = CDev02MasterCursor.fetchall()

                #JSON 형식으로 변환하여 출력
                strResult = json.dumps(rgResult, ensure_ascii = False)
            return strResult
        except Exception as e:
            return str(e)

    def board_init(self):
        seq_diag = [0,4,8]
        for offset in range(0,9,3):
            seq = [i for i in range(1,10)]
            random.shuffle(seq)
            for idx in range(0,9):
                i, j = idx//3, idx%3
                self.row[offset+i][seq[idx]] = 1
                self.col[offset+j][seq[idx]] = 1
                k = seq_diag[offset//3]
                self.diag[k][seq[idx]] = 1
                self.origin_board[offset+i][offset+j] = seq[idx]

    def make(self, k):
        global terminate_flag, board

        if self.terminate_flag == True:
            return True

        if k > 80:
            for i in range(0,9):
                for j in range(0,9):
                    self.board[i][j] = self.origin_board[i][j]

            terminate_flag = True
            return True

        i, j = k//9, k%9
        start_num = random.randint(1,9)

        if self.origin_board[i][j] != 0:
            self.make(k+1)

        for m in range(1,10):
            d = (i//3)*3 + (j//3)

            if self.row[i][m] == 0 and self.col[j][m] == 0 and self.diag[d][m] == 0:
                self.row[i][m], self.col[j][m], self.diag[d][m] = 1, 1, 1
                self.origin_board[i][j] = m
                self.make(k+1)
                self.row[i][m], self.col[j][m], self.diag[d][m] = 0, 0, 0
                self.origin_board[i][j] = 0

    def make_sudoku(self):
        self.board_init()
        self.make(0)
        ready_board = [self.board[i] for i in range(0,9)]

        return ready_board
