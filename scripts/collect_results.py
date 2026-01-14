#!/usr/bin/env python3
import sys
import re

def parse_time_output(lines):
    """
    Parse the output of /usr/bin/time -v.
    Returns a dict with 'elapsed_seconds' and 'max_rss_bytes'.
    """
    rss_re = re.compile(r"Maximum resident set size.*:\s*(\d+)")
    disk_re = re.compile(r"Temporary disk space peak: (\d+) bytes")

    elapsed_seconds = None
    max_rss_bytes = None
    disk_peak = 0

    for line in lines:
        # Match elapsed time — supports h:mm:ss, m:ss, or s.s formats
        if "Elapsed (wall clock) time" in line:
            # Two formats based on whether the time is more than a hour:
            # Elapsed (wall clock) time (h:mm:ss or m:ss): 1:13:01
            # Elapsed (wall clock) time (h:mm:ss or m:ss): 51:00.54
            s = line.split(" ")[-1].strip()
            if s.count(":") == 2: # h:mm:ss
                hours = int(s.split(":")[0])
                mins = int(s.split(":")[1])
                secs = int(s.split(":")[2])
                elapsed_seconds = hours * 60*60 + mins * 60 + secs
            else: # m:ss
                mins = int(s.split(":")[0])
                secs = float(s.split(":")[1])
                elapsed_seconds = mins * 60 + secs

        # Match max RSS (in kilobytes)
        elif "Maximum resident set size" in line:
            match = rss_re.search(line)
            if match:
                max_rss_bytes = int(match.group(1)) * 1024  # convert KB to bytes

        elif "Temporary disk space peak:" in line:
            match = disk_re.search(line)
            if match:
                disk_peak = int(match.group(1))

    return {"elapsed_seconds": elapsed_seconds, "max_rss_bytes": max_rss_bytes, "temp_disk": disk_peak}


datasets = ["salmonella", "random"]
genome_count_lists = [[2**i for i in range(1,16+1)], [2**i for i in range(1,14+1)]]
tools= ["themisto", "ggcat", "bifrost", "metagraph_anno"]

print("\t".join(["tool", "dataset", "n_genomes", "time_seconds", "mem_bytes"]))
for tool in tools:
    for dataset_idx, dataset in enumerate(datasets):
        for n in genome_count_lists[dataset_idx]:
            filename = f"logs/{dataset}_{n}_{tool}.log"
            try:
                res = parse_time_output(open(filename).readlines())
                print("{}\t{}\t{}\t{}\t{}".format(tool, dataset, n, res["elapsed_seconds"], res["max_rss_bytes"]))
            except:
                pass

# res = parse_time_output(open(indexing_filename).readlines()) 
