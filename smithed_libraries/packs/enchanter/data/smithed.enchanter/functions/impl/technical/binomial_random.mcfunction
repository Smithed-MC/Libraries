from bolt_expressions import Scoreboard
from ./path import path
data_obj = Scoreboard("smithed.data")

trials = data_obj["#trials"]
out = data_obj["$out"]


inTrials = data_obj["$trials"]
inChance = data_obj["$chance"]

count = 0
def randomInt(min, max):
    global inTrials
    global inChance
    inTrials = max - min
    inChance = 500000000
    function smithed.enchanter:impl/technical/binomial_random
    global count
    output = data_obj[f"out_{count}"]
    output = out + min
    count += 1
    return output


trials = inTrials
out = 0


if score inTrials.scoreholder inTrials.objective matches 1..1000 if score inChance.scoreholder inChance.objective matches 1..1000000000 function smithed.enchanter:impl/technical/binomial_loop:

    merge predicate smithed.enchanter:random/score_ppb {
        "condition": "minecraft:value_check",
        "value": {
            "min": 1,
            "max": 1000000000
        },
        "range": {
            "min": 1,
            "max": {
                "type": "minecraft:score",
                "score": inChance.objective,
                "target": {
                    "type": "minecraft:fixed",
                    "name": inChance.scoreholder
                }
            }
        }
    }

    # say loop
    if predicate smithed.enchanter:random/score_ppb function smithed.enchanter:impl/technical/binomial_loop/pass:
        out += 1
        # say pass
    trials -= 1
    if score trials.scoreholder trials.objective matches 1.. run function smithed.enchanter:impl/technical/binomial_loop

    