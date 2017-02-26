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
    pattern_sectors = get_pattern_sectors(pattern_ref)

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
        for sector in pattern_sectors:
            #  Count up sectors till coordinates match.
            if row[3] > (sector[0] - tolerance_radius):
                sector_count += 1
        temp_event = EventCollection(row[0], row[1], row[2], event_type, sector_count)
        event_sectors.append(temp_event)

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
        collection_data.append(IndividualCollection(row[0], row[1], row[2], row[3], row[4], row[5]))
    return collection_data


def add_events_to_collections(collection_list: list, event_list: list):
    for col in collection_list:
        for event_type in event_list:
            for event in event_type:
                col.add_event(event)
    return