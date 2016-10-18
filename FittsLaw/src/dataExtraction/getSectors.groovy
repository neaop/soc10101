package dataExtraction
import candid.ConnectDB

def DBname = "schoolsv6"
def domain = "localhost"
def UserName = "root"
def PassWord = "admin"

def connection = new ConnectDB(domain, DBname, UserName, PassWord)
def sql = connection.getConnection()

println "Connection made to MySQL $DBname"

def sectorData = """
SELECT patternX
FROM fittssectorid
WHERE patternRef = ?
"""

def sid3 = sql.rows(sectorData,[3])
def sid4 = sql.rows(sectorData,[4])

sid3.each{println "$it"}

sid3