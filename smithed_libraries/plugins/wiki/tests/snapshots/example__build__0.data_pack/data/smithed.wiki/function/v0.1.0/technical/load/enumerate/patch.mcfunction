execute if score #{{ project_id }}.patch load.status matches ..0 unless score #{{ project_id }}.patch load.status matches 0 run function smithed.wiki:v0.1.0/technical/load/enumerate/set_version
