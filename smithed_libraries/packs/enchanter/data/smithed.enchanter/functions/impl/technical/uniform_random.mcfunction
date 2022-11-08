from bolt_expressions import Scoreboard
data_obj = Scoreboard("smithed.data")

size = data_obj["#size"]
lcg = data_obj["#lcg"]
lcg_a = data_obj["#lcg_a"]
lcg_c = data_obj["#lcg_c"]
lcg_m = data_obj["#lcg_m"]
min = data_obj["$min"]
max = data_obj["$max"]
out = data_obj["$out"]



# print(min, max)
size = max - min + 1


#/ Xn+1 = (aXn + c) mod m
lcg *= lcg_a
lcg += lcg_c
lcg %= lcg_m

# Trim "low quality" bits
# Get within desired range
out = ((lcg/8) % size) + min
