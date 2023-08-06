class Printer():
    def __init__(self) -> None:
        pass

    def print(self, result):
        print("Tables before Action: " + str(result.beforeTables))
        print("Tables after Action: " + str(result.afterTables))

        print("Deleted Tables: " + str(result.deletedTables))
        print("Created Tables: " + str(result.createdTables))