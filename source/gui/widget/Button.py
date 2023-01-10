from typing import Callable, Optional, TYPE_CHECKING

import pyglet

from source.gui.sprite import Sprite
from source.gui.widget.base import Widget
from source.utils import in_bbox

if TYPE_CHECKING:
    from typing import Self
    from source.gui.scene.base import Scene
    from source.gui.window import Window


class Button(Widget):
    __slots__ = ("on_press", "on_release", "_x", "_y", "_width", "_height", "_text", "_normal_image", "_hover_image",
                 "_hovering")

    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,

                 on_press: Optional[Callable] = None,
                 on_release: Optional[Callable] = None,
                 normal_image: pyglet.image.AbstractImage = None,
                 hover_image: pyglet.image.AbstractImage = None,

                 batch: pyglet.graphics.Batch = None,
                 group: pyglet.graphics.Group = None,

                 *args, **kwargs
                 ):

        # TODO: use batch
        # TODO: use texture bin and animation to simplify the image handling ?
        # TODO: add an image when the mouse click ?
        # TODO: make x, y, width, height, font_size optionally function to allow dynamic sizing

        # initialise the default value for the property
        self._x, self._y, self._width, self._height = x, y, width, height

        # the label used for the text
        self._label = pyglet.text.Label(
            anchor_x="center",
            anchor_y="center",
            *args, **kwargs
        )

        # hovering and background
        self._hovering = False

        self._normal_sprite = Sprite(normal_image)
        self._hover_sprite = Sprite(hover_image)

        # the event when the button is clicked
        self.on_press: Optional[Callable[["Self", "Window", "Scene", int, int, int, int], None]] = on_press
        self.on_release: Optional[Callable[["Self", "Window", "Scene", int, int, int, int], None]] = on_release

        # update the size of the widget
        self._update_size()

    # function

    def _update_size(self):
        for sprite in self._normal_sprite, self._hover_sprite:
            sprite.x = self.x
            sprite.y = self.y
            sprite.width = self.width
            sprite.height = self.height

        self._label.x = self.x + (self.width // 2)
        self._label.y = self.y + (self.height // 2)

    # button getter and setter

    @property
    def background_sprite(self) -> Optional[pyglet.sprite.Sprite]:
        return self._hover_sprite if self._hovering else self._normal_sprite

    @property
    def bbox(self) -> tuple[int, int, int, int]:
        return self.x, self.y, self.x + self.width, self.y + self.height

    # label getter and setter

    @property
    def x(self) -> int: return self._x

    @x.setter
    def x(self, x: int):
        self._x = x
        self._update_size()

    @property
    def y(self) -> int: return self._y

    @y.setter
    def y(self, y: int):
        self._y = y
        self._update_size()

    @property
    def width(self) -> int: return self._width

    @width.setter
    def width(self, width: int):
        self._width = width
        self._update_size()

    @property
    def height(self) -> int: return self._height

    @height.setter
    def height(self, height: int):
        self._height = height
        self._update_size()

    # event

    def on_mouse_press(self, window: "Window", scene: "Scene", x: int, y: int, button: int, modifiers: int):
        if not in_bbox((x, y), self.bbox): return
        if self.on_press is not None: self.on_press(self, window, scene, x, y, button, modifiers)

    def on_mouse_release(self, window: "Window", scene: "Scene", x: int, y: int, button: int, modifiers: int):
        if not in_bbox((x, y), self.bbox): return
        if self.on_release is not None: self.on_release(self, window, scene, x, y, button, modifiers)

    def on_mouse_motion(self, window: "Window", scene: "Scene", x: int, y: int, dx: int, dy: int):
        self._hovering = in_bbox((x, y), self.bbox)

    def on_draw(self, window: "Window", scene: "Scene"):
        if (bg := self.background_sprite) is not None: bg.draw()
        self._label.draw()
