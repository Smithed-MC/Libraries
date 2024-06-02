playsound minecraft:item.bucket.empty block @a[distance=..7, tag=smithed.inside_crafter] ~ ~ ~
data modify entity @s HandItems[0].id set value "minecraft:bucket"
scoreboard players set $temp smithed.data 1