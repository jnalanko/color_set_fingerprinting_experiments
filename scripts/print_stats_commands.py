max_power_salmonella = 15
max_power_random = 14

for i in range(1, max_power_salmonella):
    n = 2**i
    print(f"echo stats for salmonella_{n} && themisto2 stats -t 32 -i themisto2/salmonella_{n}.thm2")

for i in range(1, max_power_random):
    n = 2**i
    print(f"echo stats for random_{n} && themisto2 stats -t 32 -i themisto2/random_{n}.thm2")
