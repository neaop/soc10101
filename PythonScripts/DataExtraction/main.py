from DataExtraction.eventSecotrs import get_event_sectors

table = "fittslooplocations"

loop_sectors = get_event_sectors(table, 3)
for val in loop_sectors:
    print(val)

