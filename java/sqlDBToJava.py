from sql.sqlDB import SQLDB
from java.javaProject import JAVAProject

class SQLDBToJAVA:
    def __init__(self, sqlDB, package):
        self.sqlDB = sqlDB
        self.project = JAVAProject(sqlDB, package)
        self.package = package
    
    def save(self):
        self.project.save()