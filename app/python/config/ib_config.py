#!/usr/local/bin/python3.9
import socket

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
        self.alias = "dev02.01"
        if socket.gethostbyname(socket.getfqdn()) == '192.168.56.1':
            self.root = "/DEV02"
            self.app = self.root + "/app"
            self.python = self.app + "/python"
            self.nodejs = self.app + "/nodejs"
            self.database = self.app + "/db"
            self.python_syslog = self.python + "/syslog"
        else:
            self.root = "/".join(['', 'home', 'dev02.01'])
            self.app = "/".join(['', 'home', 'dev02.01', 'app'])
            self.python = "/".join(['', 'home', 'dev02.01', 'app', 'python'])
            self.nodejs = "/".join(['', 'home', 'dev02.01', 'app', 'nodejs'])
            self.database = "/".join(['', 'home', 'dev02.01', 'app', 'db'])
            self.python_syslog = "/".join(['', 'home', 'dev02.01', 'app', 'python', 'syslog'])
