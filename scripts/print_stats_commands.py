max_power_salmonella = 16
max_power_random = 14

for i in range(1, max_power_salmonella+1):
    n = 2**i
    print(f"echo stats for salmonella_{n} && themisto2 stats -t 32 -i themisto2/salmonella_{n}_d10000.thm2 > stats/salmonella_{n}_d10000.thm2.stats")

for i in range(1, max_power_random+1):
    n = 2**i
    print(f"echo stats for random_{n} && themisto2 stats -t 32 -i themisto2/random_{n}_d10000.thm2 > stats/random_{n}_d10000.thm2.stats")
