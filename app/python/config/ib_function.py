#!/usr/local/bin/python3.9
import logging, sys, subprocess
from logging import DEBUG, INFO, ERROR

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
