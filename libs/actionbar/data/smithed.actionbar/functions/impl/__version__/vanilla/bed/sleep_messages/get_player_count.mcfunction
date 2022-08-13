tag @s add smithed.actionbar.self
execute if entity @a[tag=!smithed.actionbar.self,limit=1] run scoreboard players set $is_server smithed.actionbar.const 1
tag @s remove smithed.actionbar.self
