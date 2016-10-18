import pymysql

con = pymysql.connect(host='localhost', port=3306, user='root', passwd='admin', db='schoolsv6')
cur = con.cursor()

pat3sec = []
pat4sec = []

cur.execute("SELECT `patternX` FROM `fittssectorid` WHERE `patternRef` = 3")
for row in cur:
    for val in row:
        pat3sec.append(val)

cur.execute("SELECT `patternX` FROM `fittssectorid` WHERE `patternRef` = 4")
for row in cur:
    for val in row:
        pat4sec.append(val)


# print(pat3sec)s
# print(pat4sec)

cur.execute("SELECT * FROM fittsliftlocations WHERE patternRef = 3")

# print(cur.fetchone())

header = ['collectionref', 'sequenceNo', 'patternRef', 'xCoord', 'yCoord', 'liftDuration', 'sectorID']

pat3 = [header]
pat4 = [header]

for row in cur:
    sector = 1
    for val in pat3sec:

        if row[3] > val:
            sector += 1

    newRow = list(row)
    newRow.append(sector)
    pat3.append(newRow)

cur.execute("SELECT * FROM fittsliftlocations WHERE patternRef =4")

for row in cur:
    sector = 1
    for val in pat4sec:

        if row[3] > val:
            sector += 1

    newRow = list(row)
    newRow.append(sector)
    pat4.append(newRow)


for val in pat3:
    print(val)

print()
print()

for val in pat4:
    print(val)

cur.close()
con.close()