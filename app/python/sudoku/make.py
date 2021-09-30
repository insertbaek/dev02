#!/usr/local/bin/python3.9
import random

origin_board = [[0 for j in range(0,9)] for i in range(0,9)]
board = [[0 for j in range(0,9)] for i in range(0,9)]

row = [[0 for j in range(0,10)] for i in range(0,10)]
col = [[0 for j in range(0,10)] for i in range(0,10)]
diag = [[0 for j in range(0,10)] for i in range(0,10)]

terminate_flag = False

def board_init():
    seq_diag = [0,4,8]
    for offset in range(0,9,3):
        seq = [i for i in range(1,10)]
        random.shuffle(seq)
        for idx in range(0,9):
            i, j = idx//3, idx%3
            row[offset+i][seq[idx]] = 1
            col[offset+j][seq[idx]] = 1
            k = seq_diag[offset//3]
            diag[k][seq[idx]] = 1
            origin_board[offset+i][offset+j] = seq[idx]

def make_sudoku(k):
    global terminate_flag, board

    if terminate_flag == True:
        return True

    if k > 80:
        for i in range(0,9):
            for j in range(0,9):
                board[i][j] = origin_board[i][j]

        terminate_flag = True
        return True

    i, j = k//9, k%9
    start_num = random.randint(1,9)

    if origin_board[i][j] != 0:
        make_sudoku(k+1)

    for m in range(1,10):
        #m = 1 + (m + start_num)%9
        d = (i//3)*3 + (j//3)
        
        if row[i][m] == 0 and col[j][m] == 0 and diag[d][m] == 0:
            row[i][m], col[j][m], diag[d][m] = 1, 1, 1
            origin_board[i][j] = m
            make_sudoku(k+1)
            row[i][m], col[j][m], diag[d][m] = 0, 0, 0
            origin_board[i][j] = 0


board_init()
make_sudoku(0)
ready_board = [board[i] for i in range(0,9)]

print(ready_board)

'''
def dfs(depth):
    if depth == blank_num:
        for v in board:
            print(' '.join(map(str, v)))
        exit(0)

    y, x = pos[depth]
    for n in range(1, 10):
        if not row_arr[y][n] and not col_arr[x][n] and not box_arr[y//3*3+x//3][n]:
            row_arr[y][n] = col_arr[x][n] = box_arr[y//3*3+x//3][n] = True
            board[y][x] = n
            dfs(depth+1)
            row_arr[y][n] = col_arr[x][n] = box_arr[y//3*3+x//3][n] = False
            board[y][x] = 0

board = [list(map(int, input().split())) for _ in range(9)]            
row_arr = [[False]*10 for _ in range(10)]
col_arr = [[False]*10 for _ in range(10)]
box_arr = [[False]*10 for _ in range(10)]

pos = []
for r in range(9):
    for c in range(9):
        if not board[r][c]:
            pos.append([r, c])
        else:
            row_arr[r][board[r][c]] = True
            col_arr[c][board[r][c]] = True
            box_arr[r//3*3+c//3][board[r][c]] = True

blank_num = len(pos)
dfs(0)            
'''