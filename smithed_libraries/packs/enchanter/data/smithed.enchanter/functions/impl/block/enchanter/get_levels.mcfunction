from bolt_expressions import Scoreboard
data_obj = Scoreboard("smithed.data")

count = 0
def randomInt(min, max):
    global count
    data_obj["$min"] = min
    data_obj["$max"] = max
    function smithed.enchanter:impl/technical/uniform_random
    out = data_obj[f"$out_{count}"]
    out = data_obj["$out"]
    count += 1
    return out
    
b = data_obj["b"]
base = data_obj["base"]
top_enchant_level = data_obj["t_lvl"]
mid_enchant_level = data_obj["m_lvl"]
bot_enchant_level = data_obj["b_lvl"]


function ./get_bookshelves  

base = randomInt(1,8) + (b / 2) + randomInt(0, b)

top_enchant_level = max(base / 3, 1)
mid_enchant_level = ((base * 2) / 3 + 1)
bot_enchant_level = max(b * 2, base)

# tellraw @a [
#     "Top: ", {"score":{"name":"t_lvl","objective":"smithed.data"}}, "\n",
#     "Mid: ", {"score":{"name":"m_lvl","objective":"smithed.data"}}, "\n",
#     "Bot: ", {"score":{"name":"b_lvl","objective":"smithed.data"}}
# ]