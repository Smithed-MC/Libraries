| Input Name         | Input Type | Input Source | Input Objective/Path | 
| ---                | ---        | ---          | ---                  | 
| "Amount of damage" | score      | @s           | smithed.damage       | 


This function applies the specified amount of damage in half-hearts to the executing entity.
```mcfunction
scoreboard players set @s smithed.damage 3    # Does 1.5 damage (3 half-hearts)
function #smithed.damage:entity/apply         # Apply the damage
```
To apply damage that respects armor, use their specific commands
`function #smithed.damage:entity/apply/armor`: Respects armor, protection, and resistance
`function #smithed.damage:entity/apply/explosion`: Respects the same as `armor` but blast protection as well
`function #smithed.damage:entity/apply/projectile`: Respects the same as `armor` but projectile protection as well
