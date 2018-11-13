from sql.sqlParser import SQLParse
from java.sqlTableToJavaClass import SQLTableToJavaClass
from java.sqlDBToJava import SQLDBToJAVA

import os

if not os.path.exists('modal'):
    os.makedirs('modal')
if not os.path.exists('repository'):
    os.makedirs('repository')

other = open('./sample/main.sql')
master = open('./sample/master.sql')
sqlParse = SQLParse('l&f', master.read() + '\n' + other.read())
db = sqlParse.getDB()
project = SQLDBToJAVA(db,'com.metacube.tms')
project.save()