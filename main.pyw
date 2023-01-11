import pyglet

from source.gui.window import Window
from source.gui.scene.debug import FPSCounterScene
from source.gui.scene.test import ButtonScene

# Créer une fenêtre
window = Window(resizable=True, visible=False)

# performance and button test

button_scene = ButtonScene()
fps_counter_scene = FPSCounterScene()

window.add_scene(button_scene, fps_counter_scene)

# Lance la fenêtre
window.set_visible(True)
pyglet.app.run()
