binary_path = "../code/bin/metagraph_DNA"

def print_all(dataset, max_power):
    for i in range(1, max_power+1):
        n = 2**i
        input = f"fof/{dataset}_fof_{n}.txt"
        output = f"metagraph/{dataset}_{n}.fna"
        log_output = f"logs/{dataset}_{n}_metagraph.log"
        mem_cap_gb = 100

        # Build DBG
        print(f"cat {input} | /usr/bin/time -v xargs {binary_path} build -k 31 -o {output} -p 32 --mem-cap-gb {mem_cap_gb} --verbose --mode canonical --graph sshash 2>&1 | tee {log_output}")

        anno_output = f"metagraph/{dataset}_{n}.fna.anno"
        anno_log_output = f"logs/{dataset}_{n}_metagraph_anno.log"
        # Build annotation 
        print(f"cat {input} | /usr/bin/time -v xargs {binary_path} annotate -i {output}.dbg -o {anno_output} --anno-filename --verbose --anno-type row -p 32 --fwd-and-reverse --mem-cap-gb {mem_cap_gb} 2>&1 | tee {anno_log_output}")

# Only up to 11 because xargs will split into multiple commands otherwise
print_all("random", 11)
print_all("salmonella", 11)

