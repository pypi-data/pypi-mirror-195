import os
import time

from datetime import datetime

from hash_calc.HashCalc import HashCalc

class Controller():
    def __init__(self, beforePath, afterPath) -> None:
        self.startTime = time.time()
        self._beforePath = beforePath
        self._afterPath = afterPath
        self._bHash = HashCalc(self._beforePath)
        self._aHash = HashCalc(self._afterPath)

    def printHeader(self):
        print("################################################################################")
        print("")
        print("sqlitediff by 5f0")
        print("Differential analysis of sqlite files")
        print("")
        print("Current working directory: " + os.getcwd())
        print("")
        print("Sqlite file before action:")
        print("-->    Path: " + self._beforePath)
        print("-->     MD5: " + self._bHash.md5)
        print("-->  SHA256: " + self._bHash.sha256)
        print("")
        print("Sqlite file after action:")
        print("-->    Path: " + self._afterPath)
        print("-->     MD5: " + self._aHash.md5)
        print("-->  SHA256: " + self._aHash.sha256)
        print("")
        print("Datetime: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        print("")
        print("################################################################################")
        print("")

    def printExecutionTime(self):
        end = time.time()
        print("")
        print("################################################################################")
        print("")
        print("Execution Time: " + str(end-self.startTime)[0:8] + " sec")
        print("")