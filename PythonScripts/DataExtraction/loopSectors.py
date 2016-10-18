import pymysql

tolerance = 10

con = pymysql.connect(host='localhost', port=3306, user='root', passwd='admin', db='schoolsv6')
curr = con.cursor()

pattern3Sectors = []
pattern4Sectors = []

curr.execute("SELECT `patternX` FROM `fittssectorid` WHERE `patternRef` = 3")
for row in curr:
    for val in row:
        pattern3Sectors.append(val)

curr.execute("SELECT `patternX` FROM `fittssectorid` WHERE `patternRef` = 4")
for row in curr:
    for val in row:
        pattern4Sectors.append(val)

header = ['collectionref', 'sequenceNo', 'patternRef', 'xCoord', 'sectorID']
pattern3Loops = [header]
pattern4Loops = [header]

curr.execute("SELECT collectionref, sequenceNo, patternRef, xCoord FROM fittslooplocations WHERE patternRef = 3")

for row in curr:
    sectorCount = 1
    for sectorCoord in pattern3Sectors:
        if row[3] > (sectorCoord - tolerance):
            sectorCount += 1

    tempRow = list(row)
    tempRow.append(sectorCount)
    pattern3Loops.append(tempRow)

for val in pattern3Loops:
    print(val)
