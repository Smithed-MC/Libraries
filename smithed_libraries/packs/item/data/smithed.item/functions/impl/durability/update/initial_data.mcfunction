# populates the item data with specific nbt
# @s = player who has a custom durability item that changed durability
# located at world spawn
# run from durability/damage

# set default values
execute store result storage smithed.item:main item.tag.smithed.durability.dur int 1 run scoreboard players get $custom_max smithed.item

# store max durability of base item
scoreboard players set $item_max smithed.item 0
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:golden_sword"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 32
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:golden_pickaxe"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 32
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:golden_axe"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 32
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:golden_shovel"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 32
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:golden_hoe"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 32

execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:wooden_sword"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 59
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:wooden_pickaxe"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 59
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:wooden_axe"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 59
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:wooden_shovel"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 59
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:wooden_hoe"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 59

execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:stone_sword"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 131
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:stone_pickaxe"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 131
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:stone_axe"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 131
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:stone_shovel"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 131
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:stone_hoe"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 131

execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:iron_sword"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 250
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:iron_pickaxe"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 250
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:iron_axe"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 250
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:iron_shovel"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 250
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:iron_hoe"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 250

execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:diamond_sword"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 1561
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:diamond_pickaxe"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 1561
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:diamond_axe"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 1561
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:diamond_shovel"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 1561
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:diamond_hoe"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 1561

execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:netherite_sword"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 2031
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:netherite_pickaxe"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 2031
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:netherite_axe"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 2031
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:netherite_shovel"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 2031
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:netherite_hoe"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 2031


execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:turtle_helmet"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 275

execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:leather_helmet"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 55
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:leather_chestplate"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 80
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:leather_leggings"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 75
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:leather_boots"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 65

execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:golden_helmet"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 77
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:golden_chestplate"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 112
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:golden_leggings"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 105
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:golden_boots"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 91

execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:chainmail_helmet"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 165
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:chainmail_chestplate"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 240
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:chainmail_leggings"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 225
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:chainmail_boots"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 195

execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:iron_helmet"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 165
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:iron_chestplate"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 240
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:iron_leggings"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 225
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:iron_boots"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 195

execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:diamond_helmet"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 363
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:diamond_chestplate"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 528
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:diamond_leggings"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 495
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:diamond_boots"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 429

execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:netherite_helmet"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 407
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:netherite_chestplate"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 592
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:netherite_leggings"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 555
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:netherite_boots"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 481


execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:fishing_rod"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 64
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:flint_and_steel"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 64
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:carrot_on_a_stick"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 25
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:shears"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 238
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:shield"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 336
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:bow"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 384
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:trident"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 250
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:elytra"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 432
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:crossbow"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 465
execute if score $item_max smithed.item matches 0 if data storage smithed.item:main item{id:"minecraft:warped_fungus_on_a_stick"} store result storage smithed.item:main item.tag.smithed.durability.item_max int 1 run scoreboard players set $item_max smithed.item 100
