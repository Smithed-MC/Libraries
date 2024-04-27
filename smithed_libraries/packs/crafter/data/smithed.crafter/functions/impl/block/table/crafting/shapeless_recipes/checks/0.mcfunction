data modify storage smithed.crafter:main root.temp.b set from storage smithed.crafter:main root.temp.simplified[0]
data remove storage smithed.crafter:main root.temp.b.count
data remove storage smithed.crafter:main root.temp.b.Slot

execute store success score $temp1 smithed.data run data modify storage smithed.crafter:main root.temp.b set from storage smithed.crafter:main root.temp.a

# if same, add 1 to the storage count
execute if score $temp1 smithed.data matches 0 store result storage smithed.crafter:main root.temp.simplified[0].count int -1 run data get storage smithed.crafter:main root.temp.simplified[0].count -1.000001

