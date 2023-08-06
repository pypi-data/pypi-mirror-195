import sqlite3

from sqlitediff.sqlite.Command import Command
from sqlitediff.model.Table import Table

class Snapshot():
    def __init__(self, name, path, id) -> None:
        self.id = id
        self.name = name
        self.tables = []
        self.dbHandle = sqlite3.connect(path)
        self.dbCursor = self.dbHandle.cursor()
        self._processTables()
        
    def _processTables(self):
        tables = self.dbCursor.execute(Command.TABLE_NAMES).fetchall()
        for table in tables:
            self._createTable(table[0])

    def _processColumns(self, columns):
        result = []
        for row in columns:
            result.append(row[0])
        return result
    
    def _createTable(self, tableName):
        rows = self.dbCursor.execute(Command.SELECT_ALL.substitute(table=tableName)).fetchall()
        columns = self._processColumns(self.dbCursor.description)

        ids = self.dbCursor.execute(Command.SELECT_ID.substitute(column=self.id, table=tableName)).fetchall()
        
        t = Table(tableName, columns, ids)
        self.tables.append(t)

    def getTablesSet(self):
        result = set()
        for table in self.tables:
            result.add(table.name)
        return result
    
    def getTablesList(self):
        result = []
        for table in self.tables:
            cmd = Command.COUNT_ROWS.substitute(table=table.name)
            count = self.dbCursor.execute(cmd).fetchall()
            result.append((table.name, count[0][0]))
        return result
    
    def getTableForName(self, name):
        result = None
        for t in self.tables:
            if(t.name == name):
                result = t
                break
        return result

    def getRowsForIds(self, table, ids):
        result = []
        for id in ids:
            cmd = Command.SELECT_ALL_WHERE.substitute(table=table, condition=self.id + "=" + str(id))
            r = self.dbCursor.execute(cmd).fetchall()
            result.append(r[0])
        return result