import pyglet

from source.gui.scene.abc import Scene
from source.gui.widget import Text, FPSDisplay, Button
from source.gui.window import Window

# Test Scene


class TestScene(Scene):
    def __init__(self, window: "Window"):
        super().__init__(window)

        # loading resource

        normal_texture = pyglet.image.load("./assets/image/button/test_button_normal.png")
        hover_texture = pyglet.image.load("./assets/image/button/test_button_hover.png")
        click_texture = pyglet.image.load("./assets/image/button/test_button_clicking.png")

        button_atlas = pyglet.image.atlas.TextureAtlas()
        normal_region = button_atlas.add(normal_texture)
        hover_region = button_atlas.add(hover_texture)
        click_region = button_atlas.add(click_texture)

        self.background_batch = pyglet.graphics.Batch()
        self.label_batch = pyglet.graphics.Batch()

        # the widgets

        self.add_widget(FPSDisplay)
        label = self.add_widget(
            Button,

            x=0.5, y=0.5, width=0.5, height=0.5,

            texture_normal=normal_region,
            texture_hover=hover_region,
            texture_click=click_region,

            label_text="Hello World !",

            background_batch=self.background_batch,
            label_batch=self.label_batch,
        )

        label.on_pressed = lambda button, modifiers: print("pressed", label, button, modifiers)
        label.on_release = lambda button, modifiers: print("release", label, button, modifiers)

    def on_draw(self):
        self.background_batch.draw()
        self.label_batch.draw()




# Create a new window
window = Window(resizable=True, vsync=False)
window.add_scene(TestScene)

# Start the event loop
pyglet.app.run(interval=0)

