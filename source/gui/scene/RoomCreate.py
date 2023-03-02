from typing import TYPE_CHECKING

from source.gui import widget, texture
from source.gui.scene import RoomHost
from source.gui.scene.abc import Scene
from source.network.packet import PacketSettings

if TYPE_CHECKING:
    from source.gui.window import Window


class RoomCreate(Scene):
    def __init__(self, window: "Window", **kwargs):
        super().__init__(window, **kwargs)

        self.back = self.add_widget(
            widget.Button,
            x=20, y=20, width=0.2, height=0.1,

            label_text="Retour",

            style=texture.Button.Style1
        )

        from source.gui.scene import MainMenu
        self.back.add_listener("on_click_release", lambda *_: self.window.set_scene(MainMenu))

        # Port

        self.add_widget(
            widget.Text,

            x=0.1, y=0.65,

            anchor_x="center", anchor_y="center",

            text="Port"
        )

        self.input_port = self.add_widget(
            widget.Input,

            x=0.2, y=0.60, width=0.15, height=0.1,

            style=texture.Input.Style1,

            regex=r"\d{1,5}",

            label_text="52321"
        )

        # Username

        self.add_widget(
            widget.Text,

            x=0.1, y=0.5,

            anchor_x="center", anchor_y="center",

            text="Pseudonyme"
        )

        self.input_username = self.add_widget(
            widget.Input,

            x=0.2, y=0.45, width=0.15, height=0.1,

            style=texture.Input.Style1,

            label_text="Host"
        )

        # Grid configuration

        self.add_widget(
            widget.Text,

            x=0.1, y=0.9,
            anchor_x="center", anchor_y="center",
            text=f"Largeur de la grille"
        )

        self.input_width = self.add_widget(
            widget.Input,

            x=0.2, y=0.86, width=0.1, height=0.08,

            regex=r"\d+",

            style=texture.Input.Style1,

            label_text="8"
        )

        self.add_widget(
            widget.Text,

            x=0.1, y=0.8,
            anchor_x="center", anchor_y="center",
            text=f"Longueur de la grille"
        )

        self.input_height = self.add_widget(
            widget.Input,

            x=0.2, y=0.76, width=0.1, height=0.08,

            regex=r"\d+",

            style=texture.Input.Style1,

            label_text="8"
        )

        # Tour

        self.checkbox_host_start = self.add_widget(
            widget.Checkbox,

            x=0.4, y=0.8, width=0.05, height=0.1,

            style=texture.Checkbox.Style1,

            state=True
        )

        self.add_widget(
            widget.Text,

            x=0.46, y=0.85,

            anchor_y="center",

            text="Premier tour pour l'hôte"
        )

        # taille et quantité des bateaux

        self.boat_size: int = 1
        self.boat_size_amount: dict[int, int] = {2: 1, 3: 1, 4: 2, 5: 1}

        def update_boat_size_text():
            self.label_boat_size.text = f"Taille: {self.boat_size}"
            self.input_boat_amount.text = str(self.boat_size_amount.get(self.boat_size, 0))

            self.label_boat_recap.text = ""
            for size, amount in sorted(self.boat_size_amount.items(), key=lambda v: v[0]):
                self.label_boat_recap.text += f"Taille: {size}, Quantité: {amount}\n"

        self.button_boat_size_previous = self.add_widget(
            widget.Button,

            x=0.7, y=0.8, width=0.03, height=0.1,

            label_text="<",
            label_font_size=25,

            style=texture.Button.Style1
        )

        def previous_boat_size():
            if self.boat_size <= 1: return
            self.boat_size -= 1
            update_boat_size_text()

        self.button_boat_size_previous.add_listener("on_click_release", lambda *_: previous_boat_size())

        self.label_boat_size = self.add_widget(
            widget.Text,

            x=0.8, y=0.85,

            anchor_x="center", anchor_y="center"
        )

        self.button_boat_size_next = self.add_widget(
            widget.Button,

            x=0.87, y=0.8, width=0.03, height=0.1,

            label_text=">",
            label_font_size=25,

            style=texture.Button.Style1
        )

        def next_boat_size():
            self.boat_size += 1
            update_boat_size_text()

        self.button_boat_size_next.add_listener("on_click_release", lambda *_: next_boat_size())

        self.input_boat_amount = self.add_widget(
            widget.Input,

            x=0.7, y=0.68, width=0.2, height=0.08,

            regex=r"\d+",

            style=texture.Input.Style1,

            label_text="8"
        )

        def change_boat_amount():
            quantity = int(self.input_boat_amount.text)

            if quantity > 0:
                self.boat_size_amount[self.boat_size] = quantity

            elif self.boat_size in self.boat_size_amount:
                self.boat_size_amount.pop(self.boat_size)

            update_boat_size_text()

        self.input_boat_amount.add_listener("on_valid_text", lambda *_: change_boat_amount())
        self.input_boat_amount.add_listener("on_enter", lambda *_: change_boat_amount())

        self.label_boat_recap = self.add_widget(
            widget.Text,

            x=0.7, y=0.60, width=0.2, height=0.1,

            multiline=True
        )

        update_boat_size_text()

        # TODO: si on diminue la taille de la grille après avoir mis des bateaux de plus longue taille, faire un check

        # Démarrer

        self.start = self.add_widget(
            widget.Button,
            x=lambda widget: widget.scene.window.width - 20 - widget.width, y=20, width=0.2, height=0.1,

            label_text="Continuer",

            style=texture.Button.Style1
        )

        self.start.add_listener("on_click_release", lambda *_: self.confirm())

    def confirm(self):
        port = int(self.input_port.text)

        settings = PacketSettings(
            grid_width=int(self.input_width.text),
            grid_height=int(self.input_height.text),
            host_start=self.checkbox_host_start.state,
            boats_length=[size for size, quantity in self.boat_size_amount.items() for _ in range(quantity)]
        )

        self.window.set_scene(
            RoomHost,
            port=port,
            username=self.input_username.text,
            settings=settings
        )
