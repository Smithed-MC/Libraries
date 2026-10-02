data modify entity @s item set from storage smithed.tech_slots:data temp.body
item replace entity @a[distance=0,tag=smithed.tech_slots.target] armor.body from entity @s container.0
kill @s
