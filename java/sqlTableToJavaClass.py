from sql.sqlTable import SQLTable
from dialectUtil import *

class JavaProperty:
    def __init__(self, scope, name, type):
        self.name = name
        self.type = getJavaType(type)
        self.scope = scope
    
    def code(self):
        if (self.name == 'id'):
            return '@Id\n' + '@GeneratedValue(strategy = GenerationType.AUTO)\n' + self.scope + ' ' + self.type  + ' ' + self.name + ';\n'    
        return self.scope + ' ' + self.type  + ' ' + self.name + ';\n'
    
    def getter(self):
        return JavaFunction('public', 'get' + camel(self.name), self.type, '', 'return ' + self.name + ';')
    
    def setter(self):
        return JavaFunction('public', 'set' + camel(self.name), 'void', self.type + ' ' + self.name, 'this.' + self.name + '=' + self.name + ';')

class SQLTableToJavaClass:
    def __init__(self, sqlTable):
        self.table = sqlTable
        self.properties = []
        self.initProperties()
        self.annotations = '@Entity\n'

    def initProperties(self):
        for prop in self.table.fields:
            prop = self.table.fields[prop]
            self.properties.append(JavaProperty('private', prop.name, prop.type))

    def getJavaClass(self):
        return ('package com.metacube.learninganddevelopment.model;\nimport java.util.UUID;import java.sql.Timestamp;import javax.persistence.Entity;import javax.persistence.GeneratedValue;import javax.persistence.GenerationType;import javax.persistence.Id;'
        + self.annotations + JavaScope('public', JavaClass(self.table.name, (''.join(map(lambda property : property.code(), self.properties))
        + (''.join(map(lambda property : property.getter(), self.properties)))
        + (''.join(map(lambda property : property.setter(), self.properties)))))))

    def getRepositoryClass(self):
        return ('package com.metacube.learninganddevelopment.repository;\nimport org.springframework.data.jpa.repository.JpaRepository;\nimport com.metacube.learninganddevelopment.model.' + self.table.name + ';\n'
        + JavaScope('public', 'interface ' + self.table.name + 'Repository extends JpaRepository<' + self.table.name + ', Long> {\n\n}\n'))