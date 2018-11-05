from sql.sqlTable import SQLTable
from sql.sqlField import SQLField
from sql.language import *
from sql.sqlDB import SQLDB

import enum 
class SQL_TOKEN_TYPE (enum.Enum): 
    OPERATOR = 1
    DATATYPE = 2
    FUNCTION = 3
    PROPERTY = 4
    COMMAND = 4
    ENTITY = 4

class SQLToken:
    def __init__(self, name, type):
        self.name = name.lower()
        self.type = type

SQL_KEYWORDS = [
    SQLToken('CREATE', SQL_TOKEN_TYPE.COMMAND),
    SQLToken('DROP', SQL_TOKEN_TYPE.COMMAND),

    SQLToken('ENUM', SQL_TOKEN_TYPE.ENTITY),
    SQLToken('TABLE', SQL_TOKEN_TYPE.ENTITY),
    SQLToken('EXTENSION', SQL_TOKEN_TYPE.ENTITY),

    SQLToken('NOT', SQL_TOKEN_TYPE.OPERATOR),

    SQLToken('IF', SQL_TOKEN_TYPE.FUNCTION),
    SQLToken('EXISTS', SQL_TOKEN_TYPE.FUNCTION),
    SQLToken('MIN', SQL_TOKEN_TYPE.FUNCTION),
    SQLToken('MAX', SQL_TOKEN_TYPE.FUNCTION),
    SQLToken('NOW', SQL_TOKEN_TYPE.FUNCTION),

    SQLToken('VARCHAR', SQL_TOKEN_TYPE.DATATYPE),
    SQLToken('SERIAL', SQL_TOKEN_TYPE.DATATYPE),
    SQLToken('BIGSERIAL', SQL_TOKEN_TYPE.DATATYPE),
    SQLToken('FLOAT', SQL_TOKEN_TYPE.DATATYPE),
    SQLToken('DOUBLE PRECISION', SQL_TOKEN_TYPE.DATATYPE),
    SQLToken('INTEGER', SQL_TOKEN_TYPE.DATATYPE),
    SQLToken('UUID', SQL_TOKEN_TYPE.DATATYPE),

    SQLToken('NULL', SQL_TOKEN_TYPE.PROPERTY),
    SQLToken('PRIMARY KEY', SQL_TOKEN_TYPE.PROPERTY),
    SQLToken('ON UPDATE', SQL_TOKEN_TYPE.PROPERTY)
]

class SQLParse:

    def __init__(self, name, query):
        self.query = query
        self.db = SQLDB(name)
        query = escapeAnnotations(query)
        queries = removeComments(query).split('\n')
        print(queries)
        queries = '\n'.join(map(lambda token: (token+' ')[0:token.find("--")].strip(), queries))
        queries = queries.split(';')
        self.queries = map(lambda token: token.replace("\r\n","").replace("\n","").strip(), queries)
        
        for q in queries:
            entity = SQLParse.resolve(self.db, q)
            if (isinstance(entity, SQLTable)):
                self.db.addTable(entity)

    @staticmethod
    def create(db, query):
        tokens = query.split(' ')
        if (tokens[1].lower() == 'table'):
            return SQLTable(db, query)

    @staticmethod
    def resolve(db, query):
        tokens = query.split(' ')
        if 'create' in tokens[0].lower():
            return SQLParse.create(db, query)

    def getDB(self):
        return self.db