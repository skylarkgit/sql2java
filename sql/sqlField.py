class SQLLink :
    def __init__(self, localField, remoteTable, remoteField, linkType, ownerTableName):
        self.localField = localField
        self.remoteField = remoteField
        self.remoteTable = remoteTable
        self.linkType = linkType
        self.ownerTableName = ownerTableName

class SQLField:
    def __init__(self, field):
        fieldTokens = field.split(' ')
        print(fieldTokens)
        self.name = fieldTokens[0].lower().strip()
        self.type = fieldTokens[1].split('(')[0].lower().strip()
        self.metaData = field
        self.fk = None

    def setLink(self, remoteTable, remoteField, linkType, tableName):
        self.fk = SQLLink(self.name, remoteTable, remoteField, linkType, tableName)