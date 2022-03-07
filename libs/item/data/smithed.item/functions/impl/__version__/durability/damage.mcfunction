execute unless data storage smithed.damage: item.tag.smithed.durability.dur run function smithed.damage:impl/__version__/durability/init

function smithed.damage:impl/__version__/durability/calc_durability
execute if score $out smithed.data matches -1..0 run playsound minecraft:entity.item.break player @a[distance=..16]
execute if score $out smithed.data matches 0 run data modify storage smithed.damage: item set value "null"

