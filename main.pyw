import pyglet

from source.gui.scene import MainMenu
from source.gui.window import Window


# Create a new window
window = Window(resizable=True, vsync=True)
window.add_scene(MainMenu)

# Start the event loop
pyglet.app.run(interval=0)

