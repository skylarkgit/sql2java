from dialectUtil import *
from java.javaClass import JAVAClass
from java.javaEnum import JAVAEnum

class JAVAProject:
    def __init__(self, db, package):
        self.package = package
        self.sqlDB = db
        self.models = {}
        self.types = {}
        for table in db.tables:
            model = JAVAClass(db.tables[table], self)
            self.models[model.name] = model
        for sqlType in db.types:
            javaType = JAVAEnum(db.types[sqlType], self)
            self.types[javaType.name] = javaType
        for model in self.models:
            model = self.models[model]
            model.setForeign()

    def save(self):
        for model in self.models:
            self.models[model].save()
            self.models[model].saveRepo()
            self.models[model].saveDAO()
        for javaType in self.types:
            self.types[javaType].save()
            