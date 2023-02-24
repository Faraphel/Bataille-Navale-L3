import pyglet

from source.gui.scene import MainMenu, Result
from source.gui.window import GameWindow


# Create a new window
window = GameWindow(resizable=True, vsync=False, caption="Bataille Navale")
window.set_minimum_size(720, 480)
window.add_scene(MainMenu)

# Start the event loop
pyglet.app.run(interval=0)

