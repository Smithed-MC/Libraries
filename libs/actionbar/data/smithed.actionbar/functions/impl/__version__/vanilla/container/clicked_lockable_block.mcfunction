advancement revoke @s only smithed.actionbar:impl/__version__/vanilla/container/clicked_lockable_block

# find block that was clicked
scoreboard players set $ray smithed.actionbar.temp 50
execute anchored eyes positioned ^ ^ ^ run function smithed.actionbar:impl/__version__/vanilla/container/raycast
