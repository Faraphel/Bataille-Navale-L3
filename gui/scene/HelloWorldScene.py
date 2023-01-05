import pyglet

from gui.scene import Scene
from gui.window import Window


class HelloWorldScene(Scene):
    """
    This scene is a simple Hello World.

    You can type anything with the keyboard or use backspace to remove characters.
    The text is centered on the screen.
    """

    def __init__(self):
        self._backspace_hold_frame: int = 0

        self.label = pyglet.text.Label(
            "Hello World !",
            anchor_x="center",
            anchor_y="center"
        )

    def on_draw(self, window: Window) -> None:
        if window.keys[pyglet.window.key.BACKSPACE]:
            if self._backspace_hold_frame % 5 == 0: self.label.text = self.label.text[:-1]
            self._backspace_hold_frame += 1
        else:
            self._backspace_hold_frame = 0

        self.label.draw()

    def on_resize(self, window: Window, width: int, height: int) -> None:
        self.label.x = width // 2
        self.label.y = height // 2

    def on_text(self, window: Window, char: str):
        self.label.text += char
