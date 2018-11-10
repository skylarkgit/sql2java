#!/usr/bin/python3
from dialectUtil import underScoreToCamelCase
from java.javaProperty import JAVAProperty
from java.javaSnippets import *
from java.javaLink import JAVALink

JAVA_PROPERTIES = {}
JAVA_PROPERTIES['JAVA_AUTO_IMPORTABLE'] = ['created_by','last_modified_by','created_date', 'last_modified_date']
class JAVAClass:
    def __init__(self, dbTable, project):
        self.project = project
        self.name = underScoreToCamelCase(dbTable.name).strip()
        self.properties = {}
        self.imports = set()
        self.foreignElements = {}
        self.dbTable = dbTable
        self.metaData = ' '
        for field in dbTable.fields:
            field = dbTable.fields[field]
            if field.fk is None:
                javaProperty = JAVAProperty(field, self)
                self.metaData += javaProperty.metaData + ' '
                isImportable = False
                for importable in JAVA_PROPERTIES['JAVA_AUTO_IMPORTABLE']:
                    if importable in javaProperty.metaData:
                        isImportable = True
                if not isImportable:
                    self.properties[javaProperty.name] = javaProperty
    
    def setForeign(self):
        for field in self.dbTable.fields:
            field = self.dbTable.fields[field]
            if field.fk is not None:
                link = JAVALink(field.fk, self)
                if link is not None:
                    self.foreignElements[link.localProperty] = link
                    

    def save(self):
        extension = ''
        if 'created_by' in self.metaData:
            extension = ' extends Auditable<Long>'
        self.imports.add('javax.persistence.Entity')
        self.imports.add('com.fasterxml.jackson.annotation.JsonIgnoreProperties')
        for javaProperty in self.properties:
            javaProperty = self.properties[javaProperty]
            for importfile in javaProperty.imports:
                self.imports.add(importfile)
        code = JavaPackage(self.project.package + '.model')
        code += self.getImports()
        body = '\n'.join(sorted(list(map(lambda token: self.properties[token].declare(), self.properties)),key = len))
        body += '\n'.join(list(map(lambda token: self.properties[token].setter(), self.properties)))
        body += '\n'.join(list(map(lambda token: self.properties[token].getter(), self.properties)))
        code += '\n'.join(classAnnotations(self))
        code += '@Entity\n@JsonIgnoreProperties({"hibernateLazyInitializer", "handler"})\n'+JavaScope('public', JavaClass(self.name + extension, body))

        filename = 'model/' + self.name + '.java'
        with open( filename,'w') as the_file:
            the_file.write(code)
    
    def getImports(self):
        return '\n'.join(list(map(lambda token: JavaImport(token), self.imports)))