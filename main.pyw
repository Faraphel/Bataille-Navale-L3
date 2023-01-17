import pyglet

from source.gui.scene.debug import FPSAbstractScene
from source.gui.scene.test import TestButtonScene, TestLabelScene
from source.gui.window import Window


# Create a new window
window = Window(resizable=True, vsync=False)
window.add_scene(TestButtonScene())
# window.add_scene(TestLabelScene())
window.add_scene(FPSAbstractScene())

# Start the event loop
pyglet.app.run(interval=0)

