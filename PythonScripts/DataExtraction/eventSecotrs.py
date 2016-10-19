import pymysql


def geteventsectors(event_table, pattern_no, tollearnace):

    con = pymysql.connect(host='localhost', port=3306, user='root', passwd='admin', db='schoolsv6')
    curr = con.cursor()

    pattern_sectors = []

    curr.execute("SELECT patternX FROM fittssectorid WHERE patternRef = %s", pattern_no)

    for row in curr:
        pattern_sectors.append(list(row))

    for val in pattern_sectors:
        print(val)

    header = ['collectionref', 'sequenceNo', 'patternRef', 'xCoord', 'sectorID']
    event_sectors = [header]


    query = "SELECT collectionref, sequenceNo, patternRef, xCoord FROM %s WHERE patternRef = %s" %(event_table, pattern_no)
    curr.execute(query)
    for row in curr:
        print(row)

    return

