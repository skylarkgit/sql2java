#!/usr/bin/python3
from sql.sqlField import SQLLink
from dialectUtil import *
from java.javaSnippets import *
from java.javaAnnotations import annotationsFor
from java.javaProperty import JAVAProperty

class JAVALink:
    def __init__(self, sqlLink, ownerClass):
        self.localProperty = firstSmall(underScoreToCamelCase(sqlLink.localField))
        self.remoteProperty = firstSmall(underScoreToCamelCase(sqlLink.remoteField))
        self.remoteClass = underScoreToCamelCase(sqlLink.remoteTable.name)
        self.linkType = sqlLink.linkType
        self.javaClass = ownerClass
        self.localPart = self.setUpLocal()
        self.foreignPart = self.setUpForiegn()

    def setUpLocal(self):
        local = JAVAProperty()
        local.metaData = self.linkType
        if '@OneToOne' in self.linkType or '@ManyToOne' in self.linkType:
            local.name = firstSmall(self.remoteClass)
            local.type = self.remoteClass
            local.javaClass = self.javaClass
            local.javaClass.properties[local.name] = local
            local.setup()
        return local
    
    def setUpForiegn(self):
        foreign = JAVAProperty()
        foreign.metaData = self.linkType
        if '@OneToOne' in self.linkType:
            foreign.name = firstSmall(self.javaClass.name)
            foreign.type = self.javaClass.name
            foreign.javaClass = self.javaClass.project.models[self.remoteClass]
            foreign.javaClass.properties[foreign.name] = foreign
            foreign.setup()
        if '@ManyToOne' in self.linkType:
            foreign.name = firstSmall(self.javaClass.name) + 'List'
            foreign.type = 'List<'+self.javaClass.name+'>'
            foreign.javaClass = self.javaClass.project.models[self.remoteClass]
            foreign.javaClass.properties[foreign.name] = foreign
            foreign.setup()
        if '@ManyToMany(' in self.linkType:
            listType = underScoreToCamelCase(self.linkType.split('(')[1].split(')')[0])
            if listType not in self.javaClass.project.models:
                listType = 'String'
            foreign.name = firstSmall(self.javaClass.name) + 'List'
            foreign.type = 'List<'+listType+'>'
            foreign.javaClass = self.javaClass.project.models[self.remoteClass]
            foreign.javaClass.properties[foreign.name] = foreign
            foreign.setup()
        return foreign
