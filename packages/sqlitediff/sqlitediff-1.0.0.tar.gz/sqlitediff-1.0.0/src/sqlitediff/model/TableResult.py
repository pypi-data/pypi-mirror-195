class TableResult():
    def __init__(self, tableName, columns, createdRows, 
                 deletedRows, createdRowValues, deletedRowValues,
                 updatedRows, updatedRowValuesBefore, updatedRowValuesAfter) -> None:
        self.tableName = tableName
        self.columns = columns
        self.createdRows = createdRows
        self.deletedRows = deletedRows
        self.createdRowValues = createdRowValues
        self.deletedRowValues = deletedRowValues
        self.updatedRows = updatedRows
        self.updatedRowValuesBefore = updatedRowValuesBefore
        self.updatedRowValuesAfter = updatedRowValuesAfter