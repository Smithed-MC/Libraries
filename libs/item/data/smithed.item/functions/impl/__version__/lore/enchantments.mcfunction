from bolt_expressions import Scoreboard, Data
data_obj = Scoreboard("smithed.data")
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
    storage.temp = storage.enchantments[-1]
    data remove storage smithed.item:main 'enchantments'[-1]
    storage.lore.lvl = storage.temp.lvl
    data_obj["$lvl"] = storage.lore.lvl

    execute function ./enchantments/loop/find_ench:
        for e in enchantments:
            if data storage smithed.item:main temp{id: e}:
                storage.lore.ench = ('{"translate":"enchantment.'+e.replace(':','.')+'","italic": "false","color":"gray"}')
        function #smithed.item:event/build_custom

    execute function ./enchantments/loop/find_level:
        if score $lvl smithed.data matches 1 function ./enchantments/loop/special_level:
            storage.lore.lvl = ('{"translate":"enchantment.level.1","italic": "false","color":"gray"}')
            only_one_level =['minecraft:aqua_affinity','minecraft:channeling','minecraft:riptide','minecraft:curse_of_binding','minecraft:curse_of_vanishing','minecraft:flame','minecraft:infinity','minecraft:mending','minecraft:multishot']
            for e in only_one_level:
                if data storage smithed.item:main temp{id: e}:
                    storage.lore.lvl = ''
        for i in range(2,11):
            if score $lvl smithed.data matches (i):
                storage.lore.lvl = ('{"translate":"enchantment.level.'+str(i)+'","italic": "false","color":"gray"}')
        if score $lvl smithed.data matches 11..:
            storage.lore.lvl = ('{"score":{"objective":"smithed.data","name":"$lvl","italic": "false","color":"gray"}}')

    data modify block -30000000 0 1603 Text1 set value '[{"nbt":"lore.ench","storage":"smithed.item:main","interpret":true}," ",{"nbt":"lore.lvl","storage":"smithed.item:main","interpret":true}]'
    data modify storage smithed.item:main item.tag.display.Lore prepend from block -30000000 0 1603 Text1

    if data storage smithed.item:main 'enchantments'[] function ./enchantments/loop