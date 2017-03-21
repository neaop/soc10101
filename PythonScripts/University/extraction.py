import csv
import os
from University.data_extractionv2 import *


def write_to_csv(file_name: str, collection: list):
    dir_path = "..\data"
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    with open(dir_path + '\\' + file_name, 'w', newline='\n') as csvFile:
        c_writer = csv.writer(csvFile)
        csv_title = []
        sector_no = 7

        if collection[0][3] == 4:
            sector_no = 8
        for i in range(2):
            for i in range(sector_no):
                csv_title.append(i+1)

        csv_title.extend(["TotalTime", "AverageTime"])
        c_writer.writerow(csv_title)

        for per in collection:
            time_list = [''] * sector_no
            id_list = [''] * sector_no

            for val in per[8]:
                time_list[val[0] - 1] = val[1]

            for val in per[9]:
                id_list[val[0] - 1] = val[1]

            time_list.extend(id_list)
            time_list.append(per[10])
            time_list.append((int(per[10]) / int(sector_no)))
            c_writer.writerow(time_list)

    csvFile.close()

    return


def main():
    event_tables = ["fittsliftlocations", "fittslooplocations", "fittsstasislocations"]
    list_headers = ["IndividualID", "CollectionRef", "SequenceRef", "PatternRef", "DominantHand", "DyslexiaStatus"]

    pattern_3_event_sectors, pattern_4_event_sectors = [], []

    for table in event_tables:
        pattern_3_event_sectors.append(get_event_sectors(3, table))
        pattern_4_event_sectors.append(get_event_sectors(4, table))

    for coll in pattern_3_event_sectors:
        for row in coll:
            print(row)

    pattern_3_d_dom = get_collection_data(3, 'Y', 'D')
    pattern_3_d_non = get_collection_data(3, 'N', 'D')
    pattern_4_d_dom = get_collection_data(4, 'Y', 'D')
    pattern_4_d_non = get_collection_data(4, 'N', 'D')

    pattern_3_nd_dom = get_collection_data(3, 'Y', 'ND')
    pattern_3_nd_non = get_collection_data(3, 'N', 'ND')
    pattern_4_nd_dom = get_collection_data(4, 'Y', 'ND')
    pattern_4_nd_non = get_collection_data(4, 'N', 'ND')

    pattern_3 = [pattern_3_d_dom, pattern_3_d_non, pattern_3_nd_dom, pattern_3_nd_non]
    pattern_4 = [pattern_4_d_dom, pattern_4_d_non, pattern_4_nd_dom, pattern_4_nd_non]

    list_headers.append("invalidSectors")

    for coll in pattern_3:
        get_invalid_sector_numbers(coll, pattern_3_event_sectors)
    for coll in pattern_4:
        get_invalid_sector_numbers(coll, pattern_4_event_sectors)

    list_headers.append("validSectors")
    list_headers.append("validSectorTimes")
    list_headers.append("sectorIP")
    list_headers.append("totalTime")

    # print(list_headers)

    for coll in pattern_3:
        for row in coll:
            invalid_to_valid(row)
            get_valid_sector_times(row)
            calculate_ip(row)
            get_total_time(row)
            # print(row)

    for coll in pattern_4:
        for row in coll:
            invalid_to_valid(row)
            get_valid_sector_times(row)
            get_total_time(row)
            get_total_time(row)

    # write_to_csv("pattern_3_d_dom.csv", pattern_3_d_dom)
    # write_to_csv("pattern_3_nd_dom.csv", pattern_3_nd_dom)

    close_connection()


if __name__ == '__main__':
    main()
