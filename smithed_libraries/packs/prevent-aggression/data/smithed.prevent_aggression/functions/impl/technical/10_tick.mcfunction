# @doc team
# Every 10 ticks (0.5 seconds), hostile mobs that attack villagers are added to the `smithed.prevent_aggression` team.
# Entities with the `smithed.entity` tag are ignored, but can be added to the team with a separate command.  
# All mobs that naturally attack villagers are added to the team by default:  
# * zombie
# * husk
# * drowned
# * zombie_villager
# * pillager
# * ravager
# * vindicator
# * evoker
# * vex
# * illusioner  
# ## Preventing Aggression
# Mobs that should not be tracked or damaged by hostile mobs should be added to the same team.
# This library is made specifically so technical villagers are not attacked by mobs.
# Other mobs can be added to the team, but there is no guarantee that it won't be attacked by hostile mobs.
# Adding the team can be done upon summoning the mob or afterwards.
# ### Example Usage
# `function: example:summon_mobs`
# ```mcfunction
# # summon custom villager that isn't tracked by hostiles
# summon villager ~ ~ ~ {
#   Team: "smithed.prevent_aggression", 
#   Tags: ["my_custom_mob"]
# }
# # summon custom zombie that respects the aggression rule
# # by default, a mob with the smithed.entity tag doesn't get added to the team, but it can be done manually
# summon zombie ~ ~ ~ {
#   Tags: ["smithed.entity", "my_custom_zombie"],
#   Team: "smithed.prevent_aggression"
# }
# ```
# This is the recommended way to create a villager that isn't tracked by hostiles.
# 
# ---  
# `function: example:protect_village`
# ```{code-block} mcfunction
# :force:
# # make villagers safe while nearby a guardian player
# tag @e[type=villager] remove protected
# execute
#   at @a[tag=guardian]
#   run tag @e[type=villager,tag=!smithed.entity,distance=..32] add protected
# team join smithed.prevent_aggression @e[type=villager,tag=protected,team=!smithed.prevent_aggression]
# team leave smithed.prevent_aggression @e[type=villager,tag=!protected,team=smithed.prevent_aggression]
# 
# # loop this function every second
# schedule function example:protect_village 20t replace
# ```
# This use case is not the intended use of this library, 
# but it is a possible option shown to demonstrate adding the team to pre-existing mobs.

team join smithed.prevent_aggression @e[type=#smithed.prevent_aggression:mobs,tag=!smithed.entity,team=!smithed.prevent_aggression]

schedule function smithed.prevent_aggression:impl/technical/10_tick 10t replace
