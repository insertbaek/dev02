import random
m = 20
n = 20
if not(n > 0 and m <= 100):
    raise Exception("N > 0, M <= 100")
mn = [[random.choice(['.','.','.','.','*']) for x in range(n)] for y in range(m)]
# for y in mn:
#     print(y)
r = mn.copy()
for y, yd in enumerate(r): # index와 요소 동시 접근 루프
    for x, xd in enumerate(yd):
        if r[y][x] == '*': continue

        count = 0        

        c = [[''] if y-1 < 0 else r[y-1][0 if x-1 < 0 else x-1:x+2], # 리스트 슬라이싱 : 마지막 요소는 포함되지 않으므로 x+2
             r[y][0 if x-1 < 0 else x-1:x+2],             
             [''] if y+1 >= m else r[y+1][0 if x-1 < 0 else x-1:x+2]]
          
        # [o, o, o]
        # [o, x, o]
        # [o, o, o]
        # x 를 기점으로 상,하,좌,우 요소를 가져온다.        

        for z in c:
            count += z.count('*') ## 총 지뢰 갯수를 체크한다.
            
        r[y][x] = str(count) ## 총 지뢰 갯수를 숫자로 넣어준다.

for y in r:
    print(''.join(y))    
