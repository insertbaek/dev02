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
        self.root = "/".join(['home', 'dev02.01'])
        self.app = str(self.root) + "/".join(['app'])
        self.python = str(self.app) + "/".join(['python'])
        self.nodejs = str(self.app) + "/".join(['nodejs'])
        self.database = str(self.app) + "/".join(['db'])