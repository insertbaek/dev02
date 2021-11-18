import pymysql, datetime
import ib_config as cfg
import ib_function as fn

class CDbConnectionInfo:
    def __init__(self):
        self.host = None
        self.db = None
        self.user = None
        self.password = None
        self.prot = None
        self.socket = None
        
    def dbDev02(self):
        self.host = str("192.168.56.14")
        self.db = str("ib_dev02_01")
        self.user = str("dev02")
        self.password = str("IBqwe123!@#")
        self.port = int(3306)
        self.socket = str("/var/lib/mysql/mysql.sock")
        self.charset = str("utf8")
        
        return self
    
    """db 접속 정보 추가시 하단 if문 추가"""
    def DbInterface(self, strDbInterface):
        if(strDbInterface == 'dbDev02'):
            return self.dbDev02()
        

class DbConnection(CDbConnectionInfo, cfg.CFilepathInfo):
    strLogAlias = "MySQL_General_log"
    
    def __init__(self, strDbInterface):
        cfg.CFilepathInfo.__init__(self)
        config = self.DbInterface(strDbInterface)
        
        self.host = config.host
        self.username = config.user
        self.password = config.password
        self.port = config.port
        self.dbname = config.db
        self.charset = config.charset
        self.dbconn = None
        
        dtToday = datetime.datetime.now()
        strProcessRunTime = "".join([dtToday.strftime('%Y%m%d'), '_', dtToday.strftime('%H')])
        strSysLogFileName = "".join([strProcessRunTime, '_', self.alias, '_', self.strLogAlias, '_', self.dbname, '.log'])
        
        self.CibLogSys = fn.CibLog(self.python_syslog, str(strSysLogFileName), self.strLogAlias)
        
    def Connection(self):
        try:
            if self.dbconn is None:
                self.dbconn = pymysql.connect(
                    host=self.host,
                    user=self.username,
                    passwd=self.password,
                    db=self.dbname,
                    port=self.port,
                    charset=self.charset
                )
                
                return [True, 0]
        except pymysql.MySQLError as e:
            self.CibLogSys.info(e)
            return [False, e]

    def Execute(self, strQuery):
        try:
            self.CibLogSys.info(strQuery)
            
            with self.dbconn.cursor() as cur:
                if 'SELECT' in strQuery:
                    rgRecords = []
                    cur.execute(strQuery)
                    rstList = cur.fetchall()
                    
                    for row in rstList:
                        rgRecords.append(row)
                    cur.close()
                    
                    return [True, rgRecords]
                
                rstList = cur.execute(strQuery)
                self.dbconn.commit()
                affected = cur.rowcount
                cur.close()
                
                return [True, affected]
        except pymysql.MySQLError as e:
            self.CibLogSys.info(e)
            return [False, e]
        
    def InsertLastId(self):
        return self.Execute('SELECT LAST_INSERT_ID()')
                
    def DisConnection(self):
        try:
            if self.dbconn:
                self.dbconn.close()
                self.dbconn = None
                
                return [True, 0]
        except pymysql.MySQLError as e:
            self.CibLogSys.info(e)
            return [False, e]


"""DbConnection Sample"""
CdbDev02dbMaster = DbConnection('dbDev02')
if (CdbDev02dbMaster.Connection() == False):
    print("DB 연결에 실패하였습니다.")
    
rstList = CdbDev02dbMaster.Execute('SELECT * from user_id')
if (rstList[0] == False):
    print("데이터 조회 오류")
print("데이터 조회 결과 : ", rstList[1])

rstList = CdbDev02dbMaster.Execute("INSERT INTO last_insert_id_table set col='insertbaek'")
if (rstList[0] == False):
    print("데이터 등록 오류")
print("데이터 등록 결과 (Affected_Rows) : ", rstList[1])

rstList = CdbDev02dbMaster.InsertLastId()
if (rstList[0] == False):
    print("데이터 등록 오류")
print("데이터 등록 결과 (last_insert_id) : ", rstList[1])

CdbDev02dbMaster.DisConnection()