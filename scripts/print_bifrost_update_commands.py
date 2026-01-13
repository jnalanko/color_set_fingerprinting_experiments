dataset = "salmonella"
max_power = 17

#dataset = "random"
#max_power = 14

for i in range(1, max_power+1):
    n = 2**i
    threads = 16 # Bifrost supports max 16, otherwise refuses to run

    graph = f"bifrost/{dataset}_{n}.fna.gfa.gz"
    fof = f"fof/{dataset}_fof_{n}.txt"
    index = f"bifrost/{dataset}_{n}.fna.bfi"
    output = f"bifrost/{dataset}_{n}_updated"
    log_output = f"logs/{dataset}_{n}_bifrost-updated.log"

    print(f"LD_LIBRARY_PATH=~/code/bifrost/build/lib/ /usr/bin/time -v ~/code/bifrost/build/bin/Bifrost update -g {graph} -r {fof} -o {output} -I {index} --tmp-dir temp --verbose 2>&1 | tee {log_output}")
