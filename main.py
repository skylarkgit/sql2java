from sql.sqlParser import SQLParse
from java.sqlTableToJavaClass import SQLTableToJavaClass
from java.sqlDBToJava import SQLDBToJAVA
import constants as CONST

import os

if not os.path.exists(CONST.MODEL):
    os.makedirs(CONST.MODEL)
if not os.path.exists(CONST.REPO):
    os.makedirs(CONST.REPO)

other = open('./sample/main.sql')
master = open('./sample/master.sql')
sqlParse = SQLParse('l&f', master.read() + '\n' + other.read())
db = sqlParse.getDB()
project = SQLDBToJAVA(db, 'com.metacube.learninganddevelopment')
project.save()