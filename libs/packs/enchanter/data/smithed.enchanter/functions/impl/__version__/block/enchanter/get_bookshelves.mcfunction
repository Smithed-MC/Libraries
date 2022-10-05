from bolt_expressions import Scoreboard
data_obj = Scoreboard("smithed.data")

patern = [
    "#####",
    "#   #",
    "#   #",
    "#   #",
    "#####"
]


merge block_tag smithed.enchanter:air {
    "values": [
        "minecraft:air",
        "minecraft:void_air",
        "minecraft:cave_air"
    ]
}

def generateCheck(x,y,z):
    if block ~x ~y ~z minecraft:bookshelf:
        airX = x-1
        airZ = z-1
        if x < 0:
            airX = x+1
        if z < 0:
            airZ = z+1

        if abs(x) == abs(z):
            if block ~airX ~ ~airZ #smithed.enchanter:air if block ~airX ~1 ~airZ #smithed.enchanter:air run scoreboard players add b smithed.data 1
        elif abs(x) > abs(z):
            if block ~airX ~ ~z #smithed.enchanter:air if block ~airX ~ ~z #smithed.enchanter:air run scoreboard players add b smithed.data 1
        elif abs(x) < abs(z):
            if block ~x ~ ~airZ #smithed.enchanter:air if block ~x ~ ~airZ #smithed.enchanter:air run scoreboard players add b smithed.data 1


data_obj["b"] = 0
for y in range(2):
    for z in range(len(patern)):
        for x in range(len(patern[y])):
            if patern[z][x] == "#":
                generateCheck(x-2,y,z-2)

if score b smithed.data matches 15..:
    data_obj["b"] = 15

# tellraw @s ["Bks: ",{"score": {"name": "b", "objective": "smithed.data"}}]
