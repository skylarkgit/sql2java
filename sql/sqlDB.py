class SQLDB:
    def __init__(self, name):
        self.name = name
        self.tables = {}
        self.types = {}
    
    def addTable(self, sqlTable):
        self.tables[sqlTable.name] = sqlTable

    def addType(self, sqlType):
        self.types[sqlType.name] = sqlType
    