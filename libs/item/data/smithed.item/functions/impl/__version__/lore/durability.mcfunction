data modify block -30000000 0 1603 Text1 set value '{"translate":"item.durability","with":[{"nbt":"item.tag.smithed.durability.dur","storage":"smithed.damage:"},{"nbt":"item.tag.smithed.durability.max","storage":"smithed.damage:"}],"color":"white","italic":false}' 
data modify storage smithed.damage: item.tag.display.Lore append from block -30000000 0 1603 Text1
