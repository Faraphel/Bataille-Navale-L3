import pyglet

from source.gui.scene.abc import Scene
from source.gui.widget import Text, FPSDisplay, Button
from source.gui.window import Window

# Test Scene


class TestScene(Scene):
    def __init__(self, window: "Window"):
        super().__init__(window)

        # loading resource

        texture_normal = pyglet.image.load("./assets/image/button/test_button_normal.png")
        texture_hover = pyglet.image.load("./assets/image/button/test_button_hover.png")
        texture_click = pyglet.image.load("./assets/image/button/test_button_clicking.png")

        button_atlas = pyglet.image.atlas.TextureAtlas()
        region_normal = button_atlas.add(texture_normal)
        region_hover = button_atlas.add(texture_hover)
        region_click = button_atlas.add(texture_click)

        self.background_batch = pyglet.graphics.Batch()
        self.label_batch = pyglet.graphics.Batch()

        # the widgets

        self.fps_display = self.add_widget(FPSDisplay)

        label = self.add_widget(
            Button,

            x=0.5, y=0.5, width=0.5, height=0.5,

            texture_normal=region_normal,
            texture_hover=region_hover,
            texture_click=region_click,

            label_text="Hello World !",

            background_batch=self.background_batch,
            label_batch=self.label_batch,
        )

        label.on_pressed = lambda button, modifiers: print("pressed", label, button, modifiers)
        label.on_release = lambda button, modifiers: print("release", label, button, modifiers)

    def on_draw(self):
        self.background_batch.draw()
        self.label_batch.draw()
        self.fps_display.draw()


# Create a new window
window = Window(resizable=True, vsync=False)
window.add_scene(TestScene)

# Start the event loop
pyglet.app.run(interval=0)

