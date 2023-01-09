from typing import Callable, Optional, TYPE_CHECKING

import pyglet

from source.gui.widget.base import Widget
from source.utils import in_bbox

if TYPE_CHECKING:
    from source.gui.scene.base import Scene
    from source.gui.window import Window


class Button(Widget):
    __slots__ = ("_x", "_y", "_width", "_height", "_text", "on_press", "on_release", "_normal_image", "_hover_image",
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
                 *args, **kwargs
                 ):

        # TODO: use batch
        # TODO: make the label centered in the button
        # TODO: use texture bin and animation to simplify the image handling ?

        self.label = pyglet.text.Label(*args, **kwargs)

        self._hovering = False
        self._normal_sprite = pyglet.sprite.Sprite(normal_image)
        self._hover_sprite = pyglet.sprite.Sprite(hover_image)

        self.on_press: Optional[Callable[["Window", "Scene", int, int, int, int], None]] = on_press
        self.on_release: Optional[Callable[["Window", "Scene", int, int, int, int], None]] = on_release

        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height

    # function

    def _update_sprite_size(self, x: int = None, y: int = None, width: int = None, height: int = None):
        for sprite in self._normal_sprite, self._hover_sprite:
            sprite.update(
                x=x,
                y=y,
                scale_x=None if width is None else width / sprite.width,
                scale_y=None if height is None else height / sprite.height,
            )

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
    def x(self, value: int):
        self._x = value
        self.label.x = value
        self._update_sprite_size(x=value)

    @property
    def y(self) -> int: return self._y

    @y.setter
    def y(self, value: int):
        self._y = value
        self.label.y = value
        self._update_sprite_size(y=value)

    @property
    def width(self) -> int: return self._width

    @width.setter
    def width(self, value: int):
        self._width = value
        self.label.width = value
        self._update_sprite_size(width=value)

    @property
    def height(self) -> int: return self._height

    @height.setter
    def height(self, value: int):
        self._height = value
        self.label.height = value
        self._update_sprite_size(height=value)

    # event

    def on_mouse_press(self, window: "Window", scene: "Scene", x: int, y: int, button: int, modifiers: int):
        if not in_bbox((x, y), self.bbox): return
        if self.on_press is not None: self.on_press(window, scene, x, y, button, modifiers)

    def on_mouse_release(self, window: "Window", scene: "Scene", x: int, y: int, button: int, modifiers: int):
        if not in_bbox((x, y), self.bbox): return
        if self.on_release is not None: self.on_release(window, scene, x, y, button, modifiers)

    def on_mouse_motion(self, window: "Window", scene: "Scene", x: int, y: int, dx: int, dy: int):
        self._hovering = in_bbox((x, y), self.bbox)

    def on_draw(self, window: "Window", scene: "Scene"):
        if (bg := self.background_sprite) is not None:
            bg.draw()

        self.label.draw()
