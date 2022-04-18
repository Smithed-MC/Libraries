# @public
#> input: smithed.item: item
#> output: smithed.item: item

execute unless data storage smithed.item:main item.tag.smithed.hasLore run function ./setup:
    data modify storage smithed.item:main item.tag.smithed.lore set from storage smithed.item:main item.tag.display.Lore
    data modify storage smithed.item:main item.tag.smithed.hasLore set value 1b
    data modify storage smithed.item:main item.tag.HideFlags set value 127

data modify storage smithed.item:main item.tag.display.Lore set value []



#resolve custom lore
execute if data storage smithed.item:main item.tag.smithed.lore run function smithed.item:impl/__version__/lore/custom


#resolve attributes
function ./attributes
#resolve durability
execute if data storage smithed.item:main item.tag.smithed.durability.dur run function smithed.item:impl/__version__/lore/durability