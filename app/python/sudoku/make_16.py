#!/usr/local/bin/python3.9
import random

'''
# origin_board    | # board
[                 | [
    [0, 0, 0, 0], |     [0, 0, 0, 0],
    [0, 0, 0, 0], |     [0, 0, 0, 0],
    [0, 0, 0, 0], |     [0, 0, 0, 0],
    [0, 0, 0, 0]  |     [0, 0, 0, 0]
]                 | ]
'''
origin_board = [[0 for j in range(0,4)] for i in range(0,4)]
board = [[0 for j in range(0,4)] for i in range(0,4)]

'''
# row                | # col                | # diag
[                    | [                    | [
    [0, 0, 0, 0, 0], |     [0, 0, 0, 0, 0], |     [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0], |     [0, 0, 0, 0, 0], |     [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0], |     [0, 0, 0, 0, 0], |     [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0]  |     [0, 0, 0, 0, 0]  |     [0, 0, 0, 0, 0],
]                    | ]                    | ]
'''
row = [[0 for j in range(0,5)] for i in range(0,5)]
col = [[0 for j in range(0,5)] for i in range(0,5)]
diag = [[0 for j in range(0,5)] for i in range(0,5)]

terminate_flag = False

def board_init():
    nIndex = 0
    seq_diag = [0,3]
    for offset in range(0,4,2): # offset : 0 or 2
        seq = [i for i in range(1,5)] # seq = [1,2,3,4]
        random.shuffle(seq)
        #print(seq)
        for idx in range(0,4): # idx = 0 or 1 or 2 or 3
            i = idx//2 # i = 0 or 0 or 1 or 1
            j = idx%2 # j = 0 or 1 or 0 or 1
            a = offset//2 # a = 0 or 1
            k = seq_diag[a] # k = 0 or 3
            
            '''
            # loop 1      | # loop 2
            row[0][1] = 1 | row[2][1] = 1
            row[0][2] = 1 | row[2][2] = 1
            row[1][3] = 1 | row[3][3] = 1
            row[1][4] = 1 | row[3][4] = 1
            '''
            row[offset+i][seq[idx]] = 1
            #print(offset+i, seq[idx])

            '''
            # loop 1      | # loop 2
            col[0][1] = 1 | col[2][1] = 1
            col[1][2] = 1 | col[3][2] = 1
            col[0][3] = 1 | col[2][3] = 1
            col[1][4] = 1 | col[3][4] = 1
            '''
            col[offset+j][seq[idx]] = 1
            #print(offset+j, seq[idx])

            '''
            # loop 1       | loop 2
            diag[0][1] = 1 | diag[3][1] = 1
            diag[0][2] = 1 | diag[3][2] = 1
            diag[0][3] = 1 | diag[3][3] = 1
            diag[0][4] = 1 | diag[3][4] = 1
            '''
            diag[k][seq[idx]] = 1
            #print(k, seq[idx])

            '''
            # loop 1               | # loop 2
            origin_board[0][0] = 1 | origin_board[2][2] = 1
            origin_board[0][1] = 2 | origin_board[2][3] = 2
            origin_board[1][0] = 3 | origin_board[3][2] = 3
            origin_board[1][1] = 4 | origin_board[3][3] = 4
            '''
            origin_board[offset+i][offset+j] = seq[idx]
            nIndex += 1
    
    #print(origin_board, col, row, diag)

def make_sudoku(k):
    global terminate_flag, board

    if terminate_flag == True:
        return True

    if k > 15:
        for i in range(0,4):
            for j in range(0,4):
                board[i][j] = origin_board[i][j]

        terminate_flag = True
        return True

    # 2차원 배열의 col과 row를 찾기위한 포인트
    i, j = k//4, k%4
    start_num = random.randint(1,4)
    #print("k : " + str(k), ", i : " + str(i), ", j : " + str(j), ", start_num : " + str(start_num))
    #print(origin_board[i][j])
    
    # origin_board의 배열값이 0인것을 채워야 한다.
    if origin_board[i][j] != 0:
        #print("OUT 1 : " + str(k))
        make_sudoku(k+1)

    for m in range(1,5): # m = 1 or 2 or 3 or 4
        #m = 1 + (m + start_num) % 4 # m = 1 or 2 or 3 or 4
        d = (i//2)*2 + (j//2)
        #print("m : " + str(m), ", d : " + str(d))
        #print("["+str(j)+"]["+str(m)+"]", "["+str(i)+"]["+str(m)+"]", "["+str(d)+"]["+str(m)+"]", col[j][m], row[i][m], diag[d][m])

        if col[j][m] == 0 and row[i][m] == 0 and diag[d][m] == 0:
            row[i][m], col[j][m], diag[d][m] = 1, 1, 1
            origin_board[i][j] = m
            #print(origin_board)
            #print("OUT 2 : " + str(k))
            make_sudoku(k+1)
            #print("OUT 2 : ?")
            row[i][m], col[j][m], diag[d][m] = 0, 0, 0
            origin_board[i][j] = 0

    #print(origin_board)
    #print("make_sudoku : k => " + str(k), ", i => " + str(i), ", j => " + str(j), ", start_num => " + str(start_num))
    

board_init()
make_sudoku(0)

ready_board = [board[i] for i in range(0,4)]

print(ready_board)    

