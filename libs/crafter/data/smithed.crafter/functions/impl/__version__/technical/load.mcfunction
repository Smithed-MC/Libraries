scoreboard objectives add smithed.inv_change dummy

data modify storage smithed.crafter:main flags set value []
schedule function smithed.crafter:impl/__version__/technical/slow_tick 5t replace
