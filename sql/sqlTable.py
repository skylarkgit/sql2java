from sql.sqlField import SQLField
from sql.language import splitEscaped
import enum
import re

class FK_TYPE(enum.Enum):
    ManyToOne = 1
    OneToOne = 2
    ManyToMany = 3
    OneToMany = 4


class SQLTable:
    def __init__(self, db, query):
        self.db = db
        self.query = query
        self.name = SQLTable.getTableName(query)
        fields = re.split(r',(?![^()]*\))', query[self.query.find('(') + 1:-1]) #splitEscaped(, ',', '(')
        print(query)
        fields = list(map(lambda token: token.strip(), fields))
        self.fields = {}

        for field in fields:
            fieldTokens = field.split(' ')
            if fieldTokens[0].lower().strip() == 'constraint':
                continue
            if fieldTokens[0].lower().strip() == 'unique':
                continue
            if fieldTokens[0].lower().strip() == 'foreign':
                self.addForeignConstraint(field)
            else:
                self.addField(SQLField(field))
        
    def addField(self, sqlField):
        self.fields[sqlField.name] = sqlField

    def addForeignConstraint(self, field):
        local = field.split('(')[1].split(')')[0].strip().lower().strip()
        foreign = field.split('(')[2].split(')')[0].strip().lower().strip()
        foreignTable = field.split('(')[1].split(' ')[-1].strip().lower().strip()
        linkType = '@'+(field.split('@')[1].strip())
        self.fields[local].setLink(self.db.tables[foreignTable], foreign, linkType, self.name)

    @staticmethod
    def getTableName(query):
        return query.split('(')[0].strip().split(' ')[-1].strip()
    