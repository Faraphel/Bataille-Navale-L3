import pyglet

from source.gui.scene import Scene
from source.gui.widget import Text, FPSDisplay
from source.gui.window import Window

# Test Scene


class TestScene(Scene):
    def __init__(self, window: "Window", *args, **kwargs):
        super().__init__(window, *args, **kwargs)

        self.add_widget(FPSDisplay)
        self.add_widget(Text, text="Hello World !")


# Create a new window
window = Window(resizable=True, vsync=False)
window.add_scene(TestScene)

# Start the event loop
pyglet.app.run(interval=0)

