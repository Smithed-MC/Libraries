schedule clear smithed.wiki:v0.1.0/technical/tick
execute if score #{{ project_id }}.major load.status matches 0 if score #{{ project_id }}.minor load.status matches 1 if score #{{ project_id }}.patch load.status matches 0 run function smithed.wiki:v0.1.0/technical/load
