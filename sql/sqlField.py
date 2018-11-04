class SQLLink :
    def __init__(self, localField, remoteTable, remoteField, linkType):
        self.localField = localField
        self.remoteField = remoteField
        self.remoteTable = remoteTable
        self.linkType = linkType

class SQLField:
    def __init__(self, field):
        fieldTokens = field.split(' ')
        self.name = fieldTokens[0].lower().strip()
        self.type = fieldTokens[1].split('(')[0].lower().strip()
        self.metaData = field
        self.fk = None

    def setLink(self, remoteTable, remoteField, linkType):
        self.fk = SQLLink(self.name, remoteTable, remoteField, linkType)