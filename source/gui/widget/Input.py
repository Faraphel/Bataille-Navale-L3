import re
from typing import TYPE_CHECKING, Optional, Type

import pyglet.image

from source.gui.sprite import Sprite
from source.gui.texture.abc import Style
from source.gui.widget.abc import BoxWidget
from source.type import Distance
from source.utils import dict_filter_prefix

if TYPE_CHECKING:
    from source.gui.scene.abc import Scene


class Input(BoxWidget):
    """
    An input widget with a background texture and a label. A regex pattern can be added to validate the input.
    """

    def __init__(self, scene: "Scene",

                 style: Type[Style],

                 regex: Optional[str | re.Pattern] = None,

                 x: Distance = 0,
                 y: Distance = 0,
                 width: Distance = None,
                 height: Distance = None,

                 **kwargs):
        super().__init__(scene, x, y, width, height)

        self.style = style

        self._invalid = False

        self.regex = re.compile(regex) if isinstance(regex, str) else regex

        self.background = Sprite(
            img=self.style.get("normal"),
            batch=self.scene.batch,
            **dict_filter_prefix("background_", kwargs)
        )

        self.label = pyglet.text.Label(
            width=None, height=None,
            anchor_x="center", anchor_y="center",
            batch=self.scene.batch,
            **dict_filter_prefix("label_", kwargs)
        )

        self.add_listener("on_activate_change", lambda *_: self._refresh_background())

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
            texture if self.activated and (texture := self.style.get("active")) is not None else  # NOQA
            texture if self.invalid and (texture := self.style.get("signal")) is not None else
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

        if symbol == pyglet.window.key.ENTER:
            self.trigger_event("on_enter")

    def on_text(self, char: str):
        if not self.activated: return  # ignore si ce widget est désactivé / non sélectionné
        if not self.label.multiline and char in "\r\n": return  # si le texte est sur une ligne, ignore les retours

        self.text += char  # ajoute le caractère au label

        if self.regex is not None:  # si il y a un regex de validation, applique le pour vérifier le texte
            self.invalid = self.regex.fullmatch(self.text) is None

        if not self.invalid:
            self.trigger_event("on_valid_text")

    def on_resize(self, width: int, height: int):
        self._refresh_size()
