
data modify storage smithed:crafter root.temp.b set from storage smithed:crafter root.temp.simplified[6]
data remove storage smithed:crafter root.temp.b.Count

execute store success score $temp1 smithed.data run data modify storage smithed:crafter root.temp.b set from storage smithed:crafter root.temp.a
execute if score $temp1 smithed.data matches 0 store result storage smithed:crafter root.temp.simplified[6].Count byte -1 run data get storage smithed:crafter root.temp.simplified[6].Count -1.000001
