import os
import csv

from University.data_extraction_v2 import *


def write(file_name, data_list):
    dir_path = "..\data"
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    with open(dir_path + '\\' + file_name, 'w', newline='\n') as csvFile:
        c_writer = csv.writer(csvFile)

        c_writer.writerow(["sad", "time"])
        for seq in data_list:
            temp = [seq.total_sad, seq.total_time]
            c_writer.writerow(temp)
    csvFile.close()
    return


def pattern_facade(pattern_ref: int):
    event_tables = ["fittsliftlocations", "fittslooplocations", "fittsstasislocations"]
    event_list = []
    for event_ in EventType:
        event_list.append(get_event_sectors(pattern_ref, event_tables[event_.value], event_))

    pattern_dom_d = get_collection_data(pattern_ref, 'Y', 'D')
    pattern_non_d = get_collection_data(pattern_ref, 'N', 'D')
    pattern_dom_n = get_collection_data(pattern_ref, 'Y', 'ND')
    pattern_non_n = get_collection_data(pattern_ref, 'N', 'ND')
    pattern_data = [pattern_dom_d, pattern_non_d, pattern_dom_n, pattern_non_n]

    pattern_sector_ids = get_sector_difficulties(pattern_ref)

    for sequence_list in pattern_data:
        add_events_to_collections(sequence_list, event_list)

        for sequence in sequence_list:
            sequence.get_invalid_sectors()
            get_sector_times(sequence)
            sequence.calculate_sector_ips(pattern_sector_ids)
            get_sequence_sad(sequence)
    return pattern_data


pattern_3_data = pattern_facade(3)

pattern_4_data = pattern_facade(4)

# write("d_3.csv", pattern_3_data[0])
# write("d_4.csv", pattern_4_data[0])
# write("n_3.csv", pattern_3_data[2])
# write("n_4.csv", pattern_4_data[2])


for sequence in pattern_3_data[0]:
    print(sequence.average_ip)

# event_tables = ["fittsliftlocations", "fittslooplocations", "fittsstasislocations"]
# pat_3_dom_d = get_collection_data(3, 'Y', 'D')
# pat_3_non_d = get_collection_data(3, 'N', 'D')
# pat_3_dom_n = get_collection_data(3, 'Y', 'ND')
# pat_3_non_n = get_collection_data(3, 'N', 'ND')
#
# pattern_3_data = [pat_3_dom_d, pat_3_non_d, pat_3_dom_n, pat_3_non_n]
# pat_4_dom_d = get_collection_data(4, 'Y', 'D')
# pat_4_non_d = get_collection_data(4, 'N', 'D')
# pat_4_dom_n = get_collection_data(4, 'Y', 'ND')
# pat_4_non_n = get_collection_data(4, 'N', 'ND')
#
# pattern_4_data = [pat_4_dom_d, pat_4_non_d, pat_4_dom_n, pat_4_non_n]
# pattern_3_events = []
#
# pattern_4_events = []
#
# for event in EventType:
#     pattern_3_events.append(get_event_sectors(3, event_tables[event.value], event))
#     pattern_4_events.append(get_event_sectors(4, event_tables[event.value], event))
#
# for col in pattern_3_data:
#     add_events_to_collections(col, pattern_3_events)
#
# for col in pattern_4_data:
#     add_events_to_collections(col, pattern_4_events)
# patter_3_sector_ids = get_sector_difficulties(3)
#
# # print(patter_3_sector_ids)
# # print(patter_4_sector_ids)
#
# patter_4_sector_ids = get_sector_difficulties(4)
#
# for x in pat_4_dom_d:
#     x.get_invalid_sectors()
#     x.get_error_count()
#     x.get_valid_sectors()
#     get_sector_times(x)
#     x.calculate_sector_ips(patter_4_sector_ids)
#     get_sequence_sad(x)
#     print(x)
#     print(x.sector_times)
#     print(x.total_time)
#     print(x.average_ip)
#     print(x.sector_ips)
#     print(x.total_time)
#     print(x.total_sad)
#     print(x.total_sad / x.total_time)
#     print("\n")
