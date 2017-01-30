from University.event_extraction import *


def append_invalid_sector_ids(pattern_collection, pattern_events):
    for collRow in pattern_collection:
        bad_sectors = []
        #  For each type of event.
        for collection in pattern_events:
            #  For each event.
            for event in collection:
                #  If event occurred in the current collection.
                if event[0] == collRow[0] and event[1] == collRow[1] and event[3] == collRow[3]:
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
        if i not in collection_data[4]:
            valid_sectors.append(i)
    collection_data[4] = valid_sectors
    return


eventTables = ["liftdetails", "stasisdetails"]

pattern_3_event_sectors, pattern_4_event_sectors = [], []

for table in eventTables:
    pattern_3_event_sectors.append(get_event_sectors(3, table))
    pattern_4_event_sectors.append(get_event_sectors(4, table))

pattern_3_dom = get_collection_data(3, 'Y')
pattern_3_non = get_collection_data(3, 'N')
pattern_4_dom = get_collection_data(4, 'Y')
pattern_4_non = get_collection_data(4, 'N')

append_invalid_sector_ids(pattern_3_dom, pattern_3_event_sectors)
append_invalid_sector_ids(pattern_3_non, pattern_3_event_sectors)
append_invalid_sector_ids(pattern_4_dom, pattern_4_event_sectors)
append_invalid_sector_ids(pattern_4_non, pattern_4_event_sectors)

for row in pattern_3_dom:
    invalid_to_valid(row)
    get_valid_sectors(row)
    print(row)

for row in pattern_4_dom:
    invalid_to_valid(row)
    get_valid_sectors(row)
    print(row)


close_connection()
