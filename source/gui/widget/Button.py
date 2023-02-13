from typing import TYPE_CHECKING, Optional

import pyglet

from source.gui.sprite import Sprite
from source.gui.widget.abc import BoxWidget
from source.type import Percentage
from source.utils import dict_prefix

if TYPE_CHECKING:
    from source.gui.scene.abc import Scene


class Button(BoxWidget):
    """
    A button widget with a background texture that change depending on if it is clicked or hovered, and a label.
    You can pass parameter to the background and label by adding "background_" and "label_" before the parameter.
    """

    def __init__(self, scene: "Scene",

                 texture_normal: pyglet.image.AbstractImage,

                 x: Percentage = 0,
                 y: Percentage = 0,
                 width: Percentage = None,
                 height: Percentage = None,

                 texture_hover: pyglet.image.AbstractImage = None,
                 texture_click: pyglet.image.AbstractImage = None,

                 **kwargs):
        super().__init__(scene, x, y, width, height)

        self._texture_normal: pyglet.image.AbstractImage = texture_normal
        self._texture_hover: Optional[pyglet.image.AbstractImage] = texture_hover
        self._texture_click: Optional[pyglet.image.AbstractImage] = texture_click

        self.background = Sprite(
            img=self._texture_normal,
            **dict_prefix("background_", kwargs)
        )

        self.label = pyglet.text.Label(
            anchor_x="center", anchor_y="center",
            **dict_prefix("label_", kwargs)
        )

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
            self._texture_click if self.clicking and self._texture_click is not None else
            self._texture_hover if self.hovering and self._texture_hover is not None else
            self._texture_normal
        )

    # refresh

    def _refresh_background(self) -> None:
        self.background.image = self.background_texture

    def _refresh_size(self) -> None:
        self.background.x = self.x
        self.background.y = self.y
        self.background.width = self.width
        self.background.height = self.height

        self.label.x = self.x + (self.width / 2)
        self.label.y = self.y + (self.height / 2)

    @BoxWidget.hovering.setter
    def hovering(self, hovering: bool):
        # when the hover state is changed, update the background
        BoxWidget.hovering.fset(self, hovering)
        self._refresh_background()

    @BoxWidget.clicking.setter
    def clicking(self, clicking: bool):
        # when the clicking state is changed, update the background
        BoxWidget.clicking.fset(self, clicking)
        self._refresh_background()

    # event

    def on_resize(self, width: int, height: int):
        self._refresh_size()

    def draw(self):
        """
        The draw function. Can be called to draw the widget, but can be ignored to draw it with batchs.
        """

        self.background.draw()
        self.label.draw()

