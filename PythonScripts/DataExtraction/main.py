from DataExtraction.event_sectors import *


def invalid_to_valid(invalid_sectors: list, pattern: int):
    sector_count = 5 + pattern
    valid_sectors = []
    for i in range(1, sector_count):
        if i not in invalid_sectors:
            valid_sectors.append(i)
    return valid_sectors


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
collection_columns = ['idCollection', 'sequenceNo', 'patternRef', 'ageGroupRef', 'invalidSectors']
pattern_3_event_sectors = []
pattern_4_event_sectors = []

#  Fill lists with invalid sectors.
for table in tables:
    pattern_3_event_sectors.append(get_event_sectors(table, 3))
    pattern_4_event_sectors.append(get_event_sectors(table, 4))

#  Get all the data from each collection for each pattern.
pattern_3_collection_data = get_collection_data(3)
pattern_4_collection_data = get_collection_data(4)

append_invalid_sector_ids(pattern_3_collection_data, pattern_3_event_sectors)
append_invalid_sector_ids(pattern_4_collection_data, pattern_4_event_sectors)

# print(collection_columns)
# print(pattern_3_collection_data[0])
# print(invalid_to_valid(pattern_3_collection_data[0][4], 3))

print(collection_columns)
print(pattern_4_collection_data[0])
print(invalid_to_valid(pattern_4_collection_data[0][4], 3))

d = pattern_4_collection_data[0][0]
seq = pattern_4_collection_data[0][1]
valid = invalid_to_valid(pattern_4_collection_data[0][4], 3)

print(get_valid_sectors(d,seq,valid))

# print(collection_columns)
# for val in pattern_3_collection_data:
#     print(val)

print(get_sector_difficulty(4))

close_connection()
