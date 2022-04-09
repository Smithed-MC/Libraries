####################
# Shapeless recipes for crafting
####################

function smithed.crafter:impl/__version__/block/table/crafting/shapeless_recipes/simplify
execute store result score count smithed.data if data storage smithed.crafter:main root.temp.shapeless_crafting_input[]

function #smithed.crafter:event/shapeless_recipes
