execute unless block ~ ~ ~ barrel run function smithed.crafter:impl/__version__/block/table/break

execute if block ~ ~ ~ barrel[open=true] run function smithed.crafter:impl/__version__/block/table/open_tick

execute if block ~ ~ ~ barrel[open=false] if entity @s[tag=smithed.open] run function smithed.crafter:impl/__version__/block/table/reset

execute if block ~ ~-1 ~ hopper run data merge block ~ ~-1 ~ {TransferCooldown:12}