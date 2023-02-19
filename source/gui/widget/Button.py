from typing import TYPE_CHECKING, Optional, Type

import pyglet

from source.gui.sprite import Sprite
from source.gui.texture.abc import Style
from source.gui.widget.abc import BoxWidget
from source.type import Distance
from source.utils import dict_filter_prefix

if TYPE_CHECKING:
    from source.gui.scene.abc import Scene


class Button(BoxWidget):
    """
    A button widget with a background texture that change depending on if it is clicked or hovered, and a label.
    You can pass parameter to the background and label by adding "background_" and "label_" before the parameter.
    """

    def __init__(self, scene: "Scene",

                 style: Type[Style],

                 x: Distance = 0,
                 y: Distance = 0,
                 width: Distance = None,
                 height: Distance = None,

                 **kwargs):
        super().__init__(scene, x, y, width, height)

        self.style = style

        self.background = Sprite(
            img=self.style.get("normal"),
            **dict_filter_prefix("background_", kwargs)
        )

        self.label = pyglet.text.Label(
            width=None, height=None,
            anchor_x="center", anchor_y="center",
            **dict_filter_prefix("label_", kwargs)
        )

        self.add_listener("on_hover_change", lambda *_: self._refresh_background())
        self.add_listener("on_click_change", lambda *_: self._refresh_background())

        self._refresh_size()  # refresh the size and position for the background and label

    # background

    @property
    def background_texture(self) -> pyglet.image.AbstractImage:
        """
        Return the correct texture for the background.
        The clicking texture per default, if hover the hovered texture (if it exists)
        and if click the clicking texture (if it exists)
        :return: the corresponding texture
        """

        return (
            texture if self.clicking and (texture := self.style.get("click")) is not None else  # NOQA
            texture if self.hovering and (texture := self.style.get("hover")) is not None else
            self.style.get("normal")
        )

    # refresh

    def _refresh_background(self) -> None:
        self.background.image = self.background_texture

    def _refresh_size(self) -> None:
        self.background.x, self.background.y = self.xy
        self.background.width, self.background.height = self.size

        # center the label
        self.label.x, self.label.y = self.center

    # event

    def on_resize(self, width: int, height: int):
        self._refresh_size()

    def draw(self):
        self.background.draw()
        self.label.draw()

