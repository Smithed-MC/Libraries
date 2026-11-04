scoreboard objectives add smithed.title.temp dummy
scoreboard objectives add smithed.title.const dummy
scoreboard objectives add smithed.title.priority dummy
scoreboard objectives add smithed.title.freeze dummy


scoreboard players set $default.freeze smithed.title.const 20
scoreboard players set $max.freeze smithed.title.const 50
scoreboard players set $min.freeze smithed.title.const 0
scoreboard players set #100 smithed.title.const 100

schedule function smithed.title:impl/technical/tick 1t
