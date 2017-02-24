from University.collection import IndividualCollection
from University.data_extraction_v2 import *

event_tables = ["fittsliftlocations", "fittslooplocations", "fittsstasislocations"]

col = IndividualCollection(10000001, 1001, 3, 3, 'Y', 'D')

pattern_3_events = []

for event in EventType:
    print(event)
    print(event.value)
    print(event_tables[event.value])
    pattern_3_events.append(get_event_sectors(3, event_tables[event.value], event))

pattern_3_events[0][0].to_string()

count = 0

for event_type in pattern_3_events:
    for event in event_type:
        col.append_event(event)
    count += 1

print(col.to_string())
print(col.get_error_count())