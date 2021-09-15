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
            self.root = "/".join(['', 'DEV02'])
            self.app = "/".join(['', 'DEV02', 'app'])
            self.python = "/".join(['', 'DEV02', 'app', 'python'])
            self.nodejs = "/".join(['', 'DEV02', 'app', 'nodejs'])
            self.database = "/".join(['', 'DEV02', 'app', 'db'])
            self.backup_syslog = "/".join(['', 'DEV02', 'app', 'python', 'syslog'])
        else:
            self.root = "/".join(['', 'home', 'dev02.01'])
            self.app = "/".join(['', 'home', 'dev02.01', 'app'])
            self.python = "/".join(['', 'home', 'dev02.01', 'app', 'python'])
            self.nodejs = "/".join(['', 'home', 'dev02.01', 'app', 'nodejs'])
            self.database = "/".join(['', 'home', 'dev02.01', 'app', 'db'])
            self.backup_syslog = "/".join(['', 'home', 'dev02.01', 'app', 'python', 'syslog'])
