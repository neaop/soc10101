from DataExtraction.event_sectors import get_event_sectors

tables = ["fittslooplocations", "fittsstasislocations", "fittsliftlocations"]
patterns = [3, 4]
event_sectors = []
for table in tables:
    for pattern in patterns:
       event_sectors.append(get_event_sectors(table, pattern))

for val in event_sectors:
    print(val[0])
    print(val[1])
    print(val[2])
