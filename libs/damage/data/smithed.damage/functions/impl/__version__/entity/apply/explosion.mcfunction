# @public

# rx97
#  adapted from TCC

# get values (x100)
execute store result score #10armor smithed.damage run attribute @s minecraft:generic.armor get 10
execute store result score #10toughness smithed.damage run attribute @s minecraft:generic.armor_toughness get 10
scoreboard players operation #damage smithed.damage = @s smithed.damage

#!dbg score "#10armor", smithed.damage
#!dbg score "#10toughness", smithed.damage
#!dbg score "#damage", smithed.damage

data modify storage smithed.damage: temp set from entity @s

# first armor and toughness
function smithed.damage:impl/__version__/entity/damage/armor/toughness

#!dbg score "#damage", smithed.damage

# then protection
function smithed.damage:impl/__version__/entity/damage/armor/protection

#!dbg score "#damage", smithed.damage

function smithed.damage:impl/__version__/entity/damage/armor/blast_protection

#!dbg score "#damage", smithed.damage

# finally resistance
function smithed.damage:impl/__version__/entity/damage/armor/resistance

#!dbg score "#damage", smithed.damage

# go back to same scale
scoreboard players operation @s smithed.damage /= 10 smithed.const

# apply new damage
execute if score @s smithed.damage matches 1.. run function smithed.damage:impl/__version__/entity/damage/apply
