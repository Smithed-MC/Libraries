
                # Reset the player's score
scoreboard players reset @s smithed.wiki.use_book

                # Exit early if they didn't use a wiki book
execute unless predicate smithed.wiki:v0.1.0/technical/holding_book run return fail

                # Determine the ID of the book they used
data remove storage smithed.wiki:temp trigger_name
data modify storage smithed.wiki:temp trigger_name set from entity @s SelectedItem.components."minecraft:custom_data".smithed.wiki.trigger
execute unless data storage smithed.wiki:temp trigger_name run data modify storage smithed.wiki:temp trigger_name set from entity @s equipment.offhand.components."minecraft:custom_data".smithed.wiki.trigger

                # Display the book
function smithed.wiki:v0.1.0/wiki/use_book/macro with storage smithed.wiki:temp {}
