from University.extraction_facade import *

pattern_3_data = pattern_facade(3, False)
pattern_4_data = pattern_facade(4, False)

write_data("d_dom_3_all_times.csv", pattern_3_data[0])
write_data("d_non_3_all_times.csv", pattern_3_data[1])
write_data("d_dom_4_all_times.csv", pattern_4_data[0])
write_data("d_non_4_all_times.csv", pattern_4_data[1])
write_data("n_dom_3_all_times.csv", pattern_3_data[2])
write_data("n_non_3_all_times.csv", pattern_3_data[3])
write_data("n_dom_4_all_times.csv", pattern_4_data[2])
write_data("n_non_4_all_times.csv", pattern_4_data[3])
# write("p_dom_3_all_times.csv", pattern_3_data[4])
# write("p_dom_4_all_times.csv", pattern_4_data[4])
