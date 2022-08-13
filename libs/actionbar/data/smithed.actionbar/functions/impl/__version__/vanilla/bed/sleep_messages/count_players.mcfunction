
execute store result score $total_players smithed.actionbar.temp if entity @a[x=0]
execute store result score $sleeping_players smithed.actionbar.temp if entity @a[x=0,nbt=!{SleepTimer:0s}]
