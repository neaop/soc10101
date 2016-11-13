from DataExtraction.event_sectors import *


def invalid_to_valid(collection_data: list):
    sector_count = 5 + collection_data[2]
    valid_sectors = []
    for i in range(1, sector_count):
        if i not in collection_data[4]:
            valid_sectors.append(i)
    collection_data.append(valid_sectors)
    return


def append_fitts_ip(collection_data: list):
    fitts_ip = []
    for val in collection_data[5]:
        sector_id = pattern_4_sector_ID[val[0] - 1][1]
        sector_time = val[1] / 1000

        fitts_ip.append([val[0], sector_id / sector_time])
    collection_data.append(fitts_ip)


def append_invalid_sector_ids(pattern_collection, pattern_events):
    for collRow in pattern_collection:
        bad_sectors = []
        #  For each type of event.
        for collection in pattern_events:
            #  For each event.
            for event in collection:
                #  If event occurred in the current collection.
                if event[0] == collRow[0] and event[1] == collRow[1] and event[2] == collRow[2]:
                    #  Add event sector location to list.
                    bad_sectors.append(event[4])
        # Sort list of invalid sectors.
        bad_sectors = set(bad_sectors)
        bad_sectors = list(bad_sectors)
        bad_sectors.sort()
        #  Append invalid sectors to current collection.
        collRow.append(bad_sectors)
    return


tables = ["fittslooplocations", "fittsstasislocations", "fittsliftlocations"]
collection_columns = ['idCollection', 'sequenceNo', 'patternRef', 'ageGroupRef', 'invalidSectors', 'validSectors/times', 'sector/IP']
pattern_3_event_sectors = []
pattern_4_event_sectors = []

#  Fill lists with invalid sectors.
for table in tables:
    pattern_3_event_sectors.append(get_event_sectors(table, 3))
    pattern_4_event_sectors.append(get_event_sectors(table, 4))

#  Get all the data from each collection for each pattern.
pattern_3_collection_data = get_collection_data(3)
pattern_4_collection_data = get_collection_data(4)

pattern_3_sector_ID = get_sector_difficulties(3)
pattern_4_sector_ID = get_sector_difficulties(4)

append_invalid_sector_ids(pattern_3_collection_data, pattern_3_event_sectors)
append_invalid_sector_ids(pattern_4_collection_data, pattern_4_event_sectors)

print(collection_columns)

for val in pattern_3_collection_data:
    invalid_to_valid(val)
    get_valid_sectors(val)
    append_fitts_ip(val)
    print(val)

close_connection()
