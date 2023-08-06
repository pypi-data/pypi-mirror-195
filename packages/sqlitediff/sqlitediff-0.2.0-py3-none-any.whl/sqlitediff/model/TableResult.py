class TableResult():
    def __init__(self, tableName, columns, createdRows, deletedRows, createdRowValues, deletedRowValues) -> None:
        self.tableName = tableName
        self.columns = columns
        self.createdRows = createdRows
        self.deletedRows = deletedRows
        self.createdRowValues = createdRowValues
        self.deletedRowValues = deletedRowValues