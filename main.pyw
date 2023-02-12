import pyglet

from source.gui.scene.abc import Scene
from source.gui.widget import Text, FPSDisplay
from source.gui.window import Window

# Test Scene


class TestScene(Scene):
    def __init__(self, window: "Window"):
        super().__init__(window)

        self.add_widget(FPSDisplay)
        label = self.add_widget(Text, text="Hello World !", x=0.5, y=0.5, width=0.5, height=0.5, anchor_x="center", anchor_y="center")

        label.on_pressed = lambda self, button, modifiers: print("pressed", self, button, modifiers)
        label.on_release = lambda self, button, modifiers: print("release", self, button, modifiers)


# Create a new window
window = Window(resizable=True, vsync=False)
window.add_scene(TestScene)

# Start the event loop
pyglet.app.run(interval=0)

