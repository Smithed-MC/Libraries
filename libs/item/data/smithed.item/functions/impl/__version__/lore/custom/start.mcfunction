data modify storage smithed.damage:main lore.temp set from storage smithed.damage:main item.tag.smithed.lore
execute store result score $iter smithed.data if data storage smithed.damage:main lore.temp[]

function smithed.damage:impl/__version__/lore/custom/iter