class SQLDB:
    def __init__(self, name):
        self.name = name
        self.tables = {}
    
    def addTable(self, sqlTable):
        self.tables[sqlTable.name] = sqlTable
    