import re
import config

SQLToJAVAType = {}
SQLToJAVAType['varchar'] = 'String'
SQLToJAVAType['bigserial'] = 'Long'
SQLToJAVAType['bigint'] = 'Long'
SQLToJAVAType['uuid'] = 'UUID'
SQLToJAVAType['int'] = 'Integer'
SQLToJAVAType['json'] = 'String'
SQLToJAVAType['double'] = 'Double'
SQLToJAVAType['float'] = 'Float'
SQLToJAVAType['timestamp'] = 'Timestamp'
SQLToJAVAType['boolean'] = 'Boolean'

def sqlToJAVAType(type):
    type = type.lower()
    if type in SQLToJAVAType:
        return SQLToJAVAType[type]
    else:
        return 'String'

def camel(strToConvert):
    return strToConvert[:1].capitalize() + strToConvert[1:]

def underScoreToCamelCase(strToConvert):
    strToConvert = strToConvert.lower()
    return ''.join(list(map(camel, strToConvert.split('_'))))

def firstSmall(strToConvert):
    return strToConvert[:1].lower() + strToConvert[1:]

JAVA_IMPORTS = {}
JAVA_IMPORTS['Integer'] = []
JAVA_IMPORTS['Boolean'] = []
JAVA_IMPORTS['Long'] = []
JAVA_IMPORTS['String'] = []
JAVA_IMPORTS['Double'] = []
JAVA_IMPORTS['Float'] = []
JAVA_IMPORTS['List'] = ['java.util.List']
JAVA_IMPORTS['Set'] = ['java.util.Set']
JAVA_IMPORTS['UUID'] = ['java.util.UUID']
JAVA_IMPORTS['Timestamp'] = ['java.sql.Timestamp']
JAVA_IMPORTS['@Entity'] = ['javax.persistence.Entity']
JAVA_IMPORTS['@Id'] = ['javax.persistence.Id']
JAVA_IMPORTS['@GeneratedValue'] = ['javax.persistence.GeneratedValue', 'javax.persistence.GenerationType']
JAVA_IMPORTS['@OneToOne'] = ['javax.persistence.OneToOne']
JAVA_IMPORTS['@OneToMany'] = ['javax.persistence.OneToMany']
JAVA_IMPORTS['@ManyToOne'] = ['javax.persistence.ManyToOne']
JAVA_IMPORTS['@ManyToMany'] = ['javax.persistence.ManyToMany']
JAVA_IMPORTS['@JsonIgnore'] = ['com.fasterxml.jackson.annotation.JsonIgnore']
JAVA_IMPORTS['@JoinColumn'] = ['javax.persistence.JoinColumn']
JAVA_IMPORTS['@JsonIgnoreProperties'] = ['com.fasterxml.jackson.annotation.JsonIgnoreProperties']
JAVA_IMPORTS['@JoinTable'] = ['javax.persistence.JoinColumn', 'javax.persistence.JoinTable']

def resolveJAVAImport(type, package):
    if '<' in type:
        print(type)
        first = resolveJAVAImport(type.split('<')[0].strip(), package)
        second = resolveJAVAImport(type.split('<')[1].split('>')[0].strip(), package)
        merged = []
        for i in first:
            merged.append(i)
        for i in second:
            merged.append(i)
        print(merged)
        return merged
    type = type.split('(')[0].strip()
    if type in JAVA_IMPORTS:
        return JAVA_IMPORTS[type]
    return [package + '.model.' + type]