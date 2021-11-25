'''
 @title	 스도쿠 게임부분 컨트롤러 테스트
 @author 오진솔
 @date	 2021-10-06
 @update
 @description
'''

import sys, os, datetime, json, random
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from config import ib_config as cfg
from config import ib_function as fn
from config import ib_dbconnection as dbc

class SudokuPlayController(fn.CValidate, cfg.CFilepathInfo):
    strLogAlias = "SudokuPlayController"
    
    def __init__(self, bSudokuHintType):
        cfg.CFilepathInfo.__init__(self)
        
        self.bSudokuHintType = bSudokuHintType
        
        dtToday = datetime.datetime.now()
        strProcessRunTime = "".join([dtToday.strftime('%Y%m%d'), '_', dtToday.strftime('%H')])
        strSysLogFileName = "".join([strProcessRunTime, '_', self.alias, '_', self.strLogAlias, '.log'])

        self.CibLogSys = fn.CibLog(self.python_syslog, str(strSysLogFileName), self.strLogAlias)

        try:
            for oConfig in [cfg.CFilepathInfo()]:
                bResult = self.isDictEmpty(oConfig.__dict__)
                
                if not bResult:
                    raise Exception(self.getDictEmpty())
        except Exception as e:
            print('환경설정 중 "' + str(e) + '" 항목 정의가 올바르지 않습니다.')
            sys.exit()
        finally:
            del oConfig, bResult
        
        '''
        # rgAreaRuleBoard   |  # rgStraightRuleBoard
        [                   |  [
            [0, 0, 0, 0],   |      [0, 0, 0, 0],
            [0, 0, 0, 0],   |      [0, 0, 0, 0],
            [0, 0, 0, 0],   |      [0, 0, 0, 0],
            [0, 0, 0, 0]    |      [0, 0, 0, 0]
        ]                   |  ]
        '''
        self.rgAreaRuleBoard = [[0 for j in range(0,9)] for i in range(0,9)]
        self.rgStraightRuleBoard = [[0 for j in range(0,9)] for i in range(0,9)]

        '''
        # rgRuleBaseRow       |  # rgRuleBaseCol       |  # rgRuleBaseDiag
        [                     |  [                     |  [
            [0, 0, 0, 0, 0],  |      [0, 0, 0, 0, 0],  |      [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],  |      [0, 0, 0, 0, 0],  |      [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],  |      [0, 0, 0, 0, 0],  |      [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]   |      [0, 0, 0, 0, 0]   |      [0, 0, 0, 0, 0],
        ]                     |  ]                     |  ]
        '''        
        self.rgRuleBaseRow = [[0 for j in range(0,10)] for i in range(0,10)]
        self.rgRuleBaseCol = [[0 for j in range(0,10)] for i in range(0,10)]
        self.rgRuleBaseDiag = [[0 for j in range(0,10)] for i in range(0,10)]
        self.bTerminate = False

        rgDiagSeq = [0,4,8]
        for nOffset in range(0,9,3): # nOffset : 0 or 2
            rgVariable = [i for i in range(1,10)] # rgVariable = [1,2,3,4]
            random.shuffle(rgVariable)

            for nIndex in range(0,9): # nIndex = 0 or 1 or 2 or 3
                nRowValue = nIndex // 3 # i = 0 or 0 or 1 or 1
                nColValue = nIndex % 3 # j = 0 or 1 or 0 or 1
                nOffsetValue = nOffset // 3 # a = 0 or 1
                nDiagValue = rgDiagSeq[nOffsetValue] # k = 0 or 3
                
                '''
                # loop 1                | # loop 2
                rgRuleBaseRow[0][1] = 1 | rgRuleBaseRow[2][1] = 1
                rgRuleBaseRow[0][2] = 1 | rgRuleBaseRow[2][2] = 1
                rgRuleBaseRow[1][3] = 1 | rgRuleBaseRow[3][3] = 1
                rgRuleBaseRow[1][4] = 1 | rgRuleBaseRow[3][4] = 1
                '''
                self.rgRuleBaseRow[nOffset + nRowValue][rgVariable[nIndex]] = 1
                #print(nOffset + nRowValue, rgVariable[nIndex])

                '''
                # loop 1                | # loop 2
                rgRuleBaseCol[0][1] = 1 | rgRuleBaseCol[2][1] = 1
                rgRuleBaseCol[1][2] = 1 | rgRuleBaseCol[3][2] = 1
                rgRuleBaseCol[0][3] = 1 | rgRuleBaseCol[2][3] = 1
                rgRuleBaseCol[1][4] = 1 | rgRuleBaseCol[3][4] = 1
                '''
                self.rgRuleBaseCol[nOffset + nColValue][rgVariable[nIndex]] = 1
                #print(nOffset + nColValue, rgVariable[nIndex])

                '''
                # loop 1                 | loop 2
                rgRuleBaseDiag[0][1] = 1 | rgRuleBaseDiag[3][1] = 1
                rgRuleBaseDiag[0][2] = 1 | rgRuleBaseDiag[3][2] = 1
                rgRuleBaseDiag[0][3] = 1 | rgRuleBaseDiag[3][3] = 1
                rgRuleBaseDiag[0][4] = 1 | rgRuleBaseDiag[3][4] = 1
                '''
                self.rgRuleBaseDiag[nDiagValue][rgVariable[nIndex]] = 1
                #print(nDiagValue, rgVariable[nIndex])

                '''
                # loop 1                  | # loop 2
                rgAreaRuleBoard[0][0] = 1 | rgAreaRuleBoard[2][2] = 1
                rgAreaRuleBoard[0][1] = 2 | rgAreaRuleBoard[2][3] = 2
                rgAreaRuleBoard[1][0] = 3 | rgAreaRuleBoard[3][2] = 3
                rgAreaRuleBoard[1][1] = 4 | rgAreaRuleBoard[3][3] = 4
                '''
                self.rgAreaRuleBoard[nOffset + nRowValue][nOffset + nColValue] = rgVariable[nIndex]

    # SELECT
    def getGameInfo(self, nGameSeq):
        try:
            # 필수 항목이 존재하는지 체크
            if not nGameSeq:
                raise Exception('필수 데이터가 비어있습니다.')
            
            CdbDev02dbMaster = dbc.DbConnection('dbDev02')
            if (CdbDev02dbMaster.Connection(isAutoCommitType=True, isDictType=True) == False):
                raise Exception('DB 연결에 실패하였습니다.')
                
            rstList = CdbDev02dbMaster.Execute('SELECT * FROM ib_dev02_01.sudoku_play_log_2021 WHERE seq=%s', [nGameSeq])
            if (rstList[0] == False):
                raise Exception('해당 항목에 대한 결과를 찾지 못하였습니다.')
            
            CdbDev02dbMaster.DisConnection()
            
            #JSON 형식으로 변환하여 출력
            strResult = json.dumps(rstList[1], ensure_ascii = False)

            return strResult
        except Exception as e:
            self.CibLogSys.error(e)
            return str(e)

    def fnMakeSudoku(self, nLastPrevious):
        if self.bTerminate == True:
            return True

        if nLastPrevious > 80:
            for i in range(0,9):
                for j in range(0,9):
                    self.rgStraightRuleBoard[i][j] = self.rgAreaRuleBoard[i][j]

            self.bTerminate = True
            return True

        # 2차원 배열의 rgRuleBaseCol과 rgRuleBaseRow를 찾기위한 포인트
        nCol, nRow = nLastPrevious // 9, nLastPrevious % 9
        nStartNumber = random.randint(1,9)
        #print("nLastPrevious : " + str(nLastPrevious), ", nCol : " + str(nCol), ", nRow : " + str(nRow), ", nStart : " + str(nStart))
        #print(rgAreaRuleBoard[nCol][nRow])
        
        # rgAreaRuleBoard의 배열값이 0인것을 채워야 한다.
        if self.rgAreaRuleBoard[nCol][nRow] != 0:
            #print("OUT 1 : " + str(nLastPrevious))
            self.fnMakeSudoku(nLastPrevious + 1)

        for nCheckNumber in range(1,10): # m = 1 or 2 or 3 or 4
            nCheckNumber = 1 + (nCheckNumber + nStartNumber) % 9 # m = 1 or 2 or 3 or 4
            nDepthNumber = (nCol // 3) * 3 + (nRow // 3)
            #print("nCheckNumber : " + str(nCheckNumber), ", nDepthNumber : " + str(nDepthNumber))
            #print("["+str(nRow)+"]["+str(nCheckNumber)+"]", "["+str(nCol)+"]["+str(nCheckNumber)+"]", "["+str(nDepthNumber)+"]["+str(nCheckNumber)+"]", rgRuleBaseCol[nRow][nCheckNumber], rgRuleBaseRow[nCol][nCheckNumber], rgRuleBaseDiag[nDepthNumber][nCheckNumber])

            if self.rgRuleBaseCol[nRow][nCheckNumber] == 0 and self.rgRuleBaseRow[nCol][nCheckNumber] == 0 and self.rgRuleBaseDiag[nDepthNumber][nCheckNumber] == 0:
                self.rgRuleBaseRow[nCol][nCheckNumber], self.rgRuleBaseCol[nRow][nCheckNumber], self.rgRuleBaseDiag[nDepthNumber][nCheckNumber] = 1, 1, 1
                self.rgAreaRuleBoard[nCol][nRow] = nCheckNumber
                #print(rgAreaRuleBoard)
                #print("OUT 2 : " + str(nLastPrevious))
                self.fnMakeSudoku(nLastPrevious + 1)
                #print("OUT 2 : ?")
                self.rgRuleBaseRow[nCol][nCheckNumber], self.rgRuleBaseCol[nRow][nCheckNumber], self.rgRuleBaseDiag[nDepthNumber][nCheckNumber] = 0, 0, 0
                self.rgAreaRuleBoard[nCol][nRow] = 0

        #print(rgAreaRuleBoard)
        #print("fnMakeSudoku : nLastPrevious => " + str(nLastPrevious), ", nCol => " + str(nCol), ", nRow => " + str(nRow), ", nStart => " + str(nStart))

    def fnHintArrowInit(self):
        self.fnMakeSudoku(0)

        rgBoardInit = [self.rgStraightRuleBoard[i] for i in range(0,9)]

        rgHint = []
        for x in range(0,len(rgBoardInit)-1):
            for y in range(0,len(rgBoardInit)-1):
                rgBoard = [rgBoardInit[x][y], rgBoardInit[x][y+1], rgBoardInit[x+1][y], rgBoardInit[x+1][y+1]]
                rgHint.append(rgBoard.index(max(rgBoard)))

        if self.bSudokuHintType == True:
            rgReturn = [[rgBoardInit], [rgHint]]
        else:
            rgReturn = [[rgBoardInit], [0]]

        return rgReturn

    def fnPlaySudoku(self):
        rgBoard = self.fnHintArrowInit()
        print("sudoku", rgBoard[0])
        print("hint", rgBoard[1])
