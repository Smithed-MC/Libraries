# display the message to the player
# @s = player that needs a new title shown
# location undefined; based on how the user calls the function
# run from message

# yes, if you define raw and json, you'll get 2 messages
#  i left this "bug" in so that folks catch this in testing

execute if data storage smithed.title:input message.subtitle_raw run title @s subtitle {"storage": "smithed.title:input", "nbt": "message.subtitle_raw"}
execute if data storage smithed.title:input message.subtitle_json run title @s subtitle {"storage": "smithed.title:input", "nbt": "message.subtitle_json", "interpret": true}

execute if data storage smithed.title:input message.title_raw run title @s title {"storage": "smithed.title:input", "nbt": "message.title_raw"}
execute if data storage smithed.title:input message.title_json run title @s title {"storage": "smithed.title:input", "nbt": "message.title_json", "interpret": true}


# copy freeze w/ bounds checking
scoreboard players operation @s smithed.title.freeze = $freeze smithed.title.temp 
scoreboard players operation @s smithed.title.freeze > $min.freeze smithed.title.const
scoreboard players operation @s smithed.title.freeze < $max.freeze smithed.title.const

# unless freeze is explicitly 0, copy priority
#  allows folks to let their messages disappear
#  prolly won't interact nicely w/ persistent messages
execute unless score @s smithed.title.freeze matches 0 run scoreboard players operation @s smithed.title.priority = $priority smithed.title.temp
