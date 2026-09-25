# @public

# resets player's title scores so they can see any new title
# @s = player that has a freeze score of 1
# located at @s
# run from technical/tick


scoreboard players reset @s smithed.title.freeze
scoreboard players set @s smithed.title.priority 0
