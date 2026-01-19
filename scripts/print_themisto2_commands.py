#dataset = "random"
#max_power = 14

dataset = "salmonella"
max_power = 17

for i in range(1, max_power+1):
    n = 2**i
    input = f"fof/{dataset}_fof_{n}.txt"
    sbwt = f"SBWTs/{dataset}_{n}.sbwt"
    lcs = f"SBWTs/{dataset}_{n}.lcs"
    output = f"themisto2/{dataset}_{n}.thm2"
    log_output = f"logs/{dataset}_{n}_themisto.log"

    print(f"/usr/bin/time -v themisto2 build -i {input} --sbwt {sbwt} --lcs {lcs} -o {output} --temp-dir temp -k 31 -d 30 -t 32 --index-type sparse-dense 2>&1 | tee {log_output}")
