schedule clear smithed.wiki:v0.1.0/technical/tick
execute if score #smithed.wiki.major load.status matches 0 if score #smithed.wiki.minor load.status matches 1 if score #smithed.wiki.patch load.status matches 0 run function smithed.wiki:v0.1.0/technical/load
