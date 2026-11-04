# @public

# set item if doesn't exist
execute unless items entity @s armor.body * run return run item replace entity @s armor.body with minecraft:poisonous_potato[!minecraft:consumable, minecraft:equippable= {slot:"body",equip_sound:"intentionally_empty"},enchantments={"minecraft:vanishing_curse":1,"minecraft:binding_curse":1},custom_data={smithed.tech_slots:{set:true}}]

# return early if smithed data is present
execute if items entity @s armor.body *[minecraft:custom_data~{smithed.tech_slots:{set:true}}] run return 1

# force binding and vanishing curses
item modify entity @s armor.body smithed.tech_slots:impl/set_body_data

# force silent equip sound
data modify storage smithed.tech_slots:data temp.body set from entity @s equipment.body
data modify storage smithed.tech_slots:data temp.body merge value {components:{"minecraft:equippable":{slot:"body",equip_sound:"intentionally_empty"}}}
item replace entity @s armor.body with air

tag @s add smithed.tech_slots.target
execute summon item_display run function smithed.tech_slots:impl/player/set_body_sound
tag @s remove smithed.tech_slots.target

data remove storage smithed.tech_slots:data temp
