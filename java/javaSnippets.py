#!/usr/bin/python3
from dialectUtil import firstSmall, camel

def JavaBody(code):
    return '{\n' + code + '}\n'

def JavaClass(name, code):
    return 'class ' + name + JavaBody(code)
    
def JavaScope(scope, code):
    return scope + ' ' + code

def JavaFunction(scope, name, type, args, code):
    return JavaScope(scope, type + ' ' + name + '('+ args +')' +  JavaBody(code + '\n'))

def JavaImport(package):
    return 'import ' + package + ';\n'

def JavaPackage(package):
    return 'package ' + package + ';\n'

def getter(type, name):
    return JavaFunction('public', 'get'+camel(name), type, '', 'return '+firstSmall(name)+';')

def setter(type, name):
    return JavaFunction('public', 'set'+camel(name), type, type+' '+name, 'this.'+firstSmall(name)+'='+firstSmall(name)+';')

def declare(type, name):
    return JavaScope('private', camel(type) + ' '  + firstSmall(name)+';')

CLASS_ANNOTATIONS = {}
def classAnnotations(javaClass):
    annotations = set()
    for classMetaData in CLASS_ANNOTATIONS:
        if classMetaData in javaClass.metaData:
            annotations.add(CLASS_ANNOTATIONS[classMetaData])
    return annotations