from sqlitediff.model.Row import Row

class Table():
    def __init__(self, name, columns, ids) -> None:
        self.name = name
        self.columns = columns
        self.rows = []
        self.ids = []
        for id in ids:
            self.ids.append(id[0])

    def addRow(self, row):
        self.rows.append(Row(row))

    def getNumberOfRows(self):
        return len(self.rows)
    
    def getIdSet(self):
        return set(self.ids)