for i in range(1, 14+1):
    n = 2**i
    input = f"fof/random_fof_{n}.txt"
    output = f"SBWTs/random_{n}"
    log_output = f"logs/random_{n}_sbwt.log"
    
    print(f"/usr/bin/time -v sbwt build --input-list {input} -t 32 -v -o {output} --temp-dir temp --in-memory -l -k 31 -m 100 -d -r 2>&1 | tee {log_output}")

    # Without --in-memory
    #print(f"/usr/bin/time -v sbwt build --input-list {input} -t 32 -v -o {output} --temp-dir temp -l -k 31 -m 100 -d -r 2>&1 | tee {log_output}")
