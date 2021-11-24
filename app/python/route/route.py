from logging import FATAL
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import controller.maze.MazePlayController as MazeController
import controller.sudoku.SudokuPlayController as SudokuController
import controller.minesweeper.MinePlayController as MineController

class PythonRoute:

        def __init__(self, strCategory, fnFunction, strJsonValue):

            self.strCategory = strCategory
            self.fnFunction = fnFunction
            self.strJsonValue = strJsonValue

            # INIT Check ex) Maze fnGetGameInfo 1 (테스트시 주석 살리기)
            print("INIT Check : "+self.strCategory,self.fnFunction,self.strJsonValue)

            self.fnRouting()

        def fnRouting(self):

            if(self.strCategory=='Maze'):
                self.fnMazeRouting(self.fnFunction,self.strJsonValue)

            elif(self.strCategory=='Sudoku'):
                self.fnSudokuRouting(self.fnFunction,self.strJsonValue)

            elif(self.strCategory=='Mine'):
                self.fnMineRouting(self.fnFunction,self.strJsonValue)
            
            else:
                print("Can't Find Catagory")
           
            # Maze Routing ex) fnGetGameInfo/1
        def fnMazeRouting(self,function,value):

            print(function+"{}"+value)

            controller = MazeController.MazePlayController

            if (function == 'fnGetGameInfo'):
                controller.fnGetGameInfo(value)
            elif(function == 'fnSetResult'):
                controller.setResult(value)

            # Sudoku Routing ex) fnSetSudoku/1
        def fnSudokuRouting(self,function,value):

            controller = SudokuController

            if (function == 'fnSetSudoku'):
                bHint = False

                if value is "1":
                    bHint = True

                CSudoku = controller.SudokuPlayController(bHint)
                CSudoku.fnPlaySudoku()

        def fnMineRouting(self,function,value):        
            controller = MineController.MinePlayController

            if (function == ''):
                controller.getGameInfo(value)

if __name__ == "__main__":
        # js route를 통해 넘어오는 데이터 (sys.argv)
        # Maze   ['/DEV02/app/python/route/route.py', 'Maze,fnGetGameInfo,1,1']
        # Sudoku ['/DEV02/app/python/route/route.py', 'Sudoku,fnSetSudoku,1,1']
        rgValues=sys.argv[1].split(',')

        #rgValue[2] ~ rgValue[..]은 해당 펑션에 들어가는 인자값임으로 하나로 합쳐서 전송해준다.
        strParameter =''

        if len(rgValues) > 2:
            for i in range(2,len(rgValues),1):
                strParameter +=rgValues[i]+","
            strParameter = strParameter[:-1]
            
        PythonRoute(rgValues[0],rgValues[1],strParameter)
        

    