from typing import TYPE_CHECKING

from source.gui import widget, texture
from source.gui.position import vw_full, vh_full, vh_center, vw_center, vw, vh
from source.gui.scene.abc.Popup import Popup
from source.network.packet import PacketQuit

if TYPE_CHECKING:
    from source.gui.window import Window
    from source.gui.scene import Game


class GameQuit(Popup):
    """
    Cette scène affiche une confirmation pour quitter la partie
    """

    def __init__(self, window: "Window", game_scene: "Game", **kwargs):
        super().__init__(window, **kwargs)

        self.game_scene = game_scene

        self.background = self.add_widget(
            widget.Image,

            x=0, y=0, width=vw_full, height=vh_full,

            image=texture.Popup.Style1.background
        )

        self.text = self.add_widget(
            widget.Text,

            x=vw_center, y=vh_center, width=vw_full,

            anchor_x="center",

            text="Voulez-vous vraiment quitter la partie ?\n(Votre partie ne sera pas sauvegardé !)",
            font_size=28,
            multiline=True,
            align="center",
        )

        self.cancel = self.add_widget(
            widget.Button,
            x=20*vw, y=20*vh, width=20*vw, height=10*vh,

            label_text="Annuler",

            style=texture.Button.Style1
        )

        self.cancel.add_listener("on_click_release", lambda *_: self.window.remove_scene(self))

        self.confirm = self.add_widget(
            widget.Button,
            x=60*vw, y=20*vh, width=20*vw, height=10*vh,

            label_text="Confirmer",

            style=texture.Button.Style1
        )

        self.confirm.add_listener("on_click_release", lambda *_: self.quit())

    def quit(self):
        PacketQuit().send_connection(self.game_scene.connection)  # envoie le packet
        self.game_scene.thread.stop()  # coupe le thread & la connexion

        from source.gui.scene import MainMenu
        self.window.set_scene(MainMenu)  # affiche le menu principal
