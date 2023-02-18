import pyglet

from source.gui.scene import MainMenu
from source.gui.window import GameWindow

# Create a new window
window = GameWindow(resizable=True, vsync=True, caption="Bataille Navale")
window.add_scene(MainMenu)

# Start the event loop
pyglet.app.run(interval=0)

