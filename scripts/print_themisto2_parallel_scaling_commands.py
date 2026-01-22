def print_all(dataset, power):
    for t in [1,2,4,8,16,32]:
        n = 2**power
        input = f"fof/{dataset}_fof_{n}.txt"
        sbwt = f"SBWTs/{dataset}_{n}.sbwt"
        lcs = f"SBWTs/{dataset}_{n}.lcs"
        output = f"themisto2/{dataset}_{n}_parallel.thm2"
        log_output = f"logs/{dataset}_{n}_themisto_t{t}.log"

        print(f"/usr/bin/time -v themisto2 build -i {input} --sbwt {sbwt} --lcs {lcs} -o {output} --temp-dir temp -k 31 -d 30 -t {t} --index-type sparse-dense 2>&1 | tee {log_output}")

print_all("salmonella", 9)
print_all("random", 9)
