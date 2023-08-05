# @public
# builds the item stats with lore
# @s = (doesn't matter)
# located at (doesn't matter)
# run from durability/update/calc_durability
# run from api call

from bolt_expressions import Scoreboard, Data
storage = Data.storage("smithed.item:main")
data_obj = Scoreboard("smithed.item")
#> input: smithed.item:main item
#> output: smithed.item:main item

# set up item the first time
execute unless data storage smithed.item:main item.tag.smithed{hasLore:1b} run function ./setup:
    # store actual lore into temp storage
    storage.item.tag.smithed.lore = storage.item.tag.display.Lore
    
    # get hideFlags values
    storage.item.tag.smithed.hideFlags = {'0':0,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0}
    if data storage smithed.item:main item.tag.HideFlags:
        data_obj["$hideFlags"] = storage.item.tag.HideFlags

        for i in range(7):
            if score $hideFlags smithed.item matches f'{pow(2, 6-i)}..':
                data_obj["$remainder"] = data_obj["$hideFlags"] % 2
                data_obj["$hideFlags"] /= 2
                store result storage smithed.item:main f'item.tag.smithed.hideFlags.{i}' int 1 scoreboard players get $remainder smithed.item
        

    # set resulting item to be marked with smithed lore and hide all actual flags (except real durability since that's a debug option)
    storage.item.tag.smithed.hasLore = 1b
    storage.item.tag.HideFlags = 127
    

# remove existing lore, going to build it up manually
data modify storage smithed.item:main item.tag.display.Lore set value []

# resolve enchantments
execute if data storage smithed.item:main item.tag.smithed.hideFlags{0:0} if data storage smithed.item:main item.tag.Enchantments run function ./enchantments

# resolve custom lore
execute if data storage smithed.item:main item.tag.smithed.lore run function ./custom

# resolve attributes
execute if data storage smithed.item:main item.tag.smithed.hideFlags{1:0} run function ./attributes

# unbreakable
scoreboard players set $unbreakable smithed.item 0
execute store result score $unbreakable smithed.item run data get storage smithed.item:main item.tag.Unbreakable 1
execute if data storage smithed.item:main item.tag.smithed.hideFlags{2:0} 
    unless score $unbreakable smithed.item matches 0 
    data modify storage smithed.item:main item.tag.display.Lore append value '{"translate":"item.unbreakable","color":"blue","italic":false}' 

# custom pack id
execute if data storage smithed.item:main item.tag.smithed.origin:
    data modify storage smithed.item:main item.tag.display.Lore append value '{"text":""}' 
    data modify storage smithed.item:main item.tag.display.Lore append from storage smithed.item:main item.tag.smithed.origin

# resolve durability
execute if data storage smithed.item:main item.tag.smithed.durability.dur run function ./durability
