import os
import csv
from UniversityData.data_extraction import *

base_header = ["individual_id", "collection_id", "sequence_id", "pattern_id"]
sector_header = ["dominant_hand", "dyslexia_status", "sector_1", "sector_2",
                 "sector_3", "sector_4", "sector_5", "sector_6", "sector_7", "sector_8", "first_sector_error",
                 "total_sad"]
event_header = ["event_type", "sector_location", "details"]


def mk_dir(dir_path):
    # Output file directory.
    dir_path = dir_path
    # If output dir doesn't exist - create it.
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
    return


def event_dump(data_lists):
    dir_path = "..\data"
    mk_dir(dir_path)
    # Create new csv file.
    csv_name = "events.csv"
    with open(dir_path + '\\' + csv_name, 'w', newline='\n') as csvFile:
        c_writer = csv.writer(csvFile)
        header = list(base_header) + event_header
        c_writer.writerow(header)
        for patt in data_lists:
            for ind in patt:
                for seq in ind:
                    for e in seq.events:
                        row = [seq.individual_id, seq.collection_ref, seq.sequence_ref, seq.pattern_ref]
                        row.extend([e.event_type.name, e.sector, e.additional])
                        c_writer.writerow(row)
    csvFile.close()
    return


def sector_dump(data_lists):
    # Output file directory.
    dir_path = "..\data"
    mk_dir(dir_path)
    # Create new csv file.
    csv_name = "sectors.csv"
    with open(dir_path + '\\' + csv_name, 'w', newline='\n') as csvFile:
        c_writer = csv.writer(csvFile)
        header = list(base_header)+sector_header
        c_writer.writerow(header)
        for patt in data_lists:
            for ind in patt:
                for seq in ind:
                    row = [seq.individual_id, seq.collection_ref, seq.sequence_ref, seq.pattern_ref, seq.dominant_hand,
                           seq.dyslexia_status]
                    row.extend(seq.sector_times)
                    if seq.pattern_ref == 3:
                        row.extend("-")
                    row.extend([seq.first_error, seq.total_sad])
                    c_writer.writerow(row)
    csvFile.close()
    event_dump(data_lists)
    return
