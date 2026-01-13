dataset = "salmonella"
max_power = 17

for i in range(1, max_power+1):
    n = 2**i
    input = f"fof/{dataset}_fof_{n}.txt"
    output = f"bifrost/{dataset}_{n}.fna"
    log_output = f"logs/{dataset}_{n}_bifrost.log"
    threads = 16 # Bifrost supports max 16, otherwise refuses to run

    print(f"LD_LIBRARY_PATH=~/code/bifrost/build/lib/ /usr/bin/time -v ~/code/bifrost/build/bin/Bifrost build -r {input} -o {output} -t {threads} --tmp-dir temp -c -v 2>&1 | tee {log_output}")
