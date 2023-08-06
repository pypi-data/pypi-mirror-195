class DiffResult():
    def __init__(self, deletedTables, createdTables, beforeTables, afterTables) -> None:
        self.deletedTables = deletedTables
        self.createdTables = createdTables
        self.beforeTables = beforeTables
        self.afterTables = afterTables