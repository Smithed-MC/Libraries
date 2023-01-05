# @public

# @doc reset
# This function resets the current freeze and priority allowing you to display another message
# ```{admonition} ⚠️ Caution ⚠️
# :class: warning
# This api **will** disrupt other packs as it blatently resets the actionbar state.
# Do not use this in any normal circumstances, as it will break compatibility in most cases.
# ```

# resets player's actionbar scores so they can see any new actionbar
# @s = player that has a freeze score of 1
# located at @s
# run from technical/tick

scoreboard players reset @s smithed.actionbar.freeze
scoreboard players set @s smithed.actionbar.priority 0
