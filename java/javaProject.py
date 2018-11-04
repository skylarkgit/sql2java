from dialectUtil import *
from java.javaClass import JAVAClass

class JAVAProject:
    def __init__(self, db, package):
        self.package = package
        self.sqlDB = db
        self.models = {}
        for table in db.tables:
            model = JAVAClass(db.tables[table], self)
            self.models[model.name] = model
        for model in self.models:
            model = self.models[model]
            model.setForeign()

    def save(self):
        for model in self.models:
            self.models[model].save()