from dialectUtil import *
from java.javaProperty import JAVAProperty
from java.javaSnippets import *
from java.javaLink import JAVALink

class JAVAClass:
    def __init__(self, dbTable, project):
        self.project = project
        self.name = underScoreToCamelCase(dbTable.name).strip()
        self.properties = {}
        self.imports = set()
        self.foreignElements = {}
        self.dbTable = dbTable
        #print("###### name = "+self.name+ " ^^^^^^^^^^^^^^^^")
        for field in dbTable.fields:
            field = dbTable.fields[field]
            if field.fk is None:
                #print(field.name)
                property = JAVAProperty(field, self)
                self.properties[property.name] = property
    
    def setForeign(self):
        for field in self.dbTable.fields:
            field = self.dbTable.fields[field]
            if field.fk is not None:
                link = JAVALink(field.fk, self)
                if link is not None:
                    self.foreignElements[link.localProperty] = link
                    

    def save(self):
        for property in self.properties:
            property = self.properties[property]
            for importfile in property.imports:
                self.imports.add(importfile)
        code = JavaPackage(self.project.package + '.model')
        code += self.getImports()
        body = '\n'.join(list(map(lambda token: self.properties[token].declare(), self.properties)))
        body += '\n'.join(list(map(lambda token: self.properties[token].setter(), self.properties)))
        body += '\n'.join(list(map(lambda token: self.properties[token].getter(), self.properties)))
        code += JavaScope('public', JavaClass(self.name, body))

        filename = 'model/' + self.name + '.java'
        with open( filename,'w') as the_file:
            the_file.write(code)
    
    def getImports(self):
        return '\n'.join(list(map(lambda token: JavaImport(token), self.imports)))