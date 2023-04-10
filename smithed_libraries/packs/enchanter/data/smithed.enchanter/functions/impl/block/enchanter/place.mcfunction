from bolt_expressions import Scoreboard, Data
enchSeed = Scoreboard("smithed.enchanter.seed")
entity = Data.entity("@s")

align xyz run summon armor_stand ~.5 ~ ~.5 {
    Tags: ["smithed.entity", "smithed.block", "smithed.enchanter"],
    ArmorItems:[{},{},{},{
        id: "minecraft:enchanting_table",
        Count: 1,
        tag: {
            smithed: {
                
            }
        }
    }]
}

align xyz positioned ~.5 ~ ~.5 as @e[tag=smithed.enchanter,dx=0] at @s run function ./set_seed:
    store result score @s smithed.enchanter.seed run time query gametime
    enchSeed["@s"] += entity.Pos[0] / 100
    enchSeed["@s"] += entity.Pos[1] / 100
    enchSeed["@s"] += entity.Pos[2] / 100
    enchSeed["@s"] -= entity.UUID[0] / 100
    enchSeed["@s"] %= entity.UUID[1] / 100
    enchSeed["@s"] += entity.UUID[2] / 100
    enchSeed["@s"] = max(enchSeed["@s"], enchSeed["@s"] * -1)
setblock ~ ~ ~ barrel[facing=up]{CustomName:'{"translate":"block.smithed.enchanter.gui","font":"smithed.enchanter:gui","color":"white","with":[{"translate":"block.smithed.enchanter","color":"#3F3F3F","font":"minecraft:default"}]}'}