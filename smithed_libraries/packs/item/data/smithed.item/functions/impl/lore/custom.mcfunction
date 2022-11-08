data modify storage smithed.item:main lore.temp set from storage smithed.item:main item.tag.smithed.lore
execute store result score $iter smithed.data if data storage smithed.item:main lore.temp[]

execute function ./custom/iter:
    data modify block -30000000 0 1603 Text1 set from storage smithed.item:main lore.temp[-1] 
    data remove storage smithed.item:main lore.temp[-1]
    scoreboard players remove $iter smithed.data 1

    data modify storage smithed.item:main item.tag.display.Lore append from block -30000000 0 1603 Text1

    execute if score $iter smithed.data matches 1.. run function smithed.item:impl/lore/custom/iter


