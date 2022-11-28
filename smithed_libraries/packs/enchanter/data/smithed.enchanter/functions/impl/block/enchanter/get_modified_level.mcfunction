from ../../technical/binomial_random import randomInt
from bolt_expressions import Scoreboard, Data
data_obj = Scoreboard("smithed.data")
entity = Data.entity("@s")


function ./get_levels

E = 10

for id in [ "t_lvl", "m_lvl", "b_lvl"]:
    mB = data_obj["m" + id[0].upper() + id[1:]]
    B = data_obj[id]
    R1 = randomInt(0, E//4)
    R2 = randomInt(0, E//4)
    mB = min(B + R1 + R2 + 1, 30)
    
    modifier = randomInt(85,115)
    mB = max(min(mB + 1 * 100 / modifier, 30), 1)

    entity.ArmorItems[3].tag.smithed.level[id] = mB

    # tellraw @a [mB.holder, ": ", {"score": {"name": mB.holder, "objective": mB.obj}}]
