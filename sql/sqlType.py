class SQLType:
    def __init__(self, db, query):
        self.name = query.strip().split(' ')[2].strip()
        self.typeList = list(map(lambda token: token.strip()[1:-1] ,query[query.find('(')+1:query.find(')')].split(',')))
        self.db = db
        