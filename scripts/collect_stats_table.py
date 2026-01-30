from datetime import datetime, timezone

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
        "Fraction of key k-mers": "key_kmer_frac_pct",
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
                value = value.replace("%", "\\%") # Escape percentage for latex
                stats[key] = value

    return stats

def format_latex_table(rows):

    # Human-readable column names
    columns = [
        ("dataset", "Dataset"),
        ("num_colors", "Genomes"),
        ("num_kmers", "$k$-mers"),
        ("key_kmer_frac_pct", r"Key $k$-mers (\%)"),
        ("num_color_sets", "Distinct sets"),
        ("num_dense", "Dense sets"),
        ("num_sparse", "Sparse sets"),
        ("mean_color_set_size", "Mean distinct set size"),
        ("mean_kmer_color_set_size", "Mean $k$-mer set size"),
        ("num_forward_unitigs", "Unitigs"),
        ("mean_unitig_len", "Mean unitig length"),
    ]

    def fmt(v):
        if isinstance(v, int):
            return f"{v:,}"
        if isinstance(v, float):
            return f"{v:.2f}"
        return str(v)

    header = " & ".join("\\makecell[l]{" + label + "}" for _, label in columns) + r" \\"

    rows_tex = [
        " & ".join(fmt(row[k]) for k, _ in columns) + r" \\"
        for row in rows
    ]

    # Narrow columns (tune widths as needed)
    colspec = (
        "c r{1.0cm} r{1.2cm} r{0.8cm} r{1.4cm} r{1.4cm} r{1.4cm} r{1.0cm} r{1.0cm} r{1.6cm} r{1.3cm}"
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
    stats["dataset"] = "Salmonella"
    rows.append(stats)

for i in range(1, max_power_random+1):
    n = 2**i
    stats_file = f"stats/random_{n}_d10000.thm2.stats"
    log_file = f"logs/random_{n}_themisto_d10000.log"
    stats = parse_stats_file(stats_file)
    log_stats = parse_log_file(log_file)
    for key in log_stats: stats[key] = log_stats[key]
    stats["dataset"] = "Random"
    rows.append(stats)

print(format_latex_table(rows))

#max_power_random = 14

#for i in range(1, max_power_random):
#    n = 2**i
#    print(f"echo stats for random_{n} && themisto2 stats -t 32 -i themisto2/random_{n}_d10000.thm2 > stats/random_{n}_d10000.thm2.stats")
