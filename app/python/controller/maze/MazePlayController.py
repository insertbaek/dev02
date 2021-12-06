'''
 @title	 미로게임 게임부분 컨트롤러 테스트
 @author 오진솔
 @date	 2021-10-06
 @update
 @description
'''
import sys, os, datetime, json, math, random, numpy
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
    def __init__(self, width = 5, height = 5):
        print("###################")
        self.cells = []
        self.width=width
        self.height=height

        self.generateMaze(width, height)
        # self.cells = self.generateMaze(width, height)
        self.solution = []
        self.solution2 = []
        
        
        self.visited = False


    def generateMaze(self, width, height):
        generateCells = [range(width)]
        for x in range(0, width-1, 1):
            generateCells.append([range(height)])
            for y in range(0, height-1, 1):
                generateCells[x][y] = Cell(x, y)
        startX = math.floor(random.randrange(0, width-1))
        startY =  math.floor(random.randrange(0,height-1))
        print("THIS",startX,width,startY,height)
        self.cells = generateCells

        self.visit(generateCells[startX][startY])
        solution = self.solve(width - 1, height - 1, 0, 0)
        solution2 = self.solve(0, height - 1, width-1, 0)
        if solution.length == solution2.length:
            self.solution = solution
            self.solution2 = solution2
            self.cells = generateCells
            # return generateCells
        else:
            self.generateMaze(width, height)

    def getOptions(self, cell, walls):
        options = []
        
        def checkOption(x, y):
            print("################!#@#",x,y)
            if (walls):
                if ((y < cell.y and cell.walls['n']) or (x > cell.x and cell.walls['e']) or (y > cell.y and cell.walls['s']) or (x < cell.x and cell.walls['w'])):
                    print("x5-1")
                    return
            print("5-2")
            if(self.cells[x] is not None):
                print("@1//")
                if(self.cells[x][y] is not None):
                    print("@2//",x,y)
                    if(not self.cells[x][y].visited):
                        print("@3//")
                        options.append(self.cells[x][y])

            print("@4//")
            #if (self.cells[x] is not None and self.cells[x][y] is not None and not self.cells[x][y].visited):
                #options.append(self.cells[x][y])
        
        checkOption(cell.x, cell.y - 1)
        checkOption(cell.x + 1, cell.y)
        checkOption(cell.x, cell.y + 1)
        checkOption(cell.x - 1, cell.y)

        return options

    def visit(self, cell, direction = None):
        cell.visited = True
        if (direction is not None) :
            cell.walls[direction] = False
        
        cell.visited = True

        print("xVisit")
        options = self.getOptions(cell, False)
        print("xVisit1")
        print(options)

        while (len(options) > 0):
            print("xVisit2")

            index =  math.floor(random.randrange(0,1)*len(options))
            nextCell = options[index]
            print("xVisit3")
            print(nextCell.x, nextCell.y)
            if cell.y > nextCell.y:
                cell.walls['n'] = False
                self.visit(nextCell, "s")
            elif cell.x < nextCell.x:
                cell.walls['e'] = False
                self.visit(nextCell, "w")
            elif cell.y < nextCell.y:
                cell.walls['s'] = False
                self.visit(nextCell, "n")
            elif cell. x > nextCell.x:
                cell.walls['w'] = False
                self.visit(nextCell, "e")

            options = self.getOptions(cell)

    def solve(self, startX, startY, endX, endY):
        startX = startX or 0
        startY = startY or 0
        endX = endX == None and self.width - 1 or endX
        endY = endY == None and self.height - 1 or endY
        print("x6")
        print("!!!!!!!!!",self.cells)
        for x in range(0, len(self.cells), 1):
            for y in range(0, len(self.cells[x]), 1):
                self.cells[x][y].visited = False
        print("x7",self.cells[0][0].walls['n'])
        solution = []
        cell = self.cells[startX][startY]
        options = []
        print("x8")
        while ((cell.x != endX) or (cell.y != endY)):
            cell.visited = True
            options = self.getOptions(cell, True)
            print("option",options)
            if (len(options) == 0):
                print(solution)
                cell = solution.pop()
            else:
                solution.push(cell)
                cell = options[0]
        print("x9")
        solution.push(cell)

        return solution

    def getData(self):
        print(self.cells)
   
class Cell:
   def __init__(self, x, y):
       self.x: int = x
       self.y: int = y

       self.walls = {
           'n' : True,
           'e' : True,
           's' : True,
           'w' : True
       }

       self.visited = False