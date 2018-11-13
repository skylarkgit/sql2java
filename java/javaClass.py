#!/usr/bin/python3
from dialectUtil import *
from java.javaProperty import JAVAProperty
from java.javaSnippets import *
from java.javaLink import JAVALink
import constants as CONST

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
        self.imports.add('javax.persistence.PrePersist')
        for javaProperty in self.properties:
            javaProperty = self.properties[javaProperty]
            for importfile in javaProperty.imports:
                self.imports.add(importfile)
        code = JavaPackage(self.project.package + '.' + CONST.MODEL)
        code += self.getImports()
        body = '\n'.join(sorted(list(map(lambda token: self.properties[token].declare(), self.properties)),key = len))
        body += '\n'.join(list(map(lambda token: self.properties[token].setter(), self.properties)))
        body += '\n'.join(list(map(lambda token: self.properties[token].getter(), self.properties)))
        prePersistCode = ''
        if 'uuid' in self.metaData:
            prePersistCode += '\nuuid = UUID.randomUUID();\n'
        prePersist = '\n@PrePersist\npublic void prePersist(){{{0}}}\n'
        body += prePersist.format(prePersistCode)
        code += '\n'.join(classAnnotations(self))
        code += '@Entity\n@JsonIgnoreProperties({"hibernateLazyInitializer", "handler"})\n'+JavaScope('public', JavaClass(self.name + extension, body))

        filename = CONST.MODEL + '/' + self.name + '.java'
        with open( filename,'w') as the_file:
            the_file.write(code)
    
    def saveRepo(self):
        code = JavaPackage(self.project.package + '.' + CONST.REPO)
        code += JavaImport('org.springframework.data.jpa.repository.JpaRepository')
        code += JavaImport(self.project.package + '.' + CONST.MODEL + '.' + self.name)
        code += 'public interface {0}Repository extends JpaRepository<{0}, Long> {{\n\n}}'.format(self.name)
        filename = CONST.REPO + '/' + self.name + 'Repository.java'
        with open( filename,'w') as the_file:
            the_file.write(code)


    def getImports(self):
        return '\n'.join(list(map(lambda token: JavaImport(token), self.imports)))