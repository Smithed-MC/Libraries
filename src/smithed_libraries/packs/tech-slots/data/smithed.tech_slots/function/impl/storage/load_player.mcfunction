# grab from storage registry
$data modify storage smithed.tech_slots:data temp.current_modifiers set from storage smithed.tech_slots:data modifier_registry."$(UUID)"

# if in registry, return amount of modifiers
execute if data storage smithed.tech_slots:data temp.current_modifiers run return run data get storage smithed.tech_slots:data temp.current_modifiers

# if not in registry, create an entry
$data modify storage smithed.tech_slots:data modifier_registry."$(UUID)" set value []
return 0
