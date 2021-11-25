import pymysql, datetime, inspect
from config import ib_config as cfg
from config import ib_function as fn
from pymysql.err import Error

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
    
    def dbDevRepair(self):
        self.host = str("192.168.56.14")
        self.db = str("ib_repair_db")
        self.user = str("dev_repair")
        self.password = str("IBqwe123!@#")
        self.port = int(3306)
        self.socket = str("/var/lib/mysql/mysql.sock")
        self.charset = str("utf8")
        
        return self
    
    """db 접속 정보 추가시 하단 if문 추가"""
    def DbInterface(self, strDbInterface):
        if (strDbInterface == 'dbDev02'):
            return self.dbDev02()
        elif (strDbInterface == 'dbDevRepair'):
            return self.dbDevRepair()
        else:
            return False
        

class DbConnection(CDbConnectionInfo, cfg.CFilepathInfo):
    strLogAlias = "MySQL_General_log"
    
    def __init__(self, strDbInterface):
        cfg.CFilepathInfo.__init__(self)
        config = self.DbInterface(strDbInterface)
        
        if (config == False):
            raise Error("클래스 인스턴스 정의 에러.")
        
        self.host = config.host
        self.username = config.user
        self.password = config.password
        self.port = config.port
        self.dbname = config.db
        self.charset = config.charset
        
        self.isTrans = False
        self.insertlastid = 0
        self.threadId = 0
        self.dbconn = None
        self.isDict = None
        self.isAutoCommit = False
        
        self.currentFrame = inspect.currentframe()
        self.dtToday = datetime.datetime.now()
        strProcessRunTime = "".join([self.dtToday.strftime('%Y%m%d'), '_', self.dtToday.strftime('%H')])
        strSysLogFileName = "".join([strProcessRunTime, '_', self.alias, '_', self.strLogAlias, '_', self.dbname, '.log'])
        
        self.CibLogSys = fn.CibLog(self.python_syslog, str(strSysLogFileName), self.strLogAlias)
        
    def Connection(self, isAutoCommitType = False, isDictType = True):
        try:
            if self.dbconn is None:
                if (isAutoCommitType == True):
                    self.isAutoCommit = True
                
                self.dbconn = pymysql.connect(
                    host=self.host,
                    user=self.username,
                    passwd=self.password,
                    db=self.dbname,
                    port=self.port,
                    charset=self.charset,
                    autocommit=self.isAutoCommit
                )
                
                if (isDictType == True):
                    self.isDict = pymysql.cursors.DictCursor
                
                return [True, 0]
        except pymysql.MySQLError as e:
            self.CibLogSys.info(e)
            return [False, e]

    def Execute(self, strQuery, rgColValue = None):
        try:
            if (self.dbconn.open is not True):
                raise Exception('DB Connection has been lost.')
            
            if (self.threadId == 0):
                self.threadId = self.dtToday.strftime('%Y%m%d%H%M%S.%f')

            if (self.isAutoCommit == False):
                self.isTrans = True

            self.CibLogSys.info([self.threadId, 'TQ', strQuery, rgColValue])
                    
            self.insertlastid = 0
            bColValueTypeisList = False
            rgRecords = []
            nAffectedRows = 0
            
            with self.dbconn.cursor(self.isDict) as cursor:
                strQueryText = strQuery.replace(" ", "")
                strQueryText = strQueryText[0:6]
                strQueryText = strQueryText.upper()
                
                if (strQueryText == "SELECT"):
                    cursor.execute(strQuery, rgColValue)
                    rstList = cursor.fetchall()
                    
                    for row in rstList:
                        rgRecords.append(row)
                    
                    return [True, rgRecords]
                elif (strQueryText == "INSERT" or strQueryText == "UPDATE" or strQueryText == "DELETE"):
                    if (strQueryText == "INSERT" and rgColValue is not None):
                        if (str(type(rgColValue)) == "<class 'list'>"):
                            bColValueTypeisList = True
                else:
                    raise Exception('syntax error')

                if (bColValueTypeisList == True):
                    rstList = cursor.executemany(strQuery, rgColValue)
                else:
                    rstList = cursor.execute(strQuery, rgColValue)        

                nAffectedRows = cursor.rowcount
                
                self.insertlastid = cursor.execute('SELECT LAST_INSERT_ID()')

                if (self.isAutoCommit == True):
                    self.TransactionCommit()
                
                return [True, nAffectedRows]
        except Exception as e:
            self.CibLogSys.info([self.threadId, self.currentFrame.f_back.f_lineno, e])
            self.TransactionRollback()
                
            return [False, e]
        except pymysql.MySQLError as e:
            self.CibLogSys.info([self.threadId, self.currentFrame.f_back.f_lineno, e])
            self.TransactionRollback()
                
            return [False, e]
        finally:
            del rgRecords, rstList, nAffectedRows, bColValueTypeisList, strQueryText
            cursor.close()

    def TransactionCommit(self):
        try:
            if (self.isTrans == True and self.isAutoCommit == False):
                self.dbconn.commit()
        except pymysql.MySQLError as e:
            if (self.isTrans == True and self.isAutoCommit == False):
                self.TransactionRollback()
                
            self.CibLogSys.info([self.threadId, self.currentFrame.f_back.f_lineno, e])
        finally:
            self.CibLogSys.info([self.threadId, 'TC'])
            self.isTrans = False
            self.insertlastid = 0
            self.threadId = 0
        
    def TransactionRollback(self):
        try:
            if (self.isTrans == True and self.isAutoCommit == False):
                self.dbconn.rollback()
        except pymysql.MySQLError as e:
            self.CibLogSys.info([self.threadId, self.currentFrame.f_back.f_lineno, e])
        finally:
            self.CibLogSys.info([self.threadId, 'TR'])
            self.isTrans = False
            self.insertlastid = 0
            self.threadId = 0
        
    def InsertLastId(self):
        return self.insertlastid
                
    def DisConnection(self):
        try:
            if (self.isTrans == True and self.isAutoCommit == False):
                self.CibLogSys.info([self.threadId, "TRANSACTION 이 종료되지 않아 강제로 ROLLBACK 을 진행했습니다."])
                self.TransactionRollback()
                raise Exception('TRANSACTION 이 종료되지 않아 강제로 ROLLBACK 을 진행했습니다. 프로세스를 점검해 주세요.')
                
            if self.dbconn:
                self.dbconn.close()
                self.dbconn = None
                
                return [True, 0]
        except pymysql.MySQLError as e:
            self.CibLogSys.info([self.threadId, self.currentFrame.f_back.f_lineno, e])
            return [False, e]
        except Exception as e:
            raise Error(e)
            

"""
ib_dev02_01 DB Create Schema

CREATE TABLE `last_insert_id_table` ( 
	`id` INT(11) NOT NULL AUTO_INCREMENT, 
	`col` VARCHAR(10) DEFAULT NULL, 
	PRIMARY KEY (`id`)
) ENGINE=INNODB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
"""


"""DbConnection Sample"""
"""
단일 py 테스트 시 상단 패키지 변경
import ib_config as cfg
import ib_function as fn


CdbDev02dbMaster = DbConnection('dbDev02')
if (CdbDev02dbMaster.Connection(isAutoCommitType=False, isDictType=True) == False):
    print("DB 연결에 실패하였습니다.")
    
rstList = CdbDev02dbMaster.Execute('SELECT * FROM user_id WHERE user_id=%s OR user_id=%s', ['b0071','nestopia'])
if (rstList[0] == False):
    print("데이터 조회 오류")
print("데이터 조회 결과 : ", rstList[1])

rstList = CdbDev02dbMaster.Execute("INSERT INTO last_insert_id_table SET col='insertbaek'")
if (rstList[0] == False):
    print("데이터 등록 오류")
print("데이터 등록 결과 (Affected_Rows) : ", rstList[1])

print("데이터 등록 결과 (last_insert_id) : ", CdbDev02dbMaster.InsertLastId())

rstList = CdbDev02dbMaster.Execute("UPDATE last_insert_id_table SET col='insertbaek' WHERE col='nestopia'")
if (rstList[0] == False):
    print("데이터 수정 오류")
print("데이터 수정 결과 (Affected_Rows) : ", rstList[1])

rstList = CdbDev02dbMaster.Execute("INSERT INTO last_insert_id_table (col) VALUES (%s)", [('star1'),('star2')])
if (rstList[0] == False):
    print("데이터 등록 오류")
print("데이터 등록 결과 (Affected_Rows) : ", rstList[1])

print("데이터 등록 결과 (last_insert_id) : ", CdbDev02dbMaster.InsertLastId())

#CdbDev02dbMaster.TransactionCommit()
#CdbDev02dbMaster.TransactionRollback()

CdbDev02dbMaster.DisConnection()
"""