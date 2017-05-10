import os
import csv
from UniversityData.data_extraction import *


# Facade class to deal with extraction from database.
def pattern_facade(pattern_ref: int, invalid_sectors: bool):
    # Error event table names.
    event_list = []
    event_tables = ["fittsliftlocations", "fittslooplocations", "fittsstasislocations"]

    # For each type of event - loop, lift, stop.
    for e in EventType:
        # Extract and append events that occurred in this sequence.
        event_list.append(get_event_sectors(pattern_ref, event_tables[e.value], e))

    # Lists to retain data of different demographics.
    # Dyslexic
    pattern_dom_d = get_collection_data(pattern_ref, 'Y', 'D')
    pattern_non_d = get_collection_data(pattern_ref, 'N', 'D')
    # Non- dyslexic
    pattern_dom_n = get_collection_data(pattern_ref, 'Y', 'ND')
    pattern_non_n = get_collection_data(pattern_ref, 'N', 'ND')
    # Possibly dyslexic.
    pattern_dom_p = get_collection_data(pattern_ref, 'Y', 'PD')
    pattern_non_p = get_collection_data(pattern_ref, 'N', 'PD')
    # List of all demographics.
    pattern_data = [pattern_dom_d, pattern_non_d, pattern_dom_n, pattern_non_n, pattern_dom_p, pattern_non_p]

    # Get difficulty of all sectors in this pattern.
    pattern_sector_ids = get_sector_difficulties(pattern_ref)

    # For each individual sequence.
    for sequence_list in pattern_data:
        # Append relevant events to sequence.
        add_events_to_collections(sequence_list, event_list)

        for sequence in sequence_list:
            if invalid_sectors:
                # Calculate invalid sectors if needed.
                sequence.get_invalid_sectors()
            sequence.get_valid_sectors()
            get_sector_times(sequence)
            sequence.calculate_sector_ips(pattern_sector_ids)
            get_sequence_sad(sequence)

    # Return all sequence for a pattern.
    return pattern_data


# Method to write data to csv file.

def write_data(file_name, data_list):
    # Output file directory.
    dir_path = "..\data"
    # If output dir doesn't exist - create it.
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    # Create new csv file.
    with open(dir_path + '\\' + file_name, 'w', newline='\n') as csvFile:
        c_writer = csv.writer(csvFile)
        # For every sequence.
        for seq in data_list:
            # Append movement time to list.
            temp = seq.sector_times

            # Write list to csv.
            c_writer.writerow(temp)
    csvFile.close()
    return

    # write_data was rewritten depending on the data required
    # Below is a snippet that was used to write only valid sectors -
    # for seq in data_list:
    #     temp = []
    #     for i in range(1, seq.number_of_sectors + 1):
    #         if i in seq.valid_sectors:
    #             temp.append(i)
    #         else:
    #             temp.append('')
