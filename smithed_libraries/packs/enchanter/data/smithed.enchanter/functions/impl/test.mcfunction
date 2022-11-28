advancement revoke @s only smithed.enchanter:impl/test
tellraw @a ["Before: ", {"nbt":"Passengers[0].UUID","entity":"@e[tag=interact,sort=nearest,limit=1]"}]
tellraw @a "---------------------------------"
at @e[tag=interact,sort=nearest,limit=1] kill @e[tag=temp,sort=nearest,limit=1]
schedule function ./test2 5t:
    at TheNuclearNexus tellraw @a ["After Kill: ",{"nbt":"Passengers[0].UUID","entity":"@e[tag=interact,sort=nearest,limit=1]"}]
schedule function ./test3 5s:
    at TheNuclearNexus tellraw @a ["After Close: ",{"nbt":"Passengers[0].UUID","entity":"@e[tag=interact,sort=nearest,limit=1]"}]
