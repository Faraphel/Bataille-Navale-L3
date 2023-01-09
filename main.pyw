import pyglet

from gui.window import Window
from gui.scene import HelloWorldScene, FPSCounterScene

# Créer une fenêtre
window = Window(resizable=True, visible=False)

window.add_scene(HelloWorldScene(), FPSCounterScene())

# Lance la fenêtre
window.set_visible(True)
pyglet.app.run()
