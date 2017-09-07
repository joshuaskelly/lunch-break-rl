# lunch-break-rl

Lunch Break Roguelike is a small game that is developed on Twitch during lunch!

[![Twitch](https://img.shields.io/badge/twitch-joshuaskelly-red.svg?colorB=4b367c)](https://www.twitch.tv/joshuaskelly) [![Python 3](https://img.shields.io/badge/python-3-blue.svg)](https://www.python.org/)

## Installation

```
$ pip install -r requirements.txt
```

## Running

You need to add a config.cfg file to the project root. It should look like:

```cfg
[ENGINE]
; Frame limit in frames per second
fps = 30

; Renderer to use. Options are ['GLSL', 'OPENGL', 'SDL']
renderer = OPENGL

; Font to use.
font = terminal32x32_gs_ro.png

[GAME]
; The length of a turn in seconds
turn = 2

[TWITCH]
; User name of Twitch account. Preferably an alternate from your main Twitch
; account.
Nickname = Nick

; OAuth token acquired from: http://twitchapps.com/tmi
Password = oauth:abcdefghijklmnopqrstuvwxyz0123

; Channel to listen to
Channel = channel

; Broadcaster display color. Default is orange (255, 163, 0).
BroadcasterColor = 255, 163, 0

; Subscriber color. Default is blue (41, 173, 255).
SubscriberColor = 41, 173, 255

; Viewer display color. Default is orange (255, 163, 0).
ViewerColor = 255, 163, 0

; Special viewer display color. Default is red (255, 0, 77).
SpecialViewerColor = 255, 0, 77

; List of special viewers names separated by newlines.
SpecialViewers =
    joshuaskelly
    gusanolocovg

```

## License

MIT

See the [license](./LICENSE) document for the full text.
