import sys, os, traceback
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

class PythonRoute:

    def __init__(self, strCategory, fnFunction, rgValue):

        self.strCategory = strCategory
        self.fnFunction = fnFunction
        self.rgValue = rgValue

        # INIT Check ex) Maze fnGetGameInfo 1 (테스트시 주석 살리기)
        # print("INIT Check : "+self.strCategory,self.fnFunction,self.rgValue)

        if(self.strCategory=='Maze'):
            self.fnMazeRouting(self.fnFunction,self.rgValue)
        elif(self.strCategory=='Sudoku'):
            self.fnSudokuRouting(self.fnFunction,self.rgValue)
        elif(self.strCategory=='Mine'):
            self.fnMineRouting(self.fnFunction,self.rgValue)
        else:
            print("Can't Find Catagory")

        # Maze Routing ex) fnGetGameInfo/1
    def fnMazeRouting(self,function,value):
        try:
            import controller.maze.MazePlayController as MazeController
            controller = MazeController.MazePlayControll
            


            if (function == 'fnGetGameInfo'):
                controller.fnGetGameInfo(self,value)
            elif(function == 'fnSetResult'):
                controller.fnSetResult(self,value)
            elif(function == 'fnSetMaze'):
                print("ok~")
                Maze_controller=MazeController.MazeMakeControll(5,5)
                print(Maze_controller)
                # Maze_controller.getData(self)
            else:
             print("Can't Find Function")
        except Exception as e:
            print(e)
            print(traceback.format_exc())

        # Sudoku Routing ex) fnSetSudoku/1
    def fnSudokuRouting(self,function,value):
        try:
            import controller.sudoku.SudokuPlayController as SudokuController
            controller = SudokuController

            if (function == 'fnSetSudoku'):
                bHint = False
                if value[0] is "1":
                    bHint = True

                CSudoku = controller.SudokuPlayController(bHint)
                CSudoku.fnPlaySudoku()
            else:
             print("Can't Find Function")
        except Exception as e:
            print(e)

    def fnMineRouting(self,function,value):
        try:
            import controller.minesweeper.MinePlayController as MineController
            controller = MineController.MinePlayController

            if (function == ''):
                controller.getGameInfo(value)
            else:
             print("Can't Find Function")

        except Exception as e:
            print(e)

if __name__ == "__main__":
        print(sys.argv)
        # js route를 통해 넘어오는 데이터 (sys.argv)
        # Maze   ['/DEV02/app/python/route/route.py', 'Maze,fnGetGameInfo,1,1']
        # Sudoku ['/DEV02/app/python/route/route.py', 'Sudoku,fnSetSudoku,1']
        rgValues=sys.argv[1].split(',')

        #rgValue[2] ~ rgValue[..]은 해당 펑션에 들어가는 인자값임으로 하나로 합쳐서 전송해준다.
        objParameter = ''

        if len(rgValues) > 2:
            for i in range(2,len(rgValues),1):
                objParameter +=rgValues[i]+","
            objParameter = objParameter[:-1]
            objParameter=objParameter.split(',')
        print(rgValues)
        PythonRoute(rgValues[0],rgValues[1],objParameter)
        

    