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
pattern3Lifts = [header]
pattern4Lifts = [header]

curr.execute("SELECT collectionref, sequenceNo, patternRef, xCoord FROM fittsliftlocations WHERE patternRef = 3")

for row in curr:
    sectorCount = 1
    for sectorCoord in pattern3Sectors:
        if row[3] > (sectorCoord - tolerance):
            sectorCount += 1

    tempRow = list(row)
    tempRow.append(sectorCount)
    pattern3Lifts.append(tempRow)

curr.execute("SELECT collectionref, sequenceNo, patternRef, xCoord FROM fittsliftlocations WHERE patternRef =4")

for row in curr:
    sectorCount = 1
    for sectorCoord in pattern4Sectors:
        if row[3] > (sectorCoord-tolerance):
            sectorCount += 1

    tempRow = list(row)
    tempRow.append(sectorCount)
    pattern4Lifts.append(tempRow)

for val in pattern3Lifts:
    print(val)

print()
print()

for val in pattern4Lifts:
    print(val)

curr.close()
con.close()
