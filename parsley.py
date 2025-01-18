import json
import numpy as np
import os

write_file = "stats.txt"
data_path = "data/"

essay_sets = os.listdir(data_path)

def length_stats(json_object, set_title):
    word_counts = []
    num_essays = len(json_object.values())
   # print(raw)
    for e in json_object.values():
        word_counts.append(len(e.split(" ")))
   # print(word_counts)
    avg_word_count = np.mean(word_counts).round(2)
    std_dev_word_count = np.std(word_counts).round(2)
   # print(avg_word_count, std_dev_word_count)

    stat_string = f"{set_title}: Num Essays = {num_essays}; Average Word Count = {avg_word_count}; Std Word Count = {std_dev_word_count} \n"
    return stat_string, num_essays

def compile_stats():
    stat_coll = []
    total_num = 0
    for json_file in essay_sets:
        with open(data_path+json_file, "r") as curr_set:
            raw = json.load(curr_set)
            stats, num_essays = length_stats(raw, json_file)
            stat_coll.append(stats)
            total_num += num_essays
    with open(write_file, "w") as outfile:
        outfile.write(f"Total Number of Essays: {total_num}\n")
        for i in stat_coll:
            outfile.write(i)
compile_stats()

