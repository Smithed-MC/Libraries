<p align="center">
  <img width='50%' src="https://github.com/TheNuclearNexus/smithed/blob/master/public/official_smithed_library.png?raw=true">
</p>

# Prevent Agression

Every 10 ticks (0.5 seconds), hostile mobs that attack villagers are added to the smithed.prevent_aggression team. Entities with the smithed.entity tag are ignored, but can be added to the team with a separate command.
All mobs that naturally attack villagers are added to the team by default:

- zombie
- husk
- drowned
- zombie_villager
- pillager
- ravager
- vindicator
- vex
- illusioner

## Usage
[Documentation](https://docs.smithed.dev/libraries/prevent-aggression/)
## Downloading
You can download it from [here](https://smithed.net/packs/prevent-aggression)
or<br/>
You can build it from source using the [beet](https://github.com/mcbeet/beet)

### Building
```
$ pip install beet mecha
$ git clone https://github.com/Smithed-MC/Libraries
$ cd Libraries/prevent-agression
$ beet -s 'meta.libraries = ["prevent-agression"]'
```