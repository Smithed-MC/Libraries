# calculates the item's new durability
# @s = player who has a custom durability item that changed durability
# located at world spawn
# run from durability/update/start

# set custom durability
## get the change in damage (neg if durability decreased, pos if durability increased)
scoreboard players operation $damage_diff smithed.item = $old_damage smithed.item
scoreboard players operation $damage_diff smithed.item -= $new_damage smithed.item

## add the change in damage to the durability
scoreboard players operation $custom_durability smithed.item += $damage_diff smithed.item

## bound between 0 and the custom max durability
scoreboard players operation $custom_durability smithed.item < $custom_max smithed.item
scoreboard players operation $custom_durability smithed.item > 0 smithed.const

## update item's custom durability
execute store result storage smithed.item:main item.tag.smithed.durability.dur int 1 run scoreboard players get $custom_durability smithed.item

# set durability bar
## get relative durability (new damage = custom durability / custom max * item max)
scoreboard players operation $relative_dur smithed.item = $custom_durability smithed.item
scoreboard players operation $relative_dur smithed.item *= $item_max smithed.item
scoreboard players operation $relative_dur smithed.item /= $custom_max smithed.item

## check if the item is allowed to break
scoreboard players set $prevent_destroy smithed.item 0
execute store result score $prevent_destroy smithed.item run data get storage smithed.item:main item.tag.smithed.durability.prevent_destroy
execute if data storage smithed.item:main item{id:"minecraft:elytra"} unless data storage smithed.item:main item.tag.smithed.durability{prevent_destroy:0b} run scoreboard players set $prevent_destroy smithed.item 1

## get the new expected item damage
scoreboard players operation $item_damage smithed.item = $item_max smithed.item
scoreboard players operation $item_damage smithed.item -= $relative_dur smithed.item
## keep the item's actual durability above 10 (prevent item breaking)
scoreboard players operation $minus_10 smithed.item = $item_max smithed.item
scoreboard players remove $minus_10 smithed.item 10
scoreboard players operation $item_damage smithed.item < $minus_10 smithed.item
## keep the item's actual damage above 16 (prevent mending overflow), unless both the custom and relative damage are below 16
scoreboard players operation $custom_damage smithed.item = $custom_max smithed.item
scoreboard players operation $custom_damage smithed.item -= $custom_durability smithed.item
execute if score $item_damage smithed.item matches ..15 if score $custom_damage smithed.item matches ..15 run scoreboard players operation $item_damage smithed.item = $custom_damage smithed.item
execute if score $item_damage smithed.item matches ..15 unless score $custom_damage smithed.item matches ..15 run scoreboard players operation $item_damage smithed.item > 16 smithed.const
## use actual durability bar if both the custom and relative durability dips below 10
execute if score $relative_dur smithed.item matches 0..10 if score $custom_durability smithed.item matches 0..10 if score $prevent_destroy smithed.item matches 0 run scoreboard players operation $item_damage smithed.item = $item_max smithed.item
execute if score $relative_dur smithed.item matches 0..10 if score $custom_durability smithed.item matches 0..10 if score $prevent_destroy smithed.item matches 0 run scoreboard players operation $item_damage smithed.item -= $custom_durability smithed.item

## change the item's actual durability
execute store result storage smithed.item:main item.tag.smithed.durability.damage int 1 store result storage smithed.item:main item.tag.Damage int 1 run scoreboard players get $item_damage smithed.item
function smithed.item:impl/lore/build

# output state (1 = durability changed, 0 = broken and gone, -1 = broken and converted to different item, -2 = no change (default))
scoreboard players set $out smithed.item 1
execute if score $custom_durability smithed.item matches 0 run scoreboard players set $out smithed.item 0
execute if score $custom_durability smithed.item matches 0..1 unless score $prevent_destroy smithed.item matches 0 run scoreboard players set $out smithed.item -1

# clean up
scoreboard players reset $custom_durability smithed.item
scoreboard players reset $damage_diff smithed.item
scoreboard players reset $item_damage smithed.item
scoreboard players reset $custom_max smithed.item
scoreboard players reset $relative_dur smithed.item
scoreboard players reset $custom_damage smithed.item
scoreboard players reset $minus_10 smithed.item
scoreboard players reset $prevent_destroy smithed.item
