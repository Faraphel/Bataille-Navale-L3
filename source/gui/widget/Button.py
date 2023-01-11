from typing import Callable, Optional, TYPE_CHECKING

import pyglet

from source.gui.sprite import Sprite
from source.gui.widget.base import AdaptativeWidget
from source.type import Percentage
from source.utils import in_bbox

if TYPE_CHECKING:
    from typing import Self
    from source.gui.scene.base import Scene
    from source.gui.window import Window


class Button(AdaptativeWidget):
    def __init__(self,

                 x: int | Percentage,
                 y: int | Percentage,
                 width: int | Percentage,
                 height: int | Percentage,

                 normal_image: pyglet.image.AbstractImage,
                 hover_image: pyglet.image.AbstractImage = None,
                 click_image: pyglet.image.AbstractImage = None,

                 on_press: Optional[Callable] = None,
                 on_release: Optional[Callable] = None,

                 *args, **kwargs
                 ):

        super().__init__(x, y, width, height)

        # TODO: use batch ?
        # TODO: use texture bin and animation to simplify the image handling ?
        # TODO: font_size dynamic sizing too ?

        # the label used for the text
        self._label = pyglet.text.Label(
            anchor_x="center", anchor_y="center",
            *args, **kwargs
        )

        # the button background
        self._hovering = False
        self._clicking = False

        self._sprite = Sprite(normal_image)

        self._normal_image = normal_image
        self._hover_image = hover_image if hover_image is not None else normal_image
        self._click_image = click_image if click_image is not None else normal_image

        # the event when the button is clicked
        self.on_press: Optional[Callable[["Self", "Window", "Scene", int, int, int, int], None]] = on_press
        self.on_release: Optional[Callable[["Self", "Window", "Scene", int, int, int, int], None]] = on_release

        # update the size of the widget
        self._update_size()

    # function

    def _update_sprite(self) -> None:
        self._sprite.image = self.background_image

    def _update_size(self):
        self._sprite.x = self.x
        self._sprite.y = self.y
        self._sprite.width = self.width
        self._sprite.height = self.height

        self._label.x = self.x + (self.width // 2)
        self._label.y = self.y + (self.height // 2)

    # button getter and setter

    @property
    def hovering(self) -> bool: return self._hovering

    @hovering.setter
    def hovering(self, hovering: bool):
        self._hovering = hovering
        self._update_sprite()

    @property
    def clicking(self) -> bool:
        return self._clicking

    @clicking.setter
    def clicking(self, clicking: bool):
        self._clicking = clicking
        self._update_sprite()

    @property
    def background_image(self) -> pyglet.image.AbstractImage:
        return (
            self._click_image if self._clicking
            else self._hover_image if self._hovering
            else self._normal_image
        )

    # label getter and setter

    @AdaptativeWidget.x.setter
    def x(self, x: int):
        super().x = x
        self._update_size()

    @AdaptativeWidget.y.setter
    def y(self, y: int):
        super().y = y
        self._update_size()

    @AdaptativeWidget.width.setter
    def width(self, width: int):
        super().width = width
        self._update_size()

    @AdaptativeWidget.height.setter
    def height(self, height: int):
        super().height = height
        self._update_size()

    # event

    def on_mouse_press(self, window: "Window", scene: "Scene", x: int, y: int, button: int, modifiers: int):
        if not in_bbox((x, y), self.bbox): return

        self.clicking = True

        if self.on_press is not None:
            self.on_press(self, window, scene, x, y, button, modifiers)

    def on_mouse_release(self, window: "Window", scene: "Scene", x: int, y: int, button: int, modifiers: int):
        old_clicking = self.clicking
        self.clicking = False

        if not in_bbox((x, y), self.bbox): return

        # if this button was the one hovered when the click was pressed
        if old_clicking and self.on_release is not None:
            self.on_release(self, window, scene, x, y, button, modifiers)

    def on_mouse_motion(self, window: "Window", scene: "Scene", x: int, y: int, dx: int, dy: int):
        self.hovering = in_bbox((x, y), self.bbox)

    def on_draw(self, window: "Window", scene: "Scene"):
        if self._sprite is not None: self._sprite.draw()
        self._label.draw()

    def on_resize(self, window: "Window", scene: "Scene", width: int, height: int):
        super().on_resize(window, scene, width, height)
        self._update_size()
