data modify storage smithed.damage: lore.temp set from storage smithed.damage: item.tag.smithed.lore
execute store result score $iter smithed.data if data storage smithed.damage: lore.temp[]

function smithed.damage:impl/__version__/lore/custom/iter