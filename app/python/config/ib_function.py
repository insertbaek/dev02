#!/usr/local/bin/python3.9
import logging, sys, subprocess
from logging import DEBUG, INFO, WARNING, ERROR, CRITICAL

class CValidate:
    def __init__(self):
        self.result = 0

    def isDictEmpty(self, rgData):
        bValue = True

        for strKey, strValue in rgData.items():
            if not strValue:
                self.setDictEmpty(strKey)
                bValue = False

        return bValue

    def setDictEmpty(self, strKey):
        self.rgKey = []
        self.rgKey.append(strKey)

    def getDictEmpty(self):
        return self.rgKey

    def isEmpty(self, rgData):
        bValue = True

        for strValue in rgData:
            if not strValue:
                bValue = False

        return bValue

class CibLog:
    def __init__(self, path, name, logname, level=INFO):
        # init construct.
        self.logname = logname
        self.level = level
        self.name = name
        self.path = path
        self.format = "[%(levelname)s] %(asctime)s : %(message)s"

        # Logger configuration.
        self.log_formatter = logging.Formatter(self.format)
        self.console_logger = logging.StreamHandler()
        self.console_logger.setFormatter(self.log_formatter)
        self.file_logger = logging.FileHandler("".join([self.path, '/', self.name]))
        self.file_logger.setFormatter(self.log_formatter)

        # Complete logging config.
        self.logger = logging.getLogger(self.logname)
        self.logger.setLevel(self.level)
        self.logger.propagate = 0
        self.logger.addHandler(self.console_logger) # Screen
        self.logger.addHandler(self.file_logger) # File

    def info(self, msg):
        self.logger.info(str(msg))

    def debug(self, msg):
        self.logger.debug(str(msg))

    def warning(self, msg):
        self.logger.warn(str(msg))

    def error(self, msg):
        self.logger.error(str(msg))

    def critical(self, msg):
        self.logger.critical(str(msg))