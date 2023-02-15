import re
from typing import TYPE_CHECKING, Optional

import pyglet.image

from source.gui.sprite import Sprite
from source.gui.widget.abc import BoxWidget
from source.type import Distance
from source.utils import dict_prefix

if TYPE_CHECKING:
    from source.gui.scene.abc import Scene


class Input(BoxWidget):
    def __init__(self, scene: "Scene",

                 texture_normal: pyglet.image.AbstractImage,
                 texture_active: pyglet.image.AbstractImage = None,
                 texture_error: pyglet.image.AbstractImage = None,

                 regex: Optional[str | re.Pattern] = None,

                 x: Distance = 0,
                 y: Distance = 0,
                 width: Distance = None,
                 height: Distance = None,
                 *args, **kwargs):
        super().__init__(scene, x, y, width, height)

        self._texture_normal: pyglet.image.AbstractImage = texture_normal
        self._texture_active: Optional[pyglet.image.AbstractImage] = texture_active
        self._texture_error: Optional[pyglet.image.AbstractImage] = texture_error

        self._invalid = False

        self.regex = re.compile(regex) if isinstance(regex, str) else regex

        self.background = Sprite(
            img=self._texture_normal,
            **dict_prefix("background_", kwargs)
        )
        self.label = pyglet.text.Label(
            width=None, height=None,
            anchor_x="center", anchor_y="center",
            **dict_prefix("label_", kwargs)
        )

        self._refresh_size()

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
            self._texture_active if self.activated and self._texture_active is not None else
            self._texture_error if self.invalid and self._texture_error is not None else
            self._texture_normal
        )

    # refresh

    def _refresh_background(self) -> None:
        self.background.image = self.background_texture

    def _refresh_size(self) -> None:
        self.background.x, self.background.y = self.x, self.y
        self.background.width, self.background.height = self.width, self.height

        # center the label
        self.label.x = self.x + (self.width / 2)
        self.label.y = self.y + (self.height / 2)

    @BoxWidget.activated.setter
    def activated(self, activated: bool) -> None:
        BoxWidget.activated.fset(self, activated)
        self._refresh_background()

    # property

    @property
    def invalid(self):
        return self._invalid

    @invalid.setter
    def invalid(self, invalid: bool):
        self._invalid = invalid
        self._refresh_background()

    @property
    def text(self):
        return self.label.text

    @text.setter
    def text(self, text: str):
        self.label.text = text

    # event

    def on_key_press(self, symbol: int, modifiers: int):
        if not self.activated: return  # ignore si ce widget est désactivé / non sélectionné

        if symbol == pyglet.window.key.BACKSPACE:  # si la touche "supprimé" est enfoncé
            self.text = self.text[0:-1]  # retire le dernier caractère du texte

    def on_text(self, char: str):
        if not self.activated: return  # ignore si ce widget est désactivé / non sélectionné
        self.text += char  # ajoute le caractère au label

        if self.regex is not None:  # si il y a un regex de validation, applique le pour vérifier le texte
            self.invalid = self.regex.fullmatch(self.text) is None

    def on_resize(self, width: int, height: int):
        self._refresh_size()

    def draw(self):
        self.background.draw()
        self.label.draw()
