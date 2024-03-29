import re
from typing import TYPE_CHECKING, Optional, Type

import pyglet.image

from source.gui.better_pyglet import Sprite, Label
from source.gui.texture.abc import Style
from source.gui.widget.abc import BoxWidget
from source.type import Distance
from source.utils import dict_filter_prefix

if TYPE_CHECKING:
    from source.gui.scene.abc import Scene


class Input(BoxWidget):
    """
    Un widget d'entrée avec une texture de fond et un label. Des paternes regex peut être ajouté pour valider l'entrée.
    """

    def __init__(self, scene: "Scene",

                 style: Type[Style],

                 type_regex: Optional[str | re.Pattern] = None,
                 check_regex: Optional[str | re.Pattern] = None,

                 x: Distance = 0,
                 y: Distance = 0,
                 width: Distance = None,
                 height: Distance = None,

                 **kwargs):
        super().__init__(scene, x, y, width, height)

        self.style = style

        self._valid = True

        self.type_regex = re.compile(type_regex) if type_regex is not None else None
        self.check_regex = re.compile(check_regex) if check_regex is not None else None

        self.background = Sprite(
            img=self.style.get("normal"),
            batch=self.scene.batch,
            **dict_filter_prefix("background_", kwargs)
        )

        self.label = Label(
            width=None, height=None,
            anchor_x="center", anchor_y="center",
            batch=self.scene.batch,
            **dict_filter_prefix("label_", kwargs)
        )

        self.add_listener("on_activate_change", lambda *_: self._refresh_background())

        self.check()  # actualise si le regex est valide ou non

        self._refresh_size()

    # background

    @property
    def background_texture(self) -> pyglet.image.AbstractImage:
        """
        Renvoie la texture de fond correspondante.
        Si le widget est activé, renvoie la texture active (si elle existe),
        la texture de clic (si elle existe) sinon la texture normale
        :return: la texture de fond correspondante
        """

        return (
            texture if self.activated and (texture := self.style.get("active")) is not None else  # NOQA
            texture if not self.valid and (texture := self.style.get("error")) is not None else
            self.style.get("normal")
        )

    # rafraichissement

    def _refresh_background(self) -> None:
        self.background.image = self.background_texture

    def _refresh_size(self) -> None:
        self.background.x, self.background.y = self.xy
        self.background.width, self.background.height = self.size

        # center the label
        self.label.x, self.label.y = self.center

    def check(self):
        if self.check_regex is not None:  # si il y a un regex de validation, applique le pour vérifier le texte
            self.valid = self.check_regex.fullmatch(self.text) is not None

    # property

    @property
    def valid(self): return self._valid

    @valid.setter
    def valid(self, valid: bool):
        self._valid = valid
        self._refresh_background()

    @property
    def text(self): return self.label.text

    @text.setter
    def text(self, text: str): self.label.text = text

    # événements

    def on_key_press(self, symbol: int, modifiers: int):
        if not self.activated: return  # ignore si ce widget est désactivé / non sélectionné

        if symbol == pyglet.window.key.BACKSPACE:  # si la touche "supprimé" est enfoncé
            self.text = self.text[0:-1]  # retire le dernier caractère du texte
            self.check()

        if symbol == pyglet.window.key.ENTER:
            self.trigger_event("on_enter")

    def on_text(self, char: str):
        if not self.activated: return  # ignore si ce widget est désactivé / non sélectionné
        if not self.label.multiline and char in "\r\n": return  # si le texte est sur une ligne, ignore les retours

        new_text: str = self.text + char

        if self.type_regex is not None:
            # s'il y a un regex d'écriture, vérifie qu'il est respecté, sinon ignore le nouveau caractère
            if self.type_regex.fullmatch(new_text) is None: return

        self.text = new_text  # ajoute le caractère au label

        self.check()  # rafraichi le fait que le texte est considéré comme valide ou non

        if self.valid:
            self.trigger_event("on_valid_text")

    def on_resize(self, width: int, height: int):
        self._refresh_size()
