# @public

data modify storage smithed.tech_slots:data temp.args.UUID set from entity @s UUID
data modify storage smithed.tech_slots:data temp.args.input set from storage smithed.tech_slots:data input
function smithed.tech_slots:impl/storage/remove_modifier with storage smithed.tech_slots:data temp.args
data remove storage smithed.tech_slots:data temp
