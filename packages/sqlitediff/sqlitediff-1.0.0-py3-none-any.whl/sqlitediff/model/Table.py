class Table():
    def __init__(self, name, columns, ids) -> None:
        self.name = name
        self.columns = columns
        self.ids = []
        for id in ids:
            self.ids.append(id[0])
    
    def getIdSet(self):
        return set(self.ids)