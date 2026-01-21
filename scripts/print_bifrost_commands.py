def print_all(dataset, max_power):
    for i in range(1, max_power+1):
        n = 2**i
        input = f"fof/{dataset}_fof_{n}.txt"
        output = f"bifrost/{dataset}_{n}.fna"
        log_output = f"logs/{dataset}_{n}_bifrost.log"
        threads = 32

        print(f"LD_LIBRARY_PATH=~/code/bifrost_fork/build/lib/ /usr/bin/time -v ~/code/bifrost_fork/build/bin/Bifrost build -r {input} -o {output} -t {threads} --tmp-dir temp -c -v 2>&1 | tee {log_output}")

print_all("random", 14)
print_all("salmonella", 17)

