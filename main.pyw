import pyglet

from source.gui.scene import MainMenu
from source.gui.scene.abc import Scene
from source.gui.widget import FPSDisplay, Button, Image, Input
from source.gui.window import Window

# Test Scene


class TestScene(Scene):
    def __init__(self, window: "Window"):
        super().__init__(window)

        # loading resource

        texture_button_normal = pyglet.image.load("./assets/image/button/normal.png")
        texture_button_hover = pyglet.image.load("./assets/image/button/hovering.png")
        texture_button_click = pyglet.image.load("./assets/image/button/clicking.png")
        texture_input_normal = pyglet.image.load("assets/image/input/normal.png")
        texture_input_active = pyglet.image.load("./assets/image/input/active.png")
        texture_input_error = pyglet.image.load("./assets/image/input/error.png")

        texture_atlas = pyglet.image.atlas.TextureAtlas()
        region_button_normal = texture_atlas.add(texture_button_normal)
        region_button_hover = texture_atlas.add(texture_button_hover)
        region_button_click = texture_atlas.add(texture_button_click)
        region_input_normal = texture_atlas.add(texture_input_normal)
        region_input_active = texture_atlas.add(texture_input_active)
        region_input_error = texture_atlas.add(texture_input_error)

        self.background_batch = pyglet.graphics.Batch()
        self.label_batch = pyglet.graphics.Batch()

        # the widgets

        self.fps_display = self.add_widget(FPSDisplay, color=(255, 255, 255, 127))

        background = self.add_widget(
            Image,

            x=0, y=0, width=1, height=1,

            image=region_input_normal,
            batch=self.background_batch,
        )

        button = self.add_widget(
            Button,

            x=0.5, y=0.5, width=0.5, height=0.5,

            texture_normal=region_button_normal,
            texture_hover=region_button_hover,
            texture_click=region_button_click,

            label_text="Hello World !",

            background_batch=self.background_batch,
            label_batch=self.label_batch,
        )

        button.on_pressed = lambda button, modifiers: "pass"
        button.on_release = lambda button, modifiers: window.set_scene(TestScene2)

        input_ = self.add_widget(
            Input,

            x=0.1, y=0.2, width=0.4, height=0.1,

            texture_normal=region_input_normal,
            texture_active=region_input_active,
            texture_error=region_input_error,

            # 4 numéros de 1 à 3 chiffres séparés par des points (IP), optionnellement suivi
            # de deux points ainsi que de 1 à 5 chiffres (port)
            regex=r"\d{1,3}(\.\d{1,3}){3}(:\d{1,5})?",

            background_batch=self.background_batch,
            label_batch=self.label_batch,
        )

    def on_draw(self):
        self.background_batch.draw()
        self.label_batch.draw()
        self.fps_display.draw()


class TestScene2(Scene):
    def __init__(self, window: "Window"):
        super().__init__(window)

    def on_draw(self):
        self.window.clear()


# Create a new window
window = Window(resizable=True, vsync=False)
window.add_scene(MainMenu)

# Start the event loop
pyglet.app.run(interval=0)

