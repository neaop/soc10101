import os
import csv

from University.data_extraction import *


def write(file_name, data_list):
    dir_path = "..\data"
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    with open(dir_path + '\\' + file_name, 'w', newline='\n') as csvFile:
        c_writer = csv.writer(csvFile)

        for seq in data_list:
            temp = []
            for i in range(1, seq.number_of_sectors + 1):
                if i in seq.valid_sectors:
                    temp.append(i)
                else:
                    temp.append('')
            c_writer.writerow(temp)
    csvFile.close()
    return


def pattern_facade(pattern_ref: int, invalid_sectors: bool):
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
            if invalid_sectors:
                sequence.get_invalid_sectors()
            sequence.get_valid_sectors()
            get_sector_times(sequence)
            sequence.calculate_sector_ips(pattern_sector_ids)
            get_sequence_sad(sequence)
    return pattern_data


pattern_3_data = pattern_facade(3, True)

pattern_4_data = pattern_facade(4, True)

write("d_ndom_3_com.csv", pattern_3_data[1])
write("d_ndom_4_com.csv", pattern_4_data[1])
write("n_ndom_3_com.csv", pattern_3_data[3])
write("n_ndom_4_com.csv", pattern_4_data[3])
