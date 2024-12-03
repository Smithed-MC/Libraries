# builds durability into lore
# @s = (doesn't matter)
# located at (doesn't matter)
# run from lore/build

data modify block -30000000 0 1603 front_text.messages[0] set value '{"translate":"item.durability","with":[{"nbt":"item.tag.smithed.durability.dur","storage":"smithed.item:main"},{"nbt":"item.tag.smithed.durability.max","storage":"smithed.item:main"}],"color":"white","italic":false}' 
data modify storage smithed.item:main item.tag.display.Lore append from block -30000000 0 1603 front_text.messages[0]
