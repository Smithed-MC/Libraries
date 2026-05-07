
                    scoreboard players remove @s smithed.wiki.example.trigger 1000
                    execute store result storage smithed.wiki:temp page int 1 run scoreboard players get @s smithed.wiki.example.trigger
                    scoreboard players reset @s smithed.wiki.example.trigger
                    function smithed.wiki:v0.1.0/wiki/example/change_page/macro with storage smithed.wiki:temp {} 
                