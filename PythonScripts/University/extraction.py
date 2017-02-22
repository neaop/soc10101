import csv
from University.data_extraction import *


def write_to_csv(file_name: str, collection: list):
    with open(file_name, 'w', newline='\n') as csvFile:
        c_writer = csv.writer(csvFile)
        csv_title = []
        sector_no = 7
        if collection[0][3] == 4:
            sector_no = 8
        for i in range(sector_no):
            csv_title.append(i)
        csv_title.extend(["TotalTime", "AverageTime"])
        c_writer.writerow(csv_title)
        for per in collection:
            number_list = [''] * sector_no
            for val in per[8]:
                number_list[val[0] - 1] = val[1]
            number_list.append(per[9])
            number_list.append(int(per[9])/int(sector_no))
            c_writer.writerow(number_list)

    csvFile.close()

    return


def main():
    event_tables = ["fittsliftlocations", "fittslooplocations", "fittsstasislocations"]
    list_headers = ["IndividualID", "CollectionRef", "SequenceRef", "PatternRef", "DominantHand", "DyslexiaStatus"]

    pattern_3_event_sectors, pattern_4_event_sectors = [], []

    for table in event_tables:
        pattern_3_event_sectors.append(get_event_sectors(3, table))
        pattern_4_event_sectors.append(get_event_sectors(4, table))

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
        get_invalid_sector_ids(coll, pattern_3_event_sectors)
    for coll in pattern_4:
        get_invalid_sector_ids(coll, pattern_4_event_sectors)

    # get_invalid_sector_ids(pattern_4_d_dom, pattern_4_event_sectors)
    # get_invalid_sector_ids(pattern_4_nd_dom, pattern_4_event_sectors)

    list_headers.append("validSectors")
    list_headers.append("validSectorTimes")
    list_headers.append("totalTime")

    for coll in pattern_3:
        for row in coll:
            invalid_to_valid(row)
            get_valid_sector_times(row)
            get_total_time(row)

    for coll in pattern_4:
        for row in coll:
            invalid_to_valid(row)
            get_valid_sector_times(row)
            get_total_time(row)

    # for row in pattern_4_d_dom:
    #     invalid_to_valid(row)
    #     get_valid_sector_times(row)
    #     get_total_time(row)
    #
    # for row in pattern_4_nd_dom:
    #     invalid_to_valid(row)
    #     get_valid_sector_times(row)
    #     get_total_time(row)

    write_to_csv("pattern_3_d_dom.csv", pattern_3_d_dom)
    write_to_csv("pattern_3_nd_dom.csv", pattern_3_nd_dom)

    close_connection()

if __name__ == '__main__':
    main()