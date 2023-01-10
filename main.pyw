import pyglet

from source.gui.widget.Button import Button
from source.gui.window import Window
from source.gui.scene.debug import FPSCounterScene
from source.gui.scene import HelloWorldScene

# Créer une fenêtre
window = Window(resizable=True, visible=False)

button_normal_image = pyglet.image.load("./assets/test_button_normal.png")
button_hover_image = pyglet.image.load("./assets/test_button_hover.png")
button_click_image = pyglet.image.load("./assets/test_button_clicking.png")

# performance and button test

hello_world_scene = HelloWorldScene()

for x in range(10):
    for y in range(10):
        button = Button(
            200 + y * 50, x * 50, 50, 50,
            text=f"{x}-{y}",
            font_size=10,
            on_release=lambda self, *a, **b: setattr(self, "width", self.width + 10),
            normal_image=button_normal_image,
            hover_image=button_hover_image,
            click_image=button_click_image
        )
        hello_world_scene.add_widget(button)

fps_counter_scene = FPSCounterScene()

window.add_scene(hello_world_scene, fps_counter_scene)

# Lance la fenêtre
window.set_visible(True)
pyglet.app.run()
