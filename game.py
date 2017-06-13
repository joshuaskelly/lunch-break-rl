import tdl

from scene import Scene

tdl.set_font('terminal32x32_gs_ro.png')
console = tdl.init(40, 30, 'lunch break roguelike')

scene = Scene()

running = True
while running:
    # Draw the scene
    console.clear()
    scene.draw(console)
    tdl.flush()

    # Handle input/events
    for event in tdl.event.get():
        scene.handle_events(event)

        if event.type == 'QUIT':
            running = False
