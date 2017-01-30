import pymysql

con = pymysql.connect(host='localhost', port=3306, user='candidwebuser', passwd='pw4candid', db='fittsdb')
curr = con.cursor()


def get_event_sectors(pattern_ref: int, event_table: str):
    tolerance = 10
    event_sectors = []
    pattern_sector_coords = get_pattern_coords(pattern_ref)

    coord_name = "Xcoord" if event_table != "loopdetails" else "cogX"

    query = ("SELECT collectionpattern.collectionRef, collectionpattern.sequenceNo, {0}, collectionpattern.patternRef "
             "FROM {1} "
             "JOIN collectionpattern "
             "ON {1}.collectionRef = collectionpattern.collectionRef "
             "AND {1}.sequenceNo = collectionpattern.sequenceNo "
             "WHERE collectionpattern.patternRef = {2}".format(coord_name, event_table, pattern_ref))

    curr.execute(query)

    for row in curr:
        sector_count = 1
        for sector in pattern_sector_coords:
            #  Count up sectors till coordinates match.
            if row[2] > (sector[0] - tolerance):
                sector_count += 1
        temp_row = list(row)
        temp_row.append(sector_count)
        event_sectors.append(temp_row)

    return event_sectors


def get_collection_data(pattern_ref: int, dominant_hand: str):
    collection_data = []
    curr.execute("SELECT collectionpattern.collectionRef, collectionpattern.sequenceNo, dominant, patternRef "
                 "FROM detailedtiming "
                 "JOIN collectionpattern "
                 "ON detailedtiming.collectionRef = collectionpattern.collectionRef "
                 "AND detailedtiming.sequenceNo = collectionpattern.sequenceNo "
                 "WHERE patternRef = {0} "
                 "AND dominant = '{1}'".format(pattern_ref, dominant_hand))
    for row in curr:
        collection_data.append(list(row))

    return collection_data


def get_pattern_coords(pattern_ref: int):
    curr.execute("SELECT xValue FROM patternpoints WHERE patternRef = {0}".format(pattern_ref))
    pattern_sector_coords = []
    for row in curr:
        pattern_sector_coords.append(list(row))
    return pattern_sector_coords


def get_valid_sectors(collection_data: list):
    curr.execute("SELECT  point0, point1, point2, point3, point4, point5, point6, point7, point8 "
                 "FROM detailedtiming  "
                 "JOIN collectionpattern "
                 "ON detailedtiming.collectionRef = collectionpattern.collectionRef "
                 "AND detailedtiming.sequenceNo = collectionpattern.sequenceNo "
                 "WHERE collectionpattern.collectionRef = {0} "
                 "AND collectionpattern.sequenceNo = {1}".format(collection_data[0], collection_data[1]))
    sector_times = []
    count = 1
    for row in curr:
        for val in row:
            if count in collection_data[4]:
                temp = [count, val]
                sector_times.append(temp)
            count += 1

        collection_data[4] = sector_times


def close_connection():
    curr.close()
    con.close()
    print("\nDatabase connection closed.")
    return
