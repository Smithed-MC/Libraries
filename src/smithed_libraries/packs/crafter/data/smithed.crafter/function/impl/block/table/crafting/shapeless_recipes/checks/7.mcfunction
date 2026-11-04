
data modify storage smithed.crafter:main root.temp.b set from storage smithed.crafter:main root.temp.simplified[7]
data remove storage smithed.crafter:main root.temp.b.count

execute store success score $temp1 smithed.data run data modify storage smithed.crafter:main root.temp.b set from storage smithed.crafter:main root.temp.a

execute if score $temp1 smithed.data matches 0 store result score $temp_count smithed.data run data get storage smithed.crafter:main root.temp.simplified[7].count
execute if score $temp1 smithed.data matches 0 run scoreboard players add $temp_count smithed.data 1
execute if score $temp1 smithed.data matches 0 store result storage smithed.crafter:main root.temp.simplified[7].count int 1 run scoreboard players get $temp_count smithed.data
