# @public

# set saddle slot
item replace entity @s saddle with saddle[equippable={slot:"saddle",equip_sound:"intentionally_empty"}]

# run modifier instantly
function smithed.tech_slots:impl/modifier/modify_saddle with storage smithed.tech_slots:data input
function smithed.tech_slots:impl/modifier/trigger

# clear saddle slot
item replace entity @s saddle with air
