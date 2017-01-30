import csv
from University.event_extraction import *


def write_to_csv(file_name:str, collection:list):
    with open(file_name, 'w', newline='\n') as csvFile:
        cWriter = csv.writer(csvFile)
        # cWriter.writerow([1, 2, 3, 4, 5, 6, 7])
        for row in collection:
            number_list = [''] * 8
            for val in row[6]:
                number_list[val[0] - 1] = val[1]
            cWriter.writerow(number_list)
    csvFile.close()
    return


def append_invalid_sector_ids(pattern_collection, pattern_events):
    for collRow in pattern_collection:
        bad_sectors = []
        #  For each type of event.
        for collection in pattern_events:
            #  For each event.
            for event in collection:
                #  If event occurred in the current collection.
                if event[0] == collRow[1] and event[1] == collRow[2] and event[2] == collRow[3]:
                    #  Add event sector location to list.
                    bad_sectors.append(event[4])
        # Sort list of invalid sectors.
        bad_sectors = set(bad_sectors)
        bad_sectors = list(bad_sectors)
        bad_sectors.sort()
        #  Append invalid sectors to current collection.
        collRow.append(bad_sectors)
    return


def invalid_to_valid(collection_data: list):
    sector_count = 5 + collection_data[3]
    valid_sectors = []
    for i in range(1, sector_count):
        if i not in collection_data[6]:
            valid_sectors.append(i)
    collection_data[6] = valid_sectors
    return


event_tables = ["liftdetails", "stasisdetails"]
list_headers = ["IndividualID", "CollectionRef", "SequenceRef", "PatternRef", "DominantHand", "DyslexiaStatus", "Sectors"]

pattern_3_event_sectors, pattern_4_event_sectors = [], []

for table in event_tables:
    pattern_3_event_sectors.append(get_event_sectors(3, table))
    pattern_4_event_sectors.append(get_event_sectors(4, table))

pattern_3_d_dom = get_collection_data(3, 'Y', 'D')
pattern_3_d_non = get_collection_data(3, 'N', 'D')
pattern_4_d_dom = get_collection_data(4, 'Y', 'D')
pattern_4_d_non = get_collection_data(4, 'N', 'D')

pattern_3_nd_dom = get_collection_data(3, 'Y', 'ND')
pattern_3_nd_non = get_collection_data(3, 'N', 'ND')
pattern_4_nd_dom = get_collection_data(4, 'Y', 'ND')
pattern_4_nd_non = get_collection_data(4, 'N', 'ND')

append_invalid_sector_ids(pattern_4_d_dom, pattern_3_event_sectors)
append_invalid_sector_ids(pattern_4_nd_dom, pattern_3_event_sectors)


for row in pattern_4_d_dom:
    invalid_to_valid(row)
    get_valid_sectors(row)

for row in pattern_4_nd_dom:
    invalid_to_valid(row)
    get_valid_sectors(row)

write_to_csv("pattern_4_d_dom.csv", pattern_4_d_dom)
write_to_csv("pattern_4_nd_dom.csv", pattern_4_nd_dom)

close_connection()
