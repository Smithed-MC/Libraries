# builds enchantments into lore
# @s = (doesn't matter)
# located at (doesn't matter)
# run from lore/build

from bolt_expressions import Scoreboard, Data
data_obj = Scoreboard("smithed.item")
storage = Data.storage("smithed.item:main")

enchantments = [
    'minecraft:sharpness',
    'minecraft:smite',
    'minecraft:bane_of_arthropods',
    'minecraft:knockback',
    'minecraft:fire_aspect',
    'minecraft:sweeping',
    'minecraft:protection',
    'minecraft:fire_protection',
    'minecraft:feather_falling',
    'minecraft:blast_protection',
    'minecraft:projectile_protection',
    'minecraft:respiration',
    'minecraft:aqua_affinity',
    'minecraft:depth_strider',
    'minecraft:frost_walker',
    'minecraft:soul_speed',
    'minecraft:swift_sneak',
    'minecraft:efficiency',
    'minecraft:silk_touch',
    'minecraft:unbreaking',
    'minecraft:looting',
    'minecraft:fortune',
    'minecraft:luck_of_the_sea',
    'minecraft:lure',
    'minecraft:power',
    'minecraft:flame',
    'minecraft:punch',
    'minecraft:infinity',
    'minecraft:thorns',
    'minecraft:mending',
    'minecraft:binding_curse',
    'minecraft:vanishing_curse',
    'minecraft:loyalty',
    'minecraft:impaling',
    'minecraft:riptide',
    'minecraft:channeling',
    'minecraft:multishot',
    'minecraft:quick_charge',
    'minecraft:piercing'
]

storage.enchantments = storage.item.tag.Enchantments


execute function ./enchantments/loop:
    # go through each enchantment in the order they were added to the item
    storage.temp = storage.enchantments[-1]
    data remove storage smithed.item:main 'enchantments'[-1]
    storage.lore.lvl = storage.temp.lvl
    data_obj["$lvl"] = storage.lore.lvl

    # match enchantment with the proper string
    execute function ./enchantments/loop/find_ench:
        # add the enchantment to the lore
        for e in enchantments:
            if data storage smithed.item:main temp{id: e}:
                storage.lore.ench = ('{"translate":"enchantment.'+e.replace(':','.')+'","italic": "false","color":"gray"}')
        # custom enchantment handling
        function #smithed.item:event/build_custom

    # match enchantment level with proper string
    execute function ./enchantments/loop/find_level:
        # don't display level 1 if there's only one level
        if score $lvl smithed.item matches 1 function ./enchantments/loop/special_level:
            storage.lore.lvl = ('{"translate":"enchantment.level.1","italic": "false","color":"gray"}')
            only_one_level =['minecraft:aqua_affinity','minecraft:channeling','minecraft:riptide','minecraft:curse_of_binding','minecraft:curse_of_vanishing','minecraft:flame','minecraft:infinity','minecraft:mending','minecraft:multishot']
            for e in only_one_level:
                if data storage smithed.item:main temp{id: e}:
                    storage.lore.lvl = ''
        # display 2-10 using translate string
        for i in range(2,11):
            if score $lvl smithed.item matches (i):
                storage.lore.lvl = ('{"translate":"enchantment.level.'+str(i)+'","italic": "false","color":"gray"}')
        # display higher levels with the number (this is NOT how vanilla does it. but it's a better QoL)
        if score $lvl smithed.item matches 11..:
            storage.lore.lvl = ('{"score":{"objective":"smithed.item","name":"$lvl","italic": "false","color":"gray"}}')

    # sign trick to concat name and level into single string
    data modify block -30000000 0 1603 front_text.messages[0] set value '[{"nbt":"lore.ench","storage":"smithed.item:main","interpret":true}," ",{"nbt":"lore.lvl","storage":"smithed.item:main","interpret":true}]'
    data modify storage smithed.item:main item.tag.display.Lore prepend from block -30000000 0 1603 front_text.messages[0]

    if data storage smithed.item:main 'enchantments'[] function ./enchantments/loop
