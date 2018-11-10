from java.javaSnippets import JavaPackage
from java.templates import *
from dialectUtil import *

class JAVAEnum:
    def __init__(self, dbType, project):
        self.name = underScoreToCamelCase(dbType.name)
        self.typeList = dbType.typeList
        self.project = project

    def save(self):
        code = JavaPackage(self.project.package + '.model')
        enumDetails = {}
        enumDetails['typeName'] = self.name
        enumDetails['typeList'] = ', '.join(self.typeList)
        code += self.getBody().format(**enumDetails)
        filename = 'model/' + self.name + '.java'
        with open( filename,'w') as the_file:
            the_file.write(code)

    def getBody(self):
        if not hasattr(self, 'body'):
            body = open('./java/templates/enum.template.py')
            self.body = body.read()
        return self.body