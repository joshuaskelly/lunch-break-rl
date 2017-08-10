# lunch-break-rl

Lunch Break Roguelike is a small game that is developed on Twitch during lunch!

[![Twitch](https://img.shields.io/badge/twitch-joshuaskelly-red.svg?colorB=4b367c)](https://www.twitch.tv/joshuaskelly) [![Python 3](https://img.shields.io/badge/python-3-blue.svg)](https://www.python.org/)

## Running

You need to add a config.cfg file to the project root. It should look like:

```cfg
[ENGINE]
; Frame limit in frames per second
fps = 30

; Renderer to use. Options are ['GLSL', 'OPENGL', 'SDL']
renderer = OPENGL

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

```

## License

MIT

See the [license](./LICENSE) document for the full text.
