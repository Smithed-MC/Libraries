from bolt_expressions import Scoreboard, Data
from ./base_attributes import base_attributes

data_obj = Scoreboard("smithed.data")
storage = Data.storage("smithed.item:main")

data modify storage smithed.item:main lore.slots set value {
    mainhand: [],
    offhand: [],
    feet: [],
    legs: [],
    chest: [],
    head: []
}


unless data storage smithed.item:main item.tag.AttributeModifiers[] function ./attributes/collect_base:
    for id in base_attributes:
        if data storage smithed.item:main item{id: id}:
            storage.lore.temp = base_attributes[id]
    execute store result score $iter smithed.data if data storage smithed.item:main lore.temp[]

if data storage smithed.item:main item.tag.AttributeModifiers[] function ./attributes/setup_non_base:
    data modify storage smithed.item:main lore.temp set from storage smithed.item:main item.tag.AttributeModifiers
    execute store result score $iter smithed.data if data storage smithed.item:main lore.temp[]


if data storage smithed.item:main lore.temp[] function ./attributes/collect_non_base:
    data modify storage smithed.item:main lore.attr set from storage smithed.item:main lore.temp[-1] 
    data remove storage smithed.item:main lore.attr.UUID
    data remove storage smithed.item:main lore.attr.Name

    data remove storage smithed.item:main lore.temp[-1]

    unless data storage smithed.item:main lore.attr.Slot function ./attributes/collect_non_base/any:
        for slot in ['mainhand', 'offhand', 'feet', 'legs', 'chest', 'head']:
            data modify storage smithed.item:main f'lore.slots.{slot}' append from storage smithed.item:main lore.attr
    if data storage smithed.item:main lore.attr.Slot function ./attributes/collect_non_base/specific:
        for slot in ['mainhand', 'offhand', 'feet', 'legs', 'chest', 'head']:
            if data storage smithed.item:main lore.attr{Slot:slot} data modify storage smithed.item:main f'lore.slots.{slot}' append from storage smithed.item:main lore.attr
    


    scoreboard players remove $iter smithed.data 1

    if score $iter smithed.data matches 1.. function ./attributes/collect_non_base


modifiers = [
    'generic.max_health',
    'generic.follow_range',
    'generic.knockback_resistance',
    'generic.movement_speed',
    'generic.flying_speed',
    'generic.attack_damage',
    'generic.attack_knockback',
    'generic.attack_speed',
    'generic.luck',
    'generic.armor',
    'generic.armor_toughness'
]

def generateOperations(mode):
    color = 'blue'
    if mode == 'take':
        color = 'red'
    elif mode == 'equals':
        color = 'dark_green'


    for i in range(0, 3):
        if data storage smithed.item:main lore.attr{Operation: i} data modify storage smithed.item:main lore.attr.initialJSON set value ('{"translate":"attribute.modifier.'+ mode + '.' + str(i) + '","with":[{"nbt":"lore.attr.AmountJSON","interpret":true,"storage":"smithed.item:main"},{"nbt":"lore.attr.AttributeName","storage":"smithed.item:main","interpret":true}],"color":"' + color + '","italic":false}')
                            
    data modify block -30000000 0 1603 Text1 set from storage smithed.item:main lore.attr.initialJSON

execute function ./attributes/add_lore:
    path = 'lore/attributes/add_lore'
    for slot in ['mainhand', 'offhand', 'feet', 'legs', 'chest', 'head']:     
        execute function generate_path(f'{path}/{slot}'):
            data modify storage smithed.item:main lore.temp set from storage smithed.item:main f'lore.slots.{slot}'
            execute store result score $iter smithed.data if data storage smithed.item:main lore.temp[]
            
            if score $iter smithed.data matches 1.. function generate_path(f"{path}/{slot}/add_header"):
                data modify storage smithed.item:main item.tag.display.Lore append value '{"text":""}'
                data modify storage smithed.item:main item.tag.display.Lore append value ('{"translate":"item.modifiers.'+slot+'","italic": "false","color":"gray"}')
            if score $iter smithed.data matches 1.. function generate_path(f"{path}/{slot}/loop"):
                data modify storage smithed.item:main lore.attr set from storage smithed.item:main lore.temp[-1] 
                data remove storage smithed.item:main lore.temp[-1]
                scoreboard players remove $iter smithed.data 1

                data_obj["$oper"] = storage.lore.attr.Operation
                data_obj["$scale"] = 100
                if score $oper smithed.data matches 1.. function generate_path(f"{path}/{slot}/set_scale"):
                    data_obj["$scale"] = 1


                execute store result score $amount smithed.data run data get storage smithed.item:main lore.attr.Amount 1000000
                if data storage smithed.item:main lore.attr{base:1b} function ./attributes/get_base:
                    for m in modifiers:
                        if data storage smithed.item:main lore.attr{AttributeName: m} store result score $base smithed.data attribute @s f"minecraft:{m}" base get 1000000
                    scoreboard players operation $amount smithed.data += $base smithed.data

                for m in modifiers:
                    if data storage smithed.item:main lore.attr{AttributeName: m} data modify storage smithed.item:main lore.attr.AttributeName set value ('{"translate": "attribute.name.' + m + '"}')

                data_obj["$whole"] = data_obj["$amount"] / 10000
                data_obj["$whole"] /= data_obj["$scale"]
                data_obj["$whole"] *= 10000

                data_obj["$decimal"] = data_obj["$amount"] 
                data_obj["$decimal"] /= data_obj["$scale"]
                data_obj["$decimal"] -= data_obj["$whole"]
                data_obj["$whole"] /= 10000
                # tellraw @s ["Whole: ", {"score":{"name":"$whole","objective":"smithed.data"}}]
                # tellraw @s ["Decim: ", {"score":{"name":"$decimal","objective":"smithed.data"}}]

                if score $decimal smithed.data matches 1.. function generate_path(f"{path}/{slot}/simplify"):
                    data_obj["$decimalLast"] = data_obj["$decimal"] % 10
                    if score $decimalLast smithed.data matches 0 function generate_path(f"{path}/{slot}/simplify/iter"):
                        data_obj["$decimal"] /= 10
                        function generate_path(f"{path}/{slot}/simplify")

                unless score $decimal smithed.data matches 0 function generate_path(f"{path}/{slot}/high_low"):
                    # say high_low
                    if data storage smithed.item:main lore.attr{base:1b}:
                        storage.lore.attr.AmountJSON = '[" ",{"score":{"objective":"smithed.data","name":"$whole"}},".",{"score":{"objective":"smithed.data","name":"$decimal"}}]'
                    unless data storage smithed.item:main lore.attr{base:1b}:
                        storage.lore.attr.AmountJSON = '[{"score":{"objective":"smithed.data","name":"$whole"}},".",{"score":{"objective":"smithed.data","name":"$decimal"}}]'
                if score $decimal smithed.data matches 0 function generate_path(f"{path}/{slot}/high"):
                    # say high
                    if data storage smithed.item:main lore.attr{base:1b}:
                        storage.lore.attr.AmountJSON = '[" ",{"score":{"objective":"smithed.data","name":"$whole"}}]'
                    unless data storage smithed.item:main lore.attr{base:1b}:
                        storage.lore.attr.AmountJSON = '[{"score":{"objective":"smithed.data","name":"$whole"}}]'
                        
                storage.lore.attr.AmountHigh = data_obj["$whole"]
                storage.lore.attr.AmountLow = data_obj["$decimal"]

                if data storage smithed.item:main lore.attr{base:1b} function generate_path(f"{path}/{slot}/equals"):
                    generateOperations('equals')
                unless data storage smithed.item:main lore.attr{base:1b} function generate_path(f"{path}/{slot}/not_equals"):
                    if score $amount smithed.data matches 0.. function generate_path(f"{path}/{slot}/positive"):
                        generateOperations('plus')
                    if score $amount smithed.data matches ..-1 function generate_path(f"{path}/{slot}/negative"):
                        generateOperations('take')

                data modify storage smithed.item:main item.tag.display.Lore append from block -30000000 0 1603 Text1

                if score $iter smithed.data matches 1.. function generate_path(f"{path}/{slot}/loop")
