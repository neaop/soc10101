import pymysql
import math
from University.collection import IndividualCollection, EventType

con = pymysql.connect(host='localhost', port=3306, user='candidwebuser', passwd='pw4candid', db='fittsdb')
curr = con.cursor()

tolerance_radius = 10


def get_event_sectors(pattern_ref: int, event_table: str):
    event_sectors = []
    pattern_sector_coords = get_pattern_sectors(pattern_ref)
    query = ("SELECT cp.collectionRef, cp.sequenceNo, cp.patternRef, {0}.xCoord "
             "FROM {0} "
             "JOIN collectionpattern cp "
             "ON {0}.collectionRef = cp.collectionRef "
             "AND {0}.sequenceNo = cp.sequenceNo "
             "WHERE cp.patternRef = {1}".format(event_table, pattern_ref))

    curr.execute(query)

    for row in curr:
        sector_count = 1
        for sector in pattern_sector_coords:
            #  Count up sectors till coordinates match.
            if row[3] > (sector[0] - tolerance_radius):
                sector_count += 1
        temp_row = list(row)
        temp_row.append(sector_count)
        event_sectors.append(temp_row)

    return event_sectors


def get_collection_data(pattern_ref: int, dominant_hand: str, dyslexia_status: str):
    collection_data = []
    curr.execute("SELECT c.individualRef, cp.collectionRef, cp.sequenceNo, cp.patternRef, cp.dominant,  ds.status "
                 "FROM detailedtiming dt "
                 "JOIN collectionpattern cp "
                 "ON dt.collectionRef = cp.collectionRef "
                 "AND dt.sequenceNo = cp.sequenceNo "
                 "JOIN collection c "
                 "ON dt.collectionRef = c.idCollection "
                 "JOIN dyslexicstatus ds "
                 "on c.individualRef = ds.individualId "
                 "WHERE patternRef = {0} "
                 "AND dominant = '{1}' "
                 "AND status = '{2}' ".format(pattern_ref, dominant_hand, dyslexia_status))
    for row in curr:
        collection_data.append(list(row))

    return collection_data


def get_pattern_sectors(pattern_ref: int):
    curr.execute("SELECT patternX "
                 "FROM fittssectorid "
                 "WHERE patternRef = {0}".format(pattern_ref))
    pattern_sectors = []
    for row in curr:
        pattern_sectors.append(list(row))
    return pattern_sectors


def get_valid_sector_times(collection_data: list):
    curr.execute("SELECT startTime, point0, point1, point2, point3, point4, point5, point6, point7, point8 "
                 "FROM detailedtiming dt "
                 "JOIN collectionpattern cp "
                 "ON dt.collectionRef = cp.collectionRef "
                 "AND dt.sequenceNo = cp.sequenceNo "
                 "WHERE cp.collectionRef = {0} "
                 "AND cp.sequenceNo = {1}".format(collection_data[1], collection_data[2]))
    sector_times = []
    count = 1
    for row in curr:
        for val in row[1:]:
            if count in collection_data[7]:
                prev = row[count - 1]
                temp = [count, val-prev]
                sector_times.append(temp)
            count += 1

        collection_data.append(sector_times)


def get_total_time(collection_data: list):
    final_point = 'point8' if collection_data[3] == 4 else 'point7'

    curr.execute("SELECT startTime, {0} "
                 "FROM detailedtiming dt "
                 "JOIN collectionpattern cp "
                 "ON dt.collectionRef = cp.collectionRef "
                 "AND dt.sequenceNo = cp.sequenceNo "
                 "WHERE cp.collectionRef = {1} "
                 "AND cp.sequenceNo = {2}".format(final_point, collection_data[1], collection_data[2]))

    for row in curr:
        total_time = row[1] - row[0]
        collection_data.append(total_time)


def get_invalid_sector_numbers(pattern_collection: list, pattern_events: list):
    for collRow in pattern_collection:
        invalid_sectors = []
        #  For each type of event.
        for event_type in pattern_events:
            #  For each event.
            for event in event_type:
                #  If event occurred in the current collection.
                if event[0] == collRow[1] and event[1] == collRow[2] and event[2] == collRow[3]:
                    #  Add event sector location to list.
                    invalid_sectors.append(event[4])
        # Sort list of invalid sectors.
        error_count = len(invalid_sectors)
        invalid_sectors = set(invalid_sectors)
        invalid_sectors = list(invalid_sectors)
        invalid_sectors.sort()
        #  Append invalid sectors to current collection.
        collRow.append(invalid_sectors)
        # collRow.append(error_count)
    return


def obj_get_invalid_sectors(collection_list: list, event_list: list, event_type: EventType):
    for collection in collection_list:
        for event in event_list:
            if event[0] == collection.collection_ref \
                and event[1] == collection.sequence_ref \
                    and event[2] == collection.pattern_ref:
                collection.append_event(event, event_type)
    return


def invalid_to_valid(collection_data: list):
    sector_count = 5 + collection_data[3]
    valid_sectors = []
    for i in range(1, sector_count):
        if i not in collection_data[6]:
            valid_sectors.append(i)
    collection_data.append(valid_sectors)
    return


def get_sector_difficulties(pattern_ref: int):
    start = [0, 100]
    sector_points = [start]
    sector_difficulties = []
    curr.execute("SELECT sectorNo, patternX, patternY "
                 "FROM fittssectorid "
                 "WHERE patternRef = {0}".format(pattern_ref))

    for row in curr:
        sector_points.append([row[1], row[2]])

    for i in range(0, len(sector_points)-1):
        sector_distance = \
            math.hypot(sector_points[i+1][0] - sector_points[i][0], sector_points[i+1][1] - sector_points[i][1])

        sector_difficulties.append([i+1, math.log2((2 * sector_distance) / (2 * tolerance_radius))])

    return sector_difficulties


def calculate_ip(collection_data: list):
    sector_ip = []
    sector_ids = get_sector_difficulties(collection_data[3])
    for valid_sector in collection_data[8]:
        sec_id = sector_ids[valid_sector[0]-1][1]
        sector_time = valid_sector[1] / 1000
        sector_ip.append([valid_sector[0], sec_id / sector_time])

    collection_data.append(sector_ip)
    return


def close_connection():
    curr.close()
    con.close()
    print("\nDatabase connection closed.")
    return
