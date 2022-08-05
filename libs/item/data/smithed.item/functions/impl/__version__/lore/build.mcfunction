# @public
from bolt_expressions import Scoreboard, Data
storage = Data.storage("smithed.item:main")
data_obj = Scoreboard("smithed.data")
#> input: smithed.item:main item
#> output: smithed.item:main item

execute unless data storage smithed.item:main item.tag.smithed{hasLore:1b} run function ./setup:
    storage.item.tag.smithed.lore = storage.item.tag.display.Lore
    
    storage.item.tag.smithed.hideFlags = {'0':0,'1':0,'2':0,'3':0,'4':0,'5':0,'6':0}
    if data storage smithed.item:main item.tag.HideFlags:
        data_obj["$hideFlags"] = storage.item.tag.HideFlags

        for i in range(7):
            if score $hideFlags smithed.data matches f'{pow(2, 6-i)}..':
                data_obj["$remainder"] = data_obj["$hideFlags"] % 2
                data_obj["$hideFlags"] /= 2
                store result storage smithed.item:main f'item.tag.smithed.hideFlags.{i}' int 1 scoreboard players get $remainder smithed.data
        

    storage.item.tag.smithed.hasLore = 1b
    storage.item.tag.HideFlags = 127
    

data modify storage smithed.item:main item.tag.display.Lore set value []

#resolve enchantments
execute if data storage smithed.item:main item.tag.smithed.hideFlags{0:0} if data storage smithed.item:main item.tag.Enchantments run function ./enchantments

#resolve custom lore
execute if data storage smithed.item:main item.tag.smithed.lore run function ./custom


#resolve attributes
execute if data storage smithed.item:main item.tag.smithed.hideFlags{1:0} run function ./attributes

#unbreakable
execute if data storage smithed.item:main item.tag.smithed.hideFlags{2:0} if data storage smithed.item:main item.tag{Unbreakable:1b} data modify storage smithed.item:main item.tag.display.Lore append value '{"translate":"item.unbreakable","color":"blue","italic":false}' 
#custom pack id
execute if data storage smithed.item:main item.tag.smithed.origin:
    data modify storage smithed.item:main item.tag.display.Lore append value '{"text":""}' 
    data modify storage smithed.item:main item.tag.display.Lore append from storage smithed.item:main item.tag.smithed.origin

#resolve durability
execute if data storage smithed.item:main item.tag.smithed.durability.dur run function ./durability