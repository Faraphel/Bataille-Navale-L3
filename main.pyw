import pyglet

from source.gui.scene import MainMenuScene
from source.gui.scene.debug import FPSScene
from source.gui.scene.test import TestButtonScene, TestLabelScene
from source.gui.window import Window

# Create a new window
window = Window(resizable=True, vsync=True)
# window.add_scene(TestButtonScene())
# window.add_scene(TestLabelScene())
window.add_scene(MainMenuScene())
window.add_scene(FPSScene())

# Start the event loop
pyglet.app.run(interval=0)

