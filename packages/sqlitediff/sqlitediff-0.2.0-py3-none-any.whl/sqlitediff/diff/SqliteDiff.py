from sqlitediff.model.Snapshot import Snapshot
from sqlitediff.diff.DiffResult import DiffResult
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
    
    def _getDeletedRows(self):
        pass

    def _getUpdatedRows(self):
        pass

    def _getCreatedRows(self):
        pass

    def processTables(self):
        deletedTables = self._getDeletedTables()
        createdTables = self._getCreatedTables()
        beforeTables = self.beforeSnapshot.getTablesList()
        afterTables = self.afterSnapshot.getTablesList()

        tableResultList = []
        # Process rows for each table
        for table in afterTables:
            tBeforeTable = self.beforeSnapshot.getTableForName(table[0])
            tAfterTable = self.afterSnapshot.getTableForName(table[0])

            # Check if table already exists in before snapshot
            if(tBeforeTable != None):
                tbeforeIdSet = tBeforeTable.getIdSet()
                tAfterIdSet = tAfterTable.getIdSet()
                createdRows = tAfterIdSet.difference(tbeforeIdSet)
                deletedRows = tbeforeIdSet.difference(tAfterIdSet)
                createdRowValues = self.afterSnapshot.getRowsForIds(table[0], createdRows)
                deletedRowValues = self.beforeSnapshot.getRowsForIds(table[0], deletedRows)
            else:
                # If table is not present in before snapshot but is there in after
                # all rows are newly created
                createdRows = self.afterSnapshot.getTableForName(table[0]).ids
                createdRowValues = self.afterSnapshot.getRowsForIds(table[0], createdRows)
                deletedRows = {}
                deletedRowValues = []


            tResult = TableResult(table[0], tAfterTable.columns, createdRows, 
                                  deletedRows, createdRowValues, deletedRowValues)
            tableResultList.append(tResult)
        
        result = DiffResult(deletedTables, createdTables, 
                            beforeTables, afterTables, tableResultList)
        return result