'''
 @title	 미로게임 게임부분 컨트롤러 테스트
 @author 오진솔
 @date	 2021-10-06
 @update
 @description
'''
import sys, os, datetime, json, math
from random import randint
import numpy as np
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from config import ib_config as cfg
from config import ib_function as fn
from config import ib_dbconnection as dbc

# init classes
CFilePath = cfg.CFilepathInfo()

# init variables
strLogAlias = "MazePlayController"
dtToday = datetime.datetime.now()
strProcessRunTime = "".join([dtToday.strftime('%Y%m%d'), '_', dtToday.strftime('%H')])
strSysLogFileName = "".join([strProcessRunTime, '_', CFilePath.alias, '_', strLogAlias, '.log'])
CibLogSys = fn.CibLog(CFilePath.python_syslog, str(strSysLogFileName), strLogAlias)

class MazePlayControll:

    def __init__(self):
        pass

    def fnListCheck(self, objValue):
        if not objValue:
            return str('필수 데이터가 비어있습니다.')
        if not str(type(objValue)) == "<class 'list'>":
            return str('올바른 데이터 형식이 아닙니다.')
        return True
    
    # SELECT
    def fnGetGameInfo (self, rgGameInfo):    
        try:
            # 필수 항목이 존재하는지 체크
            if not rgGameInfo:
                raise Exception('필수 데이터가 비어있습니다.')
            if not str(type(rgGameInfo)) == "<class 'list'>":
                raise Exception('올바른 데이터 형식이 아닙니다.')

            CDev02MasterDbconn = dbc.DbConnection('dbDev02')
            if (CDev02MasterDbconn.Connection(isAutoCommitType=True, isDictType=True) == False):
                raise Exception('DB 연결에 실패하였습니다.')

            rstList = CDev02MasterDbconn.Execute('SELECT * FROM ib_dev02_01.maze_play_log_2021 WHERE seq= %s', rgGameInfo[0])
            if (rstList[0] == False):
                raise Exception('해당 항목에 대한 결과를 찾지 못하였습니다.')
            
            #JSON 형식으로 변환하여 출력
            strResult = json.dumps(rstList[1], ensure_ascii = False, default=str)
            print(strResult)

            return True
        except Exception as e:
            CibLogSys.error(e)
            return print(e)
        finally :
            if ('CDev02MasterDbconn' in locals()):
                CDev02MasterDbconn.DisConnection()

    # INSERT
    def fnSetGame (self, rgGameInfo):
        try:
            # 필수 항목이 존재하는지 체크
            if not rgGameInfo:
                raise Exception('필수 데이터가 비어있습니다.')
            if not str(type(rgGameInfo)) == "<class 'list'>":
                raise Exception('올바른 데이터 형식이 아닙니다.')

            CDev02MasterDbconn = dbc.DbConnection('dbDev02')
            if (CDev02MasterDbconn.Connection(isAutoCommitType=False, isDictType=True) == False):
                raise Exception('DB 연결에 실패하였습니다.')

            rstGameInfo = CDev02MasterDbconn.Execute("INSERT INTO ib_dev02_01.test_tbl_1 SET data1 = %(data1)s, data2 = %(data2)s", rgGameInfo)
            if (rstGameInfo[0] == False):
                raise Exception('해당 항목에 대한 결과를 찾지 못하였습니다.')
            
            CDev02MasterDbconn.TransactionCommit()
            print (CDev02MasterDbconn.InsertLastId())

            return True
        except Exception as e:
            CibLogSys.error(e)
            return print(e)
        finally :
            if ('CDev02MasterDbconn' in locals()):
                CDev02MasterDbconn.DisConnection()

    # UPDATE
    def fnSetResult (self, rgGameInfo):
        try:
            # 필수 항목이 존재하는지 체크
            if not rgGameInfo:
                raise Exception('필수 데이터가 비어있습니다.')
            if not str(type(rgGameInfo)) == "<class 'list'>":
                raise Exception('올바른 데이터 형식이 아닙니다.')

            CDev02MasterDbconn = dbc.DbConnection('dbDev02')
            if (CDev02MasterDbconn.Connection(isAutoCommitType=False, isDictType=True) == False):
                raise Exception('DB 연결에 실패하였습니다.')

            rstGameInfo = CDev02MasterDbconn.Execute("UPDATE ib_dev02_01.maze_play_log_2021 SET winner = %s, loser = %s, end_time = now() WHERE seq = %s", rgGameInfo)
            if (rstGameInfo[0] == False):
                raise Exception('해당 항목에 대한 결과를 찾지 못하였습니다.')

            CDev02MasterDbconn.TransactionCommit()
            
            return True
        except Exception as e:
            CibLogSys.error(e)
            return print(e)
        finally :
            if ('CDev02MasterDbconn' in locals()):
                CDev02MasterDbconn.DisConnection()

    # DELETE
    def fnSetDelGame (self, rgGameInfo):
        try:
            # 필수 항목이 존재하는지 체크
            if not rgGameInfo:
                raise Exception('필수 데이터가 비어있습니다.')
            if not str(type(rgGameInfo)) == "<class 'list'>":
                raise Exception('올바른 데이터 형식이 아닙니다.')

            CDev02MasterDbconn = dbc.DbConnection('dbDev02')
            if (CDev02MasterDbconn.Connection(isAutoCommitType=False, isDictType=True) == False):
                raise Exception('DB 연결에 실패하였습니다.')

            rstGameInfo = CDev02MasterDbconn.Execute("DELETE FROM ib_dev02_01.maze_play_log_2021 WHERE seq = %s", rgGameInfo[0])
            if (rstGameInfo[0] == False):
                raise Exception('해당 항목에 대한 결과를 찾지 못하였습니다.')
            
            CDev02MasterDbconn.TransactionCommit()

            return True
        except Exception as e:
            CibLogSys.error(e)
            return print(e)
        finally :
            if ('CDev02MasterDbconn' in locals()):
                CDev02MasterDbconn.DisConnection()


class MazeMakeControll:

    # def __init__(self, nStartX, nStartY, nEndX, nEndY, nMazeX, nMazeY, nLevel):

    #     print(nStartX, nStartY, nEndX, nEndY, nMazeX, nMazeY, nLevel)

    #     self.rgStart = [nStartX,nStartY]
    #     self.rgEnd = [nEndX,nEndY]
    #     self.nMazeX = nMazeX
    #     self.nMazeY = nMazeY
    #     self.nLevel = nLevel

    #     rstCreat_map = self.creat_map(self, self.rgStart, self.rgEnd, self.nMazeX, self.nMazeY, self.nLevel)

    #     print(rstCreat_map)

    def __init__(self):
        pass

    def fnCreateMap(self, rgGameInfo):

        # 지정된 순서 규약
        start_node=[rgGameInfo[0],rgGameInfo[1]]
        end_node=[rgGameInfo[2],rgGameInfo[3]]
        mazeX=rgGameInfo[4]
        mazeY=rgGameInfo[5]
        sparsity=rgGameInfo[6]

        nSizeX = mazeX
        nSizeY = mazeY
        maxWall = 13
        rgMaze = (nSizeX*nSizeY)*[0]

        for i in range(0,nSizeX,sparsity):
            for j in range(0,nSizeY,sparsity):

                rgMaze[(j*nSizeX)+i]=2

        for i in range(0,nSizeX):
            rgMaze[i]=1
            rgMaze[(nSizeX*(nSizeY-1))+i] = 1
        for i in range(1,nSizeY-1):
            rgMaze[nSizeX*i]=1
            rgMaze[(nSizeX*i)+(nSizeX-1)] = 1

        while 2 in rgMaze:
            x = randint(1,(nSizeX-1)/2)*2
            y = randint(1,(nSizeY-1)/2)*2
            c = rgMaze[(y*nSizeX)+x]

            if c == 2:
                mwc = 0
                r = randint(0,3)
                if r == 0:
                    while c != 1:
                        rgMaze[(y*nSizeX)+x] = 1
                        y -= 1
                        c = rgMaze[(y*nSizeX)+x]
                        mwc += 1
                        if mwc == maxWall: break
                if r == 1:
                    while c != 1:
                        rgMaze[(y*nSizeX)+x] = 1
                        x += 1
                        c = rgMaze[(y*nSizeX)+x]
                        mwc += 1
                        if mwc == maxWall: break
                if r == 2:
                    while c != 1:
                        rgMaze[(y*nSizeX)+x] = 1
                        y += 1
                        c = rgMaze[(y*nSizeX)+x]
                        mwc += 1
                        if mwc == maxWall: break
                if r == 3:
                    while c!= 1:
                        rgMaze[(y*nSizeX)+x] = 1
                        x -= 1
                        c = rgMaze[(y*nSizeX)+x]
                        mwc += 1
                        if mwc == maxWall: break

        rgMazeMap={}
        rgArrMake=np.ones((nSizeX,nSizeY))

        for i in range(0,nSizeY): 
            for j in range(0,nSizeX):
                k = rgMaze[(i*nSizeX)+j]
                if k == 1:
                    if (i==start_node[0]  and j==start_node[1]) or (j==end_node[1]and i==end_node[0]):
                        continue
                    else:
                        rgMazeMap[(i,j)]=1
                        rgArrMake[j][i]=0
        return rgMazeMap
