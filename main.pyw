import pyglet

from source.gui.scene.debug import FPSScene
from source.gui.scene.test import HelloWorldScene
from source.gui.window import Window


# Create a new window
window = Window(resizable=True, vsync=False)
window.add_scene(HelloWorldScene(), FPSScene())

# Start the event loop
pyglet.app.run(interval=0)

