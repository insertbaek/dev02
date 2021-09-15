#!/usr/local/bin/python3.9
class CDev02dbMaster:
    def __init__(self):
        self.host = str("192.168.56.14")
        self.db = str("ib_dev02_01")
        self.user = str("dev02")
        self.password = str("IBqwe123!@#")
        self.port = int(3306)
        self.socket = str("/var/lib/mysql/mysql.sock")

class CFilepathInfo:
    def __init__(self):
        self.alias = "@dev02.01"
        self.root = str('/') + "/".join(['home', 'dev02.01'])
        self.app = str('/') + "/".join(['home', 'dev02.01', 'app'])
        self.python = str('/') + "/".join(['home', 'dev02.01', 'app', 'python'])
        self.nodejs = str('/') + "/".join(['home', 'dev02.01', 'app', 'nodejs'])
        self.database = str('/') + "/".join(['home', 'dev02.01', 'app', 'db'])
        self.backup_syslog = str('/') + "/".join(['home', 'dev02.01', 'app', 'python', 'syslog'])