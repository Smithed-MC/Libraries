<p align="center">
  <img width='50%' src="https://github.com/TheNuclearNexus/smithed/blob/master/public/official_smithed_library.png?raw=true">
</p>

# Actionbar
This library helps multiple data packs manage the actionbar by aggregating usage by priority. This allows persistent messages to display without interrupting more urgent notification type messages.

This pack also allows vanilla survival actionbar messages to be shown over other actionbar messages. This includes:
* Not being able to sleep in a bed
* Sleeping status (i.e. sleep percentage and sleeping through the night messages)
* Trying to open a locked container
## Usage
For usage information, see the [documentation](https://docs.smithed.dev/libraries/actionbar)
## Downloading
You can download this library from [the website](https://smithed.net/packs/actionbar)  
or  
You can build it from source using [beet](https://github.com/mcbeet/beet)

### Building
```
$ pip install beet mecha
$ git clone https://github.com/Smithed-MC/Libraries
$ cd Libraries/actionbar
$ beet -s 'meta.libraries = ["actionbar"]'
```
