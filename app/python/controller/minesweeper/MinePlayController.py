import sys, os, datetime, pymysql, json, random
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from config import ib_config as cfg
from config import ib_function as fn

# init classes
Cvalidate = fn.CValidate()
CFilePath = cfg.CFilepathInfo()
CDev02dbMaster = cfg.CDev02dbMaster()

# init variables
strLogAlias = "MazePlayController"
dtToday = datetime.datetime.now()
strProcessRunTime = "".join([dtToday.strftime('%Y%m%d'), '_', dtToday.strftime('%H')])
strSysLogFileName = "".join([strProcessRunTime, '_', CFilePath.alias, '_', strLogAlias, '.log'])
CibLogSys = fn.CibLog(CFilePath.python_syslog, str(strSysLogFileName), strLogAlias)

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

class MinePlayController:

	# reconnect databases
	def DBconn(self):
		CDev02MasterDbconn = pymysql.connect(host=CDev02dbMaster.host, user=CDev02dbMaster.user, password=CDev02dbMaster.password, db=CDev02dbMaster.db, port=CDev02dbMaster.port, charset='utf8')
		return CDev02MasterDbconn
	
	def setMine(self, nRow, nColumn):
		try:
			if not nRow or not nColumn:
				raise Exception ('구성에 필요한 값이 없습니다. 관리자에게 문의하세요')
			# nRow = 20
			# nColumn = 20
			if not(nRow > 0 and nColumn <= 100):
				raise Exception("Row > 0, Column <= 100")
			mn = [[random.choice(['.','.','.','.','*']) for x in range(nRow)] for y in range(nColumn)]
			# for y in mn:
			#     print(y)
			r = mn.copy()
			for y, yd in enumerate(r): # index와 요소 동시 접근 루프
				for x, xd in enumerate(yd):
					if r[y][x] == '*': continue
					count = 0        
					c = [[''] if y-1 < 0 else r[y-1][0 if x-1 < 0 else x-1:x+2], # 리스트 슬라이싱 : 마지막 요소는 포함되지 않으므로 x+2
					r[y][0 if x-1 < 0 else x-1:x+2],             
					[''] if y+1 >= nColumn else r[y+1][0 if x-1 < 0 else x-1:x+2]]
        
						# [o, o, o]
        				# [o, x, o]
        				# [o, o, o]
        				# x 를 기점으로 상,하,좌,우 요소를 가져온다.        
					for z in c:
						count += z.count('*') ## 총 지뢰 갯수를 체크한다.
						r[y][x] = str(count)

			strResult = json.dumps(r, ensure_ascii = False)

			return strResult  

		except Exception as e:
			CibLogSys.error(e)
			return str(e)

		finally:
			del(nRow, nColumn)
			

