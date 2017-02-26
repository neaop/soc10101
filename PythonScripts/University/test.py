from University.data_extraction_v2 import *

event_tables = ["fittsliftlocations", "fittslooplocations", "fittsstasislocations"]

pat_3_dom_d = get_collection_data(3, 'Y', 'D')
pat_3_non_d = get_collection_data(3, 'N', 'D')
pat_3_dom_n = get_collection_data(3, 'Y', 'ND')
pat_3_non_n = get_collection_data(3, 'N', 'ND')
pattern_3_data = [pat_3_dom_d, pat_3_non_d, pat_3_dom_n, pat_3_non_n]

pat_4_dom_d = get_collection_data(4, 'Y', 'D')
pat_4_non_d = get_collection_data(4, 'N', 'D')
pat_4_dom_n = get_collection_data(4, 'Y', 'ND')
pat_4_non_n = get_collection_data(4, 'N', 'ND')
pattern_4_data = [pat_4_dom_d, pat_4_non_d, pat_4_dom_n, pat_4_non_n]

pattern_3_events = []
pattern_4_events = []

for event in EventType:
    pattern_3_events.append(get_event_sectors(3, event_tables[event.value], event))
    pattern_4_events.append(get_event_sectors(4, event_tables[event.value], event))

for col in pattern_3_data:
    add_events_to_collections(col, pattern_3_events)

for col in pattern_4_data:
    add_events_to_collections(col, pattern_4_events)

for x in pat_3_dom_d:
        print(x)
        print(x.get_invalid_sectors())
        print(x.get_error_count())
