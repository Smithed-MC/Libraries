# find bed block that was clicked
scoreboard players set $ray smithed.actionbar.temp 50
execute anchored eyes positioned ^ ^ ^ run function smithed.actionbar:impl/__version__/vanilla/bed/sleep_issues/raycast
