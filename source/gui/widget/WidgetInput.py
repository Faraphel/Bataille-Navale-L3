from typing import TYPE_CHECKING

import pyglet.text

from source.gui.widget.abc import AbstractResizableWidget
from source.type import Percentage

if TYPE_CHECKING:
    from source.gui.window import Window
    from source.gui.scene.abc import AbstractScene


class WidgetInput(AbstractResizableWidget):
    def __init__(self,

                 # position
                 x: int | Percentage,
                 y: int | Percentage,
                 width: int | Percentage,
                 height: int | Percentage,

                 # background
                 texture: pyglet.image.AbstractImage,

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

                 # batch
                 label_batch: pyglet.graphics.Batch = None,
                 background_batch: pyglet.graphics.Batch = None,

                 # group
                 label_group: pyglet.graphics.Group = None,
                 background_group: pyglet.graphics.Group = None,
                 ):

        super().__init__(x, y, width, height)

        self._label = None
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

        self._background_kwargs = {
            "img": texture,
            "batch": background_batch,
            "group": background_group,
        }

    def on_window_added(self, window: "Window", scene: "AbstractScene"):
        ...
