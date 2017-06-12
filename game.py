import tdl

from player import Player

tdl.set_font('terminal8x8_gs_ro.png')
console = tdl.init(40, 30, 'lunch break roguelike')

p = Player()
p.position = 10, 10

map = [
    ['#', '#', '#', '#'],
    ['#', '', '', '#'],
    ['#', '', '', '#'],
    ['#', '', '', '#'],
    ['#', '', '', '#'],
    ['#', '', '', '#'],
    ['#', '', '', '#'],
    ['#', '#', '#', '#']
]


running = True
while running:
    console.clear()


    for y in range(8):
        for x in range(4):
            if map[y][x]:
                console.draw_char(x, y, map[y][x])

    p.draw(console)

    tdl.flush()

    for event in tdl.event.get():
        p.handle_events(event)

        if event.type == 'QUIT':
            running = False
