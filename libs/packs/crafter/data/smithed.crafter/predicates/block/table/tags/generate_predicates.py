import io, os, json

outputFolder = "B:/Projects/Minecraft/SmithedCrafter/datapack/data/smithed/predicates/crafter/block/table/tags/"

pathToFunction = "B:/Projects/Minecraft/SmithedCrafter/datapack/data/smithed/functions/crafter/block/table/crafting/input/query_tags.mcfunction"

os.remove(pathToFunction)
functionFile = open(pathToFunction, "w+")

tags = [
    "acacia_logs",
    "anvil",
    "arrows",
    "axolotl_tempt_items",
    "banners",
    "beacon_payment_items",
    "beds",
    "birch_logs",
    "boats",
    "buttons",
    "candles",
    "carpets",
    "cluster_max_harvestables",
    "coals",
    "coal_ores",
    "copper_ores",
    "creeper_drop_music_discs",
    "crimson_stems",
    "dark_oak_logs",
    "diamond_ores",
    "doors",
    "emerald_ores",
    "fences",
    "fishes",
    "flowers",
    "fox_food",
    "freeze_immune_wearables",
    "gold_ores",
    "ignored_by_piglin_babies",
    "iron_ores",
    "jungle_logs",
    "lapis_ores",
    "leaves",
    "lectern_books",
    "logs",
    "logs_that_burn",
    "music_discs",
    "non_flammable_wood",
    "oak_logs",
    "occludes_vibration_signals",
    "piglin_food",
    "piglin_loved",
    "piglin_repellents",
    "planks",
    "rails",
    "redstone_ores",
    "sand",
    "saplings",
    "signs",
    "slabs",
    "small_flowers",
    "soul_fire_base_blocks",
    "spruce_logs",
    "stairs",
    "stone_bricks",
    "stone_crafting_materials",
    "stone_tool_materials",
    "tall_flowers",
    "trapdoors",
    "walls",
    "warped_stems",
    "wooden_buttons",
    "wooden_doors",
    "wooden_fences",
    "wooden_pressure_plates",
    "wooden_slabs",
    "wooden_stairs",
    "wooden_trapdoors",
    "wool",
]

functionFile.write(
    "data modify storage smithed.crafter:main root.temp.item_tag set value []\n\n"
)
for f in tags:
    file = open(outputFolder + f + ".json", "w+")
    file.write(
        json.dumps(
            {
                "condition": "minecraft:entity_properties",
                "entity": "this",
                "predicate": {"equipment": {"mainhand": {"tag": "minecraft:" + f}}},
            },
            indent=4,
        )
    )
    file.close()

    functionFile.write(
        f'execute if predicate smithed.crafter:impl/__version__/block/table/tags/{f} run data modify storage smithed.crafter:main root.temp.item_tag append value "#minecraft:{f}"\n'
    )
functionFile.write(f"\nfunction #smithed.crafter:query_tags")
