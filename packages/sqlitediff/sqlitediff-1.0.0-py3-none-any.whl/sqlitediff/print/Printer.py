class Printer():
    def __init__(self) -> None:
        pass

    def _printTableValues(self, values):
        for table in values:
            print("         --- ")
            print("         Name: " + str(table[0]))
            print("         Rows: " + str(table[1]))
        print("         --- ")
        print("")

    def _printTableNameList(self, values):
        r = []
        for v in values:
            r.append(v[0])
        print("         --- ")
        print("         List: " + str(r))

    def _printTableList(self, values):
        print("         --> " + str(values))
        print("")

    def _printTableAnalysis(self, result):
        print("Table Analysis")
        print("---")
        print("")
        print("--> Tables before: ")
        self._printTableNameList(result.beforeTables)
        self._printTableValues(result.beforeTables)
        print("--> Tables after: ")
        self._printTableNameList(result.afterTables)
        self._printTableValues(result.afterTables)
        print("--> Deleted Tables: ")
        self._printTableList(result.deletedTables)
        print("--> Created Tables: ")
        self._printTableList(result.createdTables)

    def _printRowAnalysis(self, result):
        print("")
        print("")
        print("Row Analysis")
        print("---")

        for t in result.tableResults:
            print("")
            print("--> " + t.tableName)
            print("    ---")
            print("    Colums:")
            print("    ---")
            print("     --> " + str(t.columns))
            print("    ---")
            if(len(t.createdRows) > 0):
                print("    Created: " + str(t.createdRows))
                print("    ---")
                for value in t.createdRowValues:
                    print("     --> " + str(value))
                print("    ---")
            if(len(t.updatedRows) > 0):
                print("   Updated: " + str(t.updatedRows))
                print("    ---")
                for i in range(0, len(t.updatedRows)):
                    print("     --> " + str(t.updatedRowValuesBefore[i]))
                    print("     --> " + str(t.updatedRowValuesAfter[i]))
                    print("    ---")
            if(len(t.deletedRows) > 0):    
                print("    Deleted: " + str(t.deletedRows))
                print("    ---")
                for value in t.deletedRowValues:
                    print("     --> " + str(value))
                print("    ---")
            if(len(t.createdRows) == 0 and len(t.deletedRows) == 0 and len(t.updatedRows) == 0):
                print("    No Changes")
                print("    ---")
            print("")

    def printAnalysis(self, result):
        self._printTableAnalysis(result)
        self._printRowAnalysis(result)


    def printSnapshot(self, snapshot):
        print("Snapshot Name: " + snapshot.name)
        print("---")
        for table in snapshot.tables:
            print("   Table Name: " + table.name)
            print("         Rows: " + str(snapshot.getRowCountForTable(table.name)))
            print("      Columns: " + str(table.columns))
            print("   Row Values: ")
            print("          --- ")
            for row in snapshot.getRowsForTable(table.name):
                    print("           --> " + str(row))
            print("          --- ")
            print("---")
