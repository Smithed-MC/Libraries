execute unless data storage smithed.item:main item.tag.smithed.durability.dur run function smithed.item:impl/durability/init

function smithed.item:impl/durability/calc_durability

## execute unless item smithed.item:main item{id:"minecraft:elytra} then dont do the stuff 
execute if score $out smithed.data matches -1..0 run playsound minecraft:entity.item.break player @a[distance=..16]
execute if score $out smithed.data matches 0 run data modify storage smithed.item:main item set value "null"
