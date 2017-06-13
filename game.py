import tdl

from player import Player

tdl.set_font('terminal32x32_gs_ro.png')
console = tdl.init(40, 30, 'lunch break roguelike')

p = Player()
p.position = 10, 10

map = tdl.Console(40, 30)
map.draw_char(0, 0, '#')

running = True
while running:
    console.clear()


    console.blit(map)
    p.draw(console)

    tdl.flush()

    for event in tdl.event.get():
        p.handle_events(event)

        if event.type == 'QUIT':
            running = False
