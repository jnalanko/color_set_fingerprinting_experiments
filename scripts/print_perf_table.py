#!/usr/bin/env python3
import sys
import re
import os

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

def print_as_latex_table(rows):
    # Human-readable column names
    columns = [
        "dataset",
        "themisto_d10000-time",
        "themisto_d10000-mem",
        "themisto_to_disk_d10000-time",
        "themisto_to_disk_d10000-mem",
        "themisto_d10000-colors_on_disk",
        "bifrost-time",
        "bifrost-mem",
        "bifrost-colors_on_disk",
        "ggcat-time",
        "ggcat-mem",
        "ggcat-colors_on_disk",
    ]

    #header = " & ".join("\\makecell[l]{" + label + "}" for _, label in columns) + r" \\"
    header_row1 = "\multicolumn{1}{|c}{} & \multicolumn{5}{|c}{Our method} & \multicolumn{3}{|c}{Bifrost} & \multicolumn{3}{|c|}{GGCAT 2} \\\\"
    header_row2 = "\multicolumn{1}{|l}{Dataset} & \multicolumn{1}{|l}{Time} & \multicolumn{1}{c}{Mem} & \multicolumn{1}{l}{Time} & \multicolumn{1}{c}{Mem} & \multicolumn{1}{l}{Final} & \multicolumn{1}{|c}{Time} & \multicolumn{1}{c}{Mem} & \multicolumn{1}{l}{Final} & \multicolumn{1}{|c}{Time} & \multicolumn{1}{l}{Mem} & \multicolumn{1}{l|}{Final} \\\\"
    header_row3 = "\multicolumn{1}{|l}{} & \multicolumn{1}{|l}{} & \multicolumn{1}{c}{} & \multicolumn{1}{l}{(8 pcs)} & \multicolumn{1}{c}{(8 pcs)} & \multicolumn{1}{l}{disk} & \multicolumn{1}{|c}{} & \multicolumn{1}{c}{} & \multicolumn{1}{l}{disk} & \multicolumn{1}{|c}{} & \multicolumn{1}{l}{} & \multicolumn{1}{l|}{disk} \\\\"

    header = header_row1 + "\n" + header_row2 + "\n" + header_row3 + "\n"

    def fmt(v):
        if isinstance(v, int):
            return f"{v:,}"
        if isinstance(v, float):
            return f"{v:.2f}"
        return str(v)

    rows_tex = []
    for row in rows:
        min_mem = 10**100
        min_time= 10**100
        min_disk= 10**100
        for col in columns:
            if col.endswith("-mem"):
                min_mem = min(row[col], min_mem)
            if col.endswith("-time"):
                min_time = min(row[col], min_time)
            if col.endswith("-disk"):
                min_disk = min(row[col], min_disk)

        row_tex_cells = []
        for col in columns:
            if col.endswith("-mem") and row[col] == min_mem or col.endswith("-time") and row[col] == min_time or col.endswith("-colors_on_disk") and row[col] == min_disk:
                row_tex_cells.append("\\textbf{" + fmt(row[col]) + "}")
            else:
                row_tex_cells.append(fmt(row[col]))
        row_tex = " & ".join(row_tex_cells) + r" \\"
        rows_tex.append(row_tex)

    #rows_tex = [
    #    " & ".join(fmt(row[k]) for k, _ in columns) + r" \\"
    #    for row in rows
    #]

    # Narrow columns (tune widths as needed)
    colspec = (
        "|" + "l" + "r"*(len(columns)-1) + "|"
        #"c r{1.0cm} r{1.2cm} r{0.8cm} r{1.4cm} r{1.4cm} r{1.4cm} r{1.0cm} r{1.0cm} r{1.6cm} r{1.3cm}"
    )

    print("\n".join([
        rf"\begin{{tabular}}{{{colspec}}}",
        r"\hline",
        header,
        r"\hline",
        *rows_tex,
        r"\hline",
        r"\end{tabular}",
    ]))

def get_colors_on_disk_size(dataset, n, tool):
    size = 0
    if tool == "bifrost":
        return os.path.getsize(f"bifrost/{dataset}_{n}.fna.color.bfg")
    elif tool == "ggcat":
        return os.path.getsize(f"ggcat/{dataset}_{n}.colors.dat") 
    elif "themisto" in tool: # All Themisto variants give the same index
        size = 0
        size += os.path.getsize(f"themisto2_to_disk/{dataset}_{n}_d10000.thm2.dense") 
        size += os.path.getsize(f"themisto2_to_disk/{dataset}_{n}_d10000.thm2.sparse") 
        size += os.path.getsize(f"themisto2_to_disk/{dataset}_{n}_d10000.thm2.marks") 
        return size
    else:
        return 0 # Don't care
        


datasets = ["salmonella", "random"]
genome_count_lists = [[2**i for i in range(1,16+1)], [2**i for i in range(1,14+1)]]
tools= ["themisto", "themisto_d10000", "themisto_to_disk_d10000", "ggcat", "bifrost", "metagraph_1gb_anno"]
rows = []

print("\t".join(["tool", "dataset", "n_genomes", "time_seconds", "mem_bytes"]))
for dataset_idx, dataset in enumerate(datasets):
    for n in genome_count_lists[dataset_idx]:
        if n < 128: continue # Shorter table
        row = dict()
        dataset_id = dataset + "-" + str(n)
        row["dataset"] = dataset_id
        for tool in tools:
            log_filename = f"logs/{dataset}_{n}_{tool}.log"
            try:
                X = parse_time_output(open(log_filename).readlines())
                row[tool + "-time"] = X["elapsed_seconds"] / 60 # Minutes
                row[tool + "-mem"] = X["max_rss_bytes"] / 2**30 # Gigabytes
                row[tool + "-colors_on_disk"] = get_colors_on_disk_size(dataset, n, tool) / 2**30 # Gigabytes
                # TODO: size on disk
            except:
                print("Warning: could not parse", log_filename)
        rows.append(row)

print_as_latex_table(rows)


# Columns:
# (Dataset, Number of genomes)
# (Our time (to disk), Our mem (to disk), Our size on disk) 
# (Bifrost time, bifrost mem, bifrost size on disk)
# (GGCAT time, GGCAT mem, GGCAT size on disk)
# = 11 columns.

# Mention in text: time breakdown by phase on Salmonella 64k and Random 16k
# Maybe even: peak RAM breakdown by phase on Salmonella 64k and Random 16k
