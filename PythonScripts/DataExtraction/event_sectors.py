#  Class for extracting data formDatabase.
import pymysql

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
def get_collection_data(pattern):
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


def close_connection():
    curr.close()
    con.close()
    print("\nDatabase connection closed.")
    return
