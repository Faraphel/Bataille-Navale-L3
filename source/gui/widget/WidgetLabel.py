from typing import TYPE_CHECKING, Optional

import pyglet.text

from source.gui.widget.base import Sprite, Label
from source.gui.widget.abc import AbstractResizableWidget
from source.type import Percentage

if TYPE_CHECKING:
    from source.gui.window import Window
    from source.gui.scene.abc import AbstractScene


class WidgetLabel(AbstractResizableWidget):
    def __init__(self,

                 # position
                 x: int | Percentage,
                 y: int | Percentage,
                 width: int | Percentage = None,
                 height: int | Percentage = None,

                 # label
                 text: str = "",
                 font_name: str = None,
                 font_size: int = None,
                 bold: bool = False,
                 italic: bool = False,
                 stretch: bool = False,
                 color: tuple[int, int, int, int] = (255, 255, 255, 255),
                 align: str = "center",
                 multiline: bool = False,
                 dpi: int = None,
                 rotation: int = 0,

                 # background
                 texture: pyglet.image.AbstractImage = None,

                 # batch
                 label_batch: pyglet.graphics.Batch = None,
                 background_batch: pyglet.graphics.Batch = None,

                 # group
                 label_group: pyglet.graphics.Group = None,
                 background_group: pyglet.graphics.Group = None
                 ):

        super().__init__(x, y, width, height)

        self._label: Optional[Label] = None
        self._label_kwargs = {
            "text": text,
            "font_name": font_name,
            "font_size": font_size,
            "bold": bold,
            "italic": italic,
            "stretch": stretch,
            "color": color,
            "align": align,
            "multiline": multiline,
            "dpi": dpi,
            "rotation": rotation,

            "batch": label_batch,
            "group": label_group,
        }

        if texture is not None and width is None or height is None:
            raise ValueError("You need to set a width and a height to create a Label with a background !")

        self._background = None
        self._background_kwargs = {
            "img": texture,
            "batch": background_batch,
            "group": background_group,
        } if texture is not None else None

    def on_window_added(self, window: "Window", scene: "AbstractScene"):
        super().on_window_added(window, scene)

        self._label = Label(
            x=self.x, y=self.y, width=self.width, height=self.height,
            **self._label_kwargs
        )

        if self._background_kwargs is not None:
            self._background = Sprite(
                x=self.x, y=self.y, width=self.width, height=self.height,
                **self._background_kwargs
            )

    def update_size(self):
        self._label.update_size(self.x, self.y, self.width, self.height)
        if self._background is not None: self._background.update_size(self.x, self.y, self.width, self.height)
