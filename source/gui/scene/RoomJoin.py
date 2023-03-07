from typing import TYPE_CHECKING, Optional

from source import network
from source.gui.scene.abc import Scene
from source.gui import widget, texture, regex

if TYPE_CHECKING:
    from source.gui.window import Window


class RoomJoin(Scene):
    def __init__(self, window: "Window", **kwargs):
        super().__init__(window, **kwargs)

        self.back = self.add_widget(
            widget.Button,
            x=20, y=20, width=0.2, height=0.1,

            label_text="Retour",

            style=texture.Button.Style1
        )

        self.back.add_listener("on_click_release", self.button_back_callback)

        # Pseudo

        self.entry_username = self.add_widget(
            widget.Input,
            x=0.4, y=0.55, width=0.2, height=0.1,

            type_regex=regex.username_type,
            check_regex=regex.username_check,

            style=texture.Input.Style1,

            label_text="Client"
        )

        # IP / Port

        self.entry_ip = self.add_widget(
            widget.Input,
            x=0.4, y=0.45, width=0.13, height=0.1,

            type_regex=regex.ipv4_type,
            check_regex=regex.ipv4_check,

            style=texture.Input.Style1,

            label_text="127.0.0.1"
        )

        self.entry_port = self.add_widget(
            widget.Input,
            x=0.53, y=0.45, width=0.07, height=0.1,

            type_regex=regex.port_type,
            check_regex=regex.port_check,

            label_text="52321",

            style=texture.Input.Style1
        )

        self.connect = self.add_widget(
            widget.Button,
            x=0.4, y=0.35, width=0.2, height=0.1,

            label_text="Se connecter",

            style=texture.Button.Style1
        )

        self.connect.add_listener("on_click_release", self.button_connect)

        self.status = self.add_widget(
            widget.Text,
            x=0.5, y=0.25,

            anchor_x="center",
        )

        self.thread: Optional[network.Client] = None

    def button_connect(self, widget, *_):
        self.status.text = "Connexion..."
        self.status.label.color = (255, 255, 255, 255)  # blanc
        widget.remove_listener("on_click_release", self.button_connect)

        self.thread = network.Client(
            window=self.window,
            on_connexion_refused=self.connexion_refused,
            ip_address=self.entry_ip.text,
            port=int(self.entry_port.text),
            daemon=True,
            username=self.entry_username.text
        )
        self.thread.start()

    def connexion_refused(self):
        self.status.text = "Échec de la connexion"
        self.status.label.color = (255, 32, 32, 255)  # rouge
        self.connect.add_listener("on_click_release", self.button_connect)

    def button_back_callback(self, widget, *_):
        if self.thread is not None: self.thread.stop()

        from source.gui.scene import MainMenu
        self.window.set_scene(MainMenu)


