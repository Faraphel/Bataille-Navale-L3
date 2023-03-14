from typing import TYPE_CHECKING, Type

import pyglet

from source.gui.better_pyglet import Sprite, Label
from source.gui.texture.abc import Style
from source.gui.widget.abc import BoxWidget
from source.type import Distance
from source.utils import dict_filter_prefix

if TYPE_CHECKING:
    from source.gui.scene.abc import Scene


class Button(BoxWidget):
    """
    Un bouton avec une texture de fond qui change en fonction de s'il est cliqué ou survolé et un label.
    Vous pouvez passer des paramètres pour le background et au label en ajoutant "background_" et "label_"
    devant le paramètre.
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
            batch=self.scene.batch,
            **dict_filter_prefix("background_", kwargs)
        )

        self.label = Label(
            width=None, height=None,
            anchor_x="center", anchor_y="center",
            batch=self.scene.batch,
            **dict_filter_prefix("label_", kwargs)
        )

        self.add_listener("on_hover_change", lambda *_: self._refresh_background())
        self.add_listener("on_click_change", lambda *_: self._refresh_background())

        self._refresh_size()  # rafraîchit la taille et la position du background et du label

    # background

    @property
    def background_texture(self) -> pyglet.image.AbstractImage:
        """
        Renvoie la bonne texture pour le fond.
        Utilise la texture normale par défaut, si survolé la texture de survol (si elle existe)
        et la texture de clic (si elle existe) si cliqué
        :return: la texture correspondante
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
