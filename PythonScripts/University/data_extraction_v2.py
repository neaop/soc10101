import pymysql
import math
from University.collection import *

con = pymysql.connect(host='localhost', port=3306, user='candidwebuser', passwd='pw4candid', db='fittsdb')
curr = con.cursor()

tolerance_radius = 10


def get_pattern_sectors(pattern_ref: int):
    curr.execute("SELECT patternX "
                 "FROM fittssectorid "
                 "WHERE patternRef = {0}".format(pattern_ref))
    pattern_sectors = []
    for row in curr:
        pattern_sectors.append(list(row))
    return pattern_sectors


def get_event_sectors(pattern_ref: int, event_table: str, event_type: EventType):
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
        # temp_row = list(row)
        temp_event = EventCollection(row[0], row[1], row[2], event_type, sector_count)
        # temp_row.append(sector_count)
        event_sectors.append(temp_event)

    return event_sectors
