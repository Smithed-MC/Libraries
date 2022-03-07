# Smithed Actionbar:
*Actionbar compatibility between datapacks*

This library helps manage usage of the actionbar by aggregating usage by priority. This allows persistent messages to display without interrupting more urgent notification type messages.

## Usage

Instead of using `/title` to display the message, take the original string you were going to display and use it in this command:

-> Persistent Compass HUD

```mcfunction
data modify storage smithed.actionbar:message input set value {raw:'X Y Z', priority: 'persistent'}
```

-> Notification

```mcfunction
data modify storage smithed.actionbar:message input set value {json:'{"text":"You cannot complete this action!", "color": "red"}', priority: 'notification'}
```

Once you have the `storage` set how you like, you can run the public api function to process the message.

```mcfunction
function #smithed:actionbar/message
```

Priorities are set via specific strings.

- `override`: This is the highest priority and will always override the current message, no matter what.
- `notification`: This is for brief, non-repeating, notification type messages, such as the vanilla "You can't sleep now" message.
- `conditional`: This should be used for any message which will display constantly on a condition. A good example is displaying a compass HUD while you hold a compass or showcasing the amount of XP in a nearby tank. This doesn't include any persistent messages which toggle via a config option!
- `persistent`: This is the lowest priority message and is designated for messages which always displays (or displays continously if a config value is set). You can think of this as a custom ui display such as in Manic or even the Vanilla Tweaks coordinate HUD which always displays.

Additionally, you can also set a `freeze` field in the storage space. This will deteremine how long your message should be protected. By default, when using `notification`, this field is set to 20. Otherwise, this field is set to 2 (consider this 1, but for optimization, it's 2).

```mcfunction
data modify storage smithed.actionbar:message input set value {raw:'Random Event!', priority: 'notification', freeze: 30}
```

The freeze value has a min value of 0 and a max value of 50.

## Other info

This pack also reimplements as many vanilla actionbars as reasonable. As of now, this includes:

- Not being able to sleep in a bed
