from typing import TYPE_CHECKING, Callable, Optional

import pyglet.image

from source.gui.widget.base import Sprite, Label
from source.gui.widget.abc import AbstractResizableWidget
from source.type import Percentage
from source.utils import in_bbox

if TYPE_CHECKING:
    from source.gui.window import Window
    from source.gui.scene.abc import AbstractScene


class Button(AbstractResizableWidget):
    def __init__(self,

                 # position
                 x: int | Percentage,
                 y: int | Percentage,
                 width: int | Percentage,
                 height: int | Percentage,

                 # background
                 normal_texture: pyglet.image.AbstractImage,
                 hover_texture: pyglet.image.AbstractImage = None,
                 click_texture: pyglet.image.AbstractImage = None,

                 # label
                 label_text: str = "",
                 label_font_name: str = None,
                 label_font_size: int = None,
                 label_bold: bool = False,
                 label_italic: bool = False,
                 label_stretch: bool = False,
                 label_color: tuple[int, int, int, int] = (255, 255, 255, 255),
                 label_align: str = "center",
                 label_multiline: bool = False,
                 label_dpi: int = None,
                 label_rotation: int = 0,

                 # callback function
                 on_press: Callable = None,
                 on_release: Callable = None,

                 # batch
                 label_batch: pyglet.graphics.Batch = None,
                 background_batch: pyglet.graphics.Batch = None,

                 # group
                 label_group: pyglet.graphics.Group = None,
                 background_group: pyglet.graphics.Group = None,
                 ):

        super().__init__(x, y, width, height)

        self._normal_texture = normal_texture
        self._hover_texture = hover_texture
        self._click_texture = click_texture

        self.on_press = on_press
        self.on_release = on_release

        self._label: Optional[Label] = None
        self._label_kwargs = {
            "text": label_text,
            "font_name": label_font_name,
            "font_size": label_font_size,
            "bold": label_bold,
            "italic": label_italic,
            "stretch": label_stretch,
            "color": label_color,
            "align": label_align,
            "multiline": label_multiline,
            "dpi": label_dpi,
            "rotation": label_rotation,

            "batch": label_batch,
            "group": label_group,
        }

        self._background: Optional[Sprite] = None
        self._background_kwargs = {
            "batch": background_batch,
            "group": background_group,
        }

        self._hover = False
        self._click = False

    def on_window_added(self, window: "Window", scene: "AbstractScene"):
        super().on_window_added(window, scene)

        self._label = Label(
            x=self.x + self.width / 2, y=self.y + self.height / 2, width=self.width,
            anchor_x="center", anchor_y="center",

            **self._label_kwargs
        )

        self._background = Sprite(
            self._normal_texture,
            x=self.x, y=self.y, width=self.width, height=self.height,

            **self._background_kwargs
        )

    # button update

    @property
    def hover(self) -> bool:
        return self._hover

    @hover.setter
    def hover(self, hover: bool) -> None:
        self._hover = hover
        self.update_sprite()

    @property
    def click(self) -> bool:
        return self._click

    @click.setter
    def click(self, click: bool) -> None:
        self._click = click
        self.update_sprite()

    @property
    def background_texture(self) -> pyglet.image.AbstractImage:
        return (
            self._click_texture if self._click else
            self._hover_texture if self._hover else
            self._normal_texture
        )

    def update_sprite(self):
        self._background.image = self.background_texture

    def update_size(self):
        self._background.update_size(self.x, self.y, self.width, self.height)
        self._label.update_size(self.x + self.width // 2, self.y + self.height // 2, self.width)

    # event

    def on_mouse_motion(self, window: "Window", scene: "AbstractScene", x: int, y: int, dx: int, dy: int):
        self.hover = in_bbox((x, y), self.bbox)

    def on_mouse_press(self, window: "Window", scene: "AbstractScene", x: int, y: int, button: int, modifiers: int):
        if not in_bbox((x, y), self.bbox): return

        self.click = True

        if self.on_press is not None:
            self.on_press(self, window, scene, x, y, button, modifiers)

    def on_mouse_release(self, window: "Window", scene: "AbstractScene", x: int, y: int, button: int, modifiers: int):
        old_click = self.click
        self.click = False

        if not in_bbox((x, y), self.bbox): return

        # if this button was the one hovered when the click was pressed
        if old_click and self.on_release is not None:
            self.on_release(self, window, scene, x, y, button, modifiers)


# TODO: on_resize seem really slow
# TODO: make the percentage dynamic or non dynamic
