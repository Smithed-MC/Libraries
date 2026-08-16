
schedule function smithed.wiki:v0.1.0/technical/tick 1 replace
execute as @a[scores={smithed.wiki.use_book=1..}] run function smithed.wiki:v0.1.0/wiki/use_book


                    scoreboard players enable @a smithed.wiki.example.trigger
                    execute as @a[scores={smithed.wiki.example.trigger=1000..}] run function smithed.wiki:v0.1.0/wiki/example/change_page
                
