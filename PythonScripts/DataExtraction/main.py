from DataExtraction.event_sectors import *

tables = ["fittslooplocations", "fittsstasislocations", "fittsliftlocations"]
event_columns = ['collectionref', 'sequenceNo', 'patternRef', 'xCoord', 'sectorID']
collection_columns = ['idCollection', 'sequenceNo', 'patternref', 'agegroupref']
pattern_3_event_sectors = []
pattern_4_event_sectors = []

for table in tables:
    pattern_3_event_sectors.append(get_event_sectors(table, 3))
for table in tables:
    pattern_4_event_sectors.append(get_event_sectors(table, 4))

pattern_3_collection_data = get_collection_data(3)
pattern_4_collection_data = get_collection_data(4)

for collRow in pattern_3_collection_data:
    for collection in pattern_3_event_sectors:
        for event in collection:
            if event[0] == collRow[0] and event[1] == collRow[1] and event[2] == collRow[2]:
                collRow.append(event[4])

for val in pattern_3_collection_data:
    print(val)


close_connection()
