import sqlite3

from sqlitediff.sqlite.Command import Command
from sqlitediff.diff.DiffResult import DiffResult

class SqliteDiff():
    def __init__(self, pathBefore, pathAfter) -> None:
        self._beforeDB = sqlite3.connect(pathBefore)
        self._beforeCursor = self._beforeDB.cursor()
        self._afterDB = sqlite3.connect(pathAfter)
        self._afterCursor = self._afterDB.cursor()
        self._beforeTables = set()
        self._afterTables = set()

    def _getDeletedTables(self):
        deltaTables = self._beforeTables.difference(self._afterTables)
        return list(deltaTables)
    
    def _getCreatedTables(self):
        deltaTables = self._afterTables.difference(self._beforeTables)
        return list(deltaTables)

    def _processTables(self):
        tables = self._beforeCursor.execute(Command.TABLE_NAMES).fetchall()
        for table in tables:
            self._beforeTables.add(table[0])

        tables = self._afterCursor.execute(Command.TABLE_NAMES).fetchall()
        for table in tables:
            self._afterTables.add(table[0])

    def process(self):
        self._processTables()
        deletedTables = self._getDeletedTables()
        createdTables = self._getCreatedTables()
        result = DiffResult(deletedTables, createdTables, list(self._beforeTables), list(self._afterTables))
        return result