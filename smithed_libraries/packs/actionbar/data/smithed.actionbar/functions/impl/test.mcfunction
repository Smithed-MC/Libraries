# execute if data storage smithed.actionbar:data block{Lock:'"test1"'} run data modify storage smithed.actionbar:input message set value {json:'{"translate":"sleep.skipping_night"}',priority:'notification',freeze:20}
# execute if data storage smithed.actionbar:data block{Lock:'"test2"'} run data modify storage smithed.actionbar:input message set value {}
# execute if data storage smithed.actionbar:data block{Lock:'"test3"'} run scoreboard players set $locked smithed.actionbar.temp 0
