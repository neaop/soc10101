#  Class for extracting data formDatabase.
import pymysql
import math

con = pymysql.connect(host='localhost', port=3306, user='root', passwd='admin', db='schoolsv6')
curr = con.cursor()


#  Returns a list of sectors with events for a  pattern, from a table.
def get_event_sectors(event_table, pattern_no):
    tolerance = 10
    event_sectors = []
    pattern_sectors = get_pattern_sectors(pattern_no)

    query = "SELECT collectionref, sequenceNo, patternRef, xCoord FROM %s WHERE patternRef = %s" \
            % (event_table, pattern_no)
    curr.execute(query)

    for row in curr:
        sector_count = 1
        for sector in pattern_sectors:
            #  Count up sectors till coordinates match.
            if row[3] > (sector[0] - tolerance):
                sector_count += 1
        temp_row = list(row)
        temp_row.append(sector_count)
        event_sectors.append(temp_row)

    return event_sectors


#  Returns all the collections from a particular pattern.
def get_collection_data(pattern: int):
    collection_data = []
    curr.execute("SELECT idCollection, sequenceNo, patternref, agegroupref FROM fittssectortimes WHERE patternref = %s"
                 , pattern)
    for row in curr:
        collection_data.append(list(row))

    return collection_data


#  Returns a list of coordinates for a particular pattern.
def get_pattern_sectors(pattern_no):
    curr.execute("SELECT patternX FROM fittssectorid WHERE patternRef = %s", pattern_no)
    pattern_sectors = []
    for row in curr:
        pattern_sectors.append(list(row))
    return pattern_sectors


#  Returns a list of the valid sector completion times
def get_valid_sectors(collection_data: list):
    curr.execute("SELECT sector1, sector2, sector3, sector4, sector5, sector6, sector7, sector8 FROM fittssectortimes WHERE idCollection = %s AND sequenceNo = %s", (collection_data[0], collection_data[1]))
    sector_times =[]
    count = 1
    for row in curr:
        for val in row:
            if count in collection_data[5]:
                temp = [count, val]
                sector_times.append(temp)
            count += 1

        collection_data[5] = sector_times


#  Returns a list with the fitts's IDs for a particular pattern.
def get_sector_difficulties(pattern: int):
    start = [0, 100]
    sector_points = [start]
    sector_difficulties = []
    curr.execute("SELECT sectorNo, patternX, patternY FROM fittssectorid WHERE patternRef = %s ", pattern)
    for row in curr:
        sector_points.append([row[1], row[2]])

    # for val in sector_points:
    #     print(val)

    for i in range(0, len(sector_points)-1):
        sector_distance = math.hypot(sector_points[i+1][0] - sector_points[i][0], sector_points[i+1][1] - sector_points[i][1])
        sector_difficulties.append([i+1, math.log2((2*sector_distance) / 20)])

    return sector_difficulties


#  Closes the database connection.
def close_connection():
    curr.close()
    con.close()
    print("\nDatabase connection closed.")
    return
