scoreboard objectives add smithed.inv_change dummy

data modify storage smithed.crafter:input flags set value []
schedule function smithed.crafter:impl/technical/slow_tick 5t replace
schedule function smithed.crafter:impl/technical/tick 1t replace
