# check if this is a server or a singleplayer world
execute unless score $is_server smithed.actionbar.const matches 1.. run function smithed.actionbar:impl/__version__/vanilla/bed/sleep_messages/get_player_count

# get required percentage
execute store result score $sleeping_percent smithed.actionbar.temp run gamerule playersSleepingPercentage
# if over 100, send can't pass night message
execute if score $sleeping_percent smithed.actionbar.temp matches 101.. run data modify storage smithed.actionbar:input message set value {raw:"",priority:'notification',freeze:10}

execute if score $is_server smithed.actionbar.temp matches 1 if score $sleeping_percent smithed.actionbar.temp matches ..100 run function smithed.actionbar:impl/__version__/vanilla/bed/sleep_messages/count_players
