class DiffResult():
    def __init__(self, deletedTables, createdTables, beforeTables, afterTables, tableResults) -> None:
        self.deletedTables = sorted(deletedTables)
        self.createdTables = sorted(createdTables)
        self.beforeTables = sorted(beforeTables)
        self.afterTables = sorted(afterTables)
        self.tableResults = tableResults