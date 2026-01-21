binary_path = "../code/bin/metagraph_DNA"

def print_all(dataset, max_power):
    for i in range(1, max_power+1):
        n = 2**i
        mem_cap_gb = 1

        # Build DBG

        input = f"fof/{dataset}_fof_{n}.txt"
        dbg = f"metagraph/{dataset}_{n}.fna.dbg"
        anno_output = f"metagraph/{dataset}_{n}_1gb.fna.anno"
        anno_log_output = f"logs/{dataset}_{n}_metagraph_1gb_anno.log"
        # Build annotation 
        print(f"cat {input} | /usr/bin/time -v xargs {binary_path} annotate -i {dbg} -o {anno_output} --anno-filename --verbose --anno-type row -p 32 --fwd-and-reverse --mem-cap-gb {mem_cap_gb} 2>&1 | tee {anno_log_output}")

# Only up to 11 because xargs will split into multiple commands otherwise
print_all("random", 11)
print_all("salmonella", 11)

