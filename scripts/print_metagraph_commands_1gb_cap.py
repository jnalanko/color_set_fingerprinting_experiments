dataset = "salmonella"
max_power = 11 # If bigger than this, xargs will split input multiple commands

#dataset = "random"
#max_power = 14

for i in range(1, max_power+1):
    n = 2**i
    mem_cap_gb = 1

    # Build DBG

    input = f"fof/{dataset}_fof_{n}.txt"
    dbg = f"metagraph/{dataset}_{n}.fna.dbg"
    anno_output = f"metagraph/{dataset}_{n}_1gb.fna.anno"
    anno_log_output = f"logs/{dataset}_{n}_metagraph_1gb_anno.log"
    # Build annotation 
    print(f"cat {input} | /usr/bin/time -v xargs ~/code/metagraph/metagraph_DNA annotate -i {dbg} -o {anno_output} --anno-filename --verbose --anno-type row -p 32 --fwd-and-reverse --mem-cap-gb {mem_cap_gb} 2>&1 | tee {anno_log_output}")
