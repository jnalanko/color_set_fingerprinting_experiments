def print_all(dataset, max_power):
    for i in range(1, max_power+1):
        n = 2**i
        input = f"fof/{dataset}_fof_{n}.txt"
        output = f"ggcat/{dataset}_{n}.fna"
        log_output = f"logs/{dataset}_{n}_ggcat.log"

        print(f"/usr/bin/time -v ggcat build -c -p -k 31 -m 256 -s 1 -o {output} -j 32 --temp-dir temp --input-lists {input} 2>&1 | tee {log_output}")

print_all("random", 14)
print_all("salmonella", 17)

# ls unitig-split-1000 | grep fof_part_ | xargs -I {} bash -c "/usr/bin/time -v ggcat build -p -k 31 -m 40 -s 1 -o unitig-split-1000/{}.fna -j 24 --input-lists unitig-split-1000/{} &> logs/{}"
