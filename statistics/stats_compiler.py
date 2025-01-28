import json
import numpy as np
import os
from datetime import datetime
import re



#File to save the statistics about generated essays
write_file = "stats.txt"
#Directory that contains all of the json essays sets
data_path = "data/"

essay_sets = os.listdir(data_path)

def length_stats(json_object, set_title):
    word_counts = []
    sent_ct = []
    num_essays = len(json_object.values())
   # print(raw)
    for e in json_object.values():
        word_counts.append(len(e.split(" ")))
        sent_ct.append(len([s for s in re.split(r"[.?!]", e) if s.strip()]))
   # print(word_counts)
    avg_word_count = np.mean(word_counts).round(2)
    std_dev_word_count = np.std(word_counts).round(2)
   # print(avg_word_count, std_dev_word_count)
    avg_sent = np.mean(sent_ct).round(2)

    stat_string = f"{set_title}: Num Essays = {num_essays}; Average Word Count = {avg_word_count}; Std Word Count = {std_dev_word_count}; Average Sentence Count: {avg_sent} \n"
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
        outfile.write(f"Total Number of Essays: {total_num} \n")
        outfile.write(f"Compiled at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} \n")
        for i in stat_coll:
            outfile.write(i)

if __name__=="__main__":
    compile_stats()

