execute store result score $temp smithed.data run data get storage smithed.damage: item.tag.Damage
scoreboard players remove $temp smithed.data 1
execute store result storage smithed.damage: item.tag.smithed.durability.damage int 1 run scoreboard players get $temp smithed.data

function smithed.damage:impl/__version__/durability/process/handle
