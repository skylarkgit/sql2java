#!/usr/bin/python3
from dialectUtil import *
from sql.sqlField import SQLField
from java.javaAnnotations import annotationsFor
from java.javaSnippets import JavaFunction

class JAVAProperty:
    def __init__(self, sqlField = None, javaClass = None):
        self.scope = 'private'
        self.isFK = False
        self.imports = set()
        if sqlField != None:
            self.javaClass = javaClass
            self.name = firstSmall(underScoreToCamelCase(sqlField.name)).strip()
            self.type = sqlToJAVAType(sqlField.type)
            self.metaData = sqlField.metaData
            self.isFK = (sqlField.fk != None)
            self.setup()

    def setup(self):
        self.annotate()
        self.resolveImports()

    def annotate(self):
        self.annotations = []
        for annotation in annotationsFor(self.metaData, self):
            self.annotations.append(annotation)

    def getter(self):
        return JavaFunction('public', 'get' + camel(self.name), self.type, '', 'return ' + self.name + ';')
    
    def setter(self):
        return JavaFunction('public', 'set' + camel(self.name), 'void', self.type + ' ' + self.name, 'this.' + self.name + '=' + self.name + ';')
    
    def declare(self):
        return '\n'.join(self.annotations) + '\n' + self.scope + ' ' + self.type  + ' ' + self.name + ';\n'
    
    def resolveImports(self):
        for importFile in resolveJAVAImport(self.type, self.javaClass.project.package):
            self.imports.add(importFile)
        for annotation in self.annotations:
            for importFile in resolveJAVAImport(annotation, self.javaClass.project.package):
                self.imports.add(importFile)
