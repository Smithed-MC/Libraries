# builds actual lore into lore
# @s = (doesn't matter)
# located at (doesn't matter)
# run from lore/build

# get stored lore
data modify storage smithed.item:main lore.temp set from storage smithed.item:main item.tag.smithed.lore
execute store result score $iter smithed.item if data storage smithed.item:main lore.temp[]

execute function ./custom/iter:
    # for each line of custom lore, add it to the item lore
    data modify block -30000000 0 1603 front_text.messages[0] set from storage smithed.item:main lore.temp[-1] 
    data remove storage smithed.item:main lore.temp[-1]
    scoreboard players remove $iter smithed.item 1

    data modify storage smithed.item:main item.tag.display.Lore append from block -30000000 0 1603 front_text.messages[0]

    execute if score $iter smithed.item matches 1.. run function smithed.item:impl/lore/custom/iter


