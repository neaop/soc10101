# Class for extraction of data from MySQL database tables.
import pymysql
import math
from University.collection import *

# Connection information.
con = pymysql.connect(host='localhost', port=3306, user='candidwebuser', passwd='pw4candid', db='fittsdb')
curr = con.cursor()

# Radius of target.
tolerance_radius = 10


# Returns a list of all the X coordinates of sectors in a pattern.
def get_pattern_sectors(pattern_ref: int):
    # Retrive X coordinates for passed pattern.
    curr.execute("SELECT patternX "
                 "FROM fittssectorid "
                 "WHERE patternRef = {0}".format(pattern_ref))
    pattern_sectors = []

    for row in curr:
        # Append coordinates to list.
        pattern_sectors.append(list(row))
    return pattern_sectors


# Returns the sectors of a pattern in which an error event occurred.
def get_event_sectors(pattern_ref: int, event_table: str, event_type: EventType):
    # Get sector coordinates.
    pattern_sectors = get_pattern_sectors(pattern_ref)
    # Retrieve error event details.
    query = ("SELECT cp.collectionRef, cp.sequenceNo, cp.patternRef, {0}.xCoord "
             "FROM {0} "
             "JOIN collectionpattern cp "
             "ON {0}.collectionRef = cp.collectionRef "
             "AND {0}.sequenceNo = cp.sequenceNo "
             "WHERE cp.patternRef = {1}".format(event_table, pattern_ref))
    curr.execute(query)

    event_sectors = []
    for row in curr:
        sector_count = 1
        # Iterate over sectors in pattern.
        for sector in pattern_sectors:
            #  Determine if error event occurred in current sector.
            if row[3] > (sector[0] - tolerance_radius):
                sector_count += 1
        # Create dedicated event object.
        temp_event = EventCollection(row[0], row[1], row[2], event_type, sector_count)
        event_sectors.append(temp_event)
    # Return events.
    return event_sectors


# Return all collection data for individual group - dyslexic, dominant-hand, etc.
def get_collection_data(pattern_ref: int, dominant_hand: str, dyslexia_status: str):
    collection_data = []
    # Retrieve demographic data.
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

    # Iterate over data and create objects.
    for row in curr:
        collection_data.append(SequenceCollection(row[0], row[1], row[2], row[3], row[4], row[5]))
    return collection_data


# Append events to relevant collection.
def add_events_to_collections(collection_list: list, event_list: list):
    for col in collection_list:
        for event_type in event_list:
            for event in event_type:
                col.add_event(event)
    return


# Return the movement times for a specific sequence.
def get_sector_times(collection_data: SequenceCollection):
    # Retrieve timings for sequence.
    curr.execute("SELECT startTime, point0, point1, point2, point3, point4, point5, point6, point7, point8 "
                 "FROM detailedtiming dt "
                 "JOIN collectionpattern cp "
                 "ON dt.collectionRef = cp.collectionRef "
                 "AND dt.sequenceNo = cp.sequenceNo "
                 "WHERE cp.collectionRef = {0} "
                 "AND cp.sequenceNo = {1}".format(collection_data.collection_ref, collection_data.sequence_ref))

    sector_times = []
    for row in curr:
        # Reverse order timings.
        backwards = row[::-1]
        for i in range(8):
            # Skip empty time - pattern 3.
            if backwards[i] is None:
                pass
            else:
                # Append time to list
                temp = backwards[i] - backwards[i + 1]
                sector_times.append(temp)
    # Reorder list.
    collection_data.sector_times = sector_times[::-1]
    # Update object variable.
    collection_data.total_time = sum(sector_times)


# Calculate the Index of Difficulty for each sector in a pattern.
def get_sector_difficulties(pattern_ref: int):
    start = [0, 100]
    sector_points = [start]
    sector_difficulties = []
    curr.execute("SELECT sectorNo, patternX, patternY "
                 "FROM fittssectorid "
                 "WHERE patternRef = {0}".format(pattern_ref))

    for row in curr:
        sector_points.append([row[1], row[2]])

    for i in range(0, len(sector_points) - 1):
        sector_distance = math.hypot(sector_points[i + 1][0] - sector_points[i][0],
                                     sector_points[i + 1][1] - sector_points[i][1])

        sector_difficulties.append(math.log2((2 * sector_distance) / (2 * tolerance_radius)))

    return sector_difficulties


# Return SAD for a sequence.
def get_sequence_sad(sequence_data: SequenceCollection):
    curr.execute("SELECT FSStdErr, TotalSAD "
                 "FROM collectionpattern "
                 "WHERE collectionRef = {0} "
                 "AND sequenceNo = {1}".format(sequence_data.collection_ref, sequence_data.sequence_ref))
    for row in curr:
        sequence_data.total_sad = row[1]
    return
