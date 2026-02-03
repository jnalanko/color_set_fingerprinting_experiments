from datetime import datetime, timezone
import copy

# This will be needed for breaking down running time across phases
def seconds_since_2026_start(timestr: str) -> int:
    """
    Parse an ISO-8601 UTC timestamp like:
    2026-01-21T18:11:16Z

    Return seconds since 2026-01-01T00:00:00Z.
    """
    t = datetime.strptime(timestr, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    start_2026 = datetime(2026, 1, 1, tzinfo=timezone.utc)
    return int((t - start_2026).total_seconds())

def parse_log_file(filename):
    text = open(filename).read()
    n_sparse, n_dense = None, None
    for line in text.split("\n"):
        if "&n_sparse_sets" in line: 
            n_sparse = int(line.split(" ")[-1])
        if "&n_dense_sets" in line: 
            n_dense = int(line.split(" ")[-1])
    assert(n_sparse != None and n_dense != None)
    return {"num_sparse": n_sparse, "num_dense": n_dense}

def parse_stats_file(filename) -> dict:

    text = open(filename).read()
    stats = {}

    key_map = {
        "Number of k-mers": "num_kmers",
        "Number of colors": "num_colors",
        "SBWT length": "sbwt_len",
        "Number of distinct color sets": "num_color_sets",
        "Mean size of distinct color sets": "mean_color_set_size",
        "Mean k-mer color set size": "mean_kmer_color_set_size",
        "Fraction of key k-mers": "key_kmer_frac",
        "Number of forward unitigs (not bidirected)": "num_forward_unitigs",
        "Min unitig length": "min_unitig_len",
        "Max unitig length": "max_unitig_len",
        "Mean unitig length": "mean_unitig_len",
    }

    for line in text.strip().splitlines():
        if ':' not in line:
            continue

        key, value = line.split(':', 1)
        key = key_map[key.strip()]
        value = value.strip()

        # Try int, then float, else keep as string
        try:
            stats[key] = int(value)
        except ValueError:
            try:
                stats[key] = float(value)
            except ValueError:
                if "%" in value:
                    value = float(value.replace("%","")) / 100
                #value = value.replace("%", " \\%") # Escape percentage for latex and put a space
                stats[key] = value

    return stats

def format_latex_table(rows):

    # Human-readable column names: TODO: not used in code anymore?
    columns = [
        ("dataset", "Dataset"),
        ("num_kmers", "$k$-mers"),
        ("key_kmer_frac", r"Key $k$-mers fraction"),
        ("num_color_sets", "Distinct sets"),
        ("num_sparse", "Sparse sets"),
        ("num_dense", "Dense sets"),
        ("mean_color_set_size", "Mean distinct set size"),
        ("mean_kmer_color_set_size", "Mean $k$-mer set size"),
        ("num_forward_unitigs", "Unitigs"),
        ("mean_unitig_len", "Mean unitig length"),
    ]

    # Put key k-mer fraction into percentage form
    for row in rows:
        row["key_kmer_frac"] = "{:.2f}".format(row["key_kmer_frac"] * 100) + " \\%"

    def fmt(v):
        if isinstance(v, int):
            return f"{v:,}"
        if isinstance(v, float):
            return f"{v:.2f}"
        return str(v)

    #header = " & ".join("\\makecell[l]{" + label + "}" for _, label in columns) + r" \\"
    header_row1 = "\multicolumn{1}{l}{Dataset} & \multicolumn{1}{l}{$k$-mers} & \multicolumn{1}{c}{Key} & \multicolumn{1}{l}{Distinct} & \multicolumn{1}{c}{Dense} & \multicolumn{1}{l}{Sparse} & \multicolumn{1}{c}{Mean} & \multicolumn{1}{c}{Mean} & \multicolumn{1}{l}{Unitigs} & \multicolumn{1}{c}{Mean} \\\\"
    header_row2 = "\multicolumn{1}{l}{} & \multicolumn{1}{l}{} & \multicolumn{1}{c}{$k$-mers} & \multicolumn{1}{l}{color sets} & \multicolumn{1}{c}{color sets} & \multicolumn{1}{l}{color sets} & \multicolumn{1}{c}{distinct} & \multicolumn{1}{c}{$k$-mer} & \multicolumn{1}{l}{} & \multicolumn{1}{c}{unitig} \\\\"
    header_row3 = "\multicolumn{1}{l}{} & \multicolumn{1}{l}{} & \multicolumn{1}{c}{} & \multicolumn{1}{l}{} & \multicolumn{1}{c}{} & \multicolumn{1}{l}{} & \multicolumn{1}{c}{set size} & \multicolumn{1}{c}{set size} & \multicolumn{1}{l}{} & \multicolumn{1}{c}{length} \\\\"

    header_row1 = "\multicolumn{1}{l}{Dataset} & \multicolumn{1}{l}{Distinct} & \multicolumn{1}{l}{Key} & \multicolumn{1}{l}{Distinct} & \multicolumn{1}{l}{Dense} & \multicolumn{1}{l}{Sparse} & \multicolumn{1}{l}{Mean} & \multicolumn{1}{l}{Mean} & \multicolumn{1}{l}{Number} & \multicolumn{1}{l}{Mean} \\\\"
    header_row2 = "\multicolumn{1}{l}{} & \multicolumn{1}{l}{$k$-mers} & \multicolumn{1}{l}{$k$-mers} & \multicolumn{1}{l}{color sets} & \multicolumn{1}{l}{color sets} & \multicolumn{1}{l}{color sets} & \multicolumn{1}{l}{distinct} & \multicolumn{1}{l}{$k$-mer} & \multicolumn{1}{l}{of unitigs} & \multicolumn{1}{l}{unitig} \\\\"
    header_row3 = "\multicolumn{1}{l}{} & \multicolumn{1}{l}{} & \multicolumn{1}{l}{} & \multicolumn{1}{l}{} & \multicolumn{1}{l}{} & \multicolumn{1}{l}{} & \multicolumn{1}{l}{set size} & \multicolumn{1}{l}{set size} & \multicolumn{1}{l}{} & \multicolumn{1}{l}{length} \\\\"

    header = header_row1 + "\n" + header_row2 + "\n" + header_row3 + "\n"

    rows_tex = [
        " & ".join(fmt(row[k]) for k, _ in columns) + r" \\"
        for row in rows
    ]

    # Narrow columns (tune widths as needed)
    colspec = (
        "rrrrrrrrrrr"
    )

    return "\n".join([
        rf"\begin{{tabular}}{{{colspec}}}",
        r"\toprule",
        header,
        r"\midrule",
        *rows_tex,
        r"\bottomrule",
        r"\end{tabular}",
    ])



max_power_salmonella = 16
max_power_random = 14

rows = []

for i in range(1, max_power_salmonella+1):
    n = 2**i
    stats_file = f"stats/salmonella_{n}_d10000.thm2.stats"
    log_file = f"logs/salmonella_{n}_themisto_d10000.log"
    stats = parse_stats_file(stats_file)
    log_stats = parse_log_file(log_file)
    for key in log_stats: stats[key] = log_stats[key]

    del stats["num_colors"]
    stats["dataset"] = "S-" + str(n)
    rows.append(stats)

for i in range(1, max_power_random+1):
    n = 2**i
    stats_file = f"stats/random_{n}_d10000.thm2.stats"
    log_file = f"logs/random_{n}_themisto_d10000.log"
    stats = parse_stats_file(stats_file)
    log_stats = parse_log_file(log_file)
    for key in log_stats: stats[key] = log_stats[key]
    del stats["num_colors"]
    stats["dataset"] = "R-" + str(n)
    rows.append(stats)

print(format_latex_table(copy.deepcopy(rows[:]))) # Make a copy because this function modifies the rows

print()
print("=====================")
print()

# Print csv
cols = rows[0].keys()
print(",".join(cols))
for row in rows:
    print(",".join([str(row[col]) for col in cols]))


