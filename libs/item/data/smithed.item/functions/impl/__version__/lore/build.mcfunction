# @public
#> input: smithed.damage: item
#> output: smithed.damage: item

execute if data storage smithed.damage: item.tag.display.Lore[] unless data storage smithed.damage: item.tag.smithed.lore run data modify storage smithed.damage: item.tag.smithed.lore set from storage smithed.damage: item.tag.display.Lore
data remove storage smithed.damage: item.tag.display.Lore



#resolve custom lore
function smithed.damage:impl/__version__/lore/custom/start

#resolve attributes

#resolve durability
execute if data storage smithed.damage: item.tag.smithed.durability.dur run function smithed.damage:impl/__version__/lore/durability