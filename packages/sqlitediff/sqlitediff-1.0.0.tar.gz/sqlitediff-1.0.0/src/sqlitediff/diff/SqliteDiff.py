import hashlib

from sqlitediff.diff.DiffResult import DiffResult
from sqlitediff.model.Snapshot import Snapshot
from sqlitediff.model.TableResult import TableResult


class SqliteDiff():
    def __init__(self, id, pathBefore, pathAfter) -> None:
        self.beforeSnapshot = Snapshot("before", pathBefore, id)
        self.afterSnapshot = Snapshot("after", pathAfter, id)
        self.bTableSet = self.beforeSnapshot.getTablesSet()
        self.aTableSet = self.afterSnapshot.getTablesSet()

    def _getDeletedTables(self):
        t = self.bTableSet.difference(self.aTableSet)
        return list(t)
    
    def _getCreatedTables(self):
        t = self.aTableSet.difference(self.bTableSet)
        return list(t)
    
    def getSnapshotForName(self, name):
        result = None
        if(name == "before"):
            result = self.beforeSnapshot
        elif(name == "after"):
            result = self.afterSnapshot
        return result
    
    def process(self):
        deletedTables = self._getDeletedTables()
        createdTables = self._getCreatedTables()
        beforeTables = self.beforeSnapshot.getTablesList()
        afterTables = self.afterSnapshot.getTablesList()
        allTables = self.aTableSet.union(self.bTableSet)
        tableResultList = []
        
        # Process rows for each table
        for table in allTables:
            tBeforeTable = self.beforeSnapshot.getTableForName(table)
            tAfterTable = self.afterSnapshot.getTableForName(table)

            if(tBeforeTable != None and tAfterTable != None):
                # Case 1: Table exists in both snapshots
                columns = tBeforeTable.columns
                tbeforeIdSet = tBeforeTable.getIdSet()
                tAfterIdSet = tAfterTable.getIdSet()
                createdRows = tAfterIdSet.difference(tbeforeIdSet)
                deletedRows = tbeforeIdSet.difference(tAfterIdSet)
                createdRowValues = self.afterSnapshot.getRowsForIds(table, createdRows)
                deletedRowValues = self.beforeSnapshot.getRowsForIds(table, deletedRows)

                sameRows = list(tAfterIdSet.intersection(tbeforeIdSet))
                sameRowValuesBefore = self.beforeSnapshot.getRowsForIds(table, sameRows)
                sameRowValuesAfter = self.afterSnapshot.getRowsForIds(table, sameRows)

                updatedRows = []
                for i in range(0, len(sameRows)):
                    bHash = hashlib.sha256(str(sameRowValuesBefore[i]).encode()).hexdigest()
                    aHash = hashlib.sha256(str(sameRowValuesAfter[i]).encode()).hexdigest()
                    if(bHash != aHash):
                        updatedRows.append(sameRows[i])

                updatedRowValuesBefore = self.beforeSnapshot.getRowsForIds(table, updatedRows)
                updatedRowValuesAfter = self.afterSnapshot.getRowsForIds(table, updatedRows)

            elif(tBeforeTable != None and tAfterTable == None):
                # Case 2: Table exists in before Snapshot but not in after snapshot
                columns = tBeforeTable.columns
                createdRows = []
                createdRowValues = []
                deletedRows = self.beforeSnapshot.getTableForName(table).ids
                deletedRowValues = self.beforeSnapshot.getRowsForIds(table, deletedRows)
                updatedRows = []
                updatedRowValuesBefore = []
                updatedRowValuesAfter = []

            elif(tBeforeTable == None and tAfterTable != None):
                # Case 3: Table exists in after Snapshot but not in before snapshot
                columns = tAfterTable.columns
                createdRows = self.afterSnapshot.getTableForName(table).ids
                createdRowValues = self.afterSnapshot.getRowsForIds(table, createdRows)
                deletedRows = {}
                deletedRowValues = []
                updatedRows = []
                updatedRowValuesBefore = []
                updatedRowValuesAfter = []

            tResult = TableResult(table, columns, createdRows, 
                                  deletedRows, createdRowValues, deletedRowValues,
                                  updatedRows, updatedRowValuesBefore, updatedRowValuesAfter)
            tableResultList.append(tResult)
        
        result = DiffResult(deletedTables, createdTables, 
                            beforeTables, afterTables, tableResultList)
        return result