import json
from pathlib import Path
from typing import TYPE_CHECKING

from source.gui import widget, texture
from source.gui.position import h_percent, w_percent
from source.gui.scene.abc import BaseGame

if TYPE_CHECKING:
    from source.gui.window import Window


class HistoryGame(BaseGame):
    def __init__(self, window: "Window", history_path: Path, **kwargs):

        with open(history_path, "r", encoding="utf8") as file:
            history_data = json.load(file)

        super().__init__(
            window,
            boats_length=[],
            name_ally=history_data["name_ally"],
            name_enemy=history_data["name_enemy"],
            board_ally_data=history_data["grid_ally"],
            board_enemy_data=history_data["grid_enemy"],
            history=history_data["history"],
            **kwargs
        )

        self.history_path = history_path

        from source.gui.scene import MainMenu
        self.button_quit.add_listener("on_click_release", lambda *_: window.set_scene(MainMenu))

        self.move_number: int = 0  # numéro du mouvement en cours

        self.grid_ally.board.clear_bombs()
        self.grid_ally.refresh_board()
        self.grid_enemy.board.clear_bombs()
        self.grid_enemy.refresh_board()

        self.previous = self.add_widget(
            widget.Button,
            x=w_percent(20), y=h_percent(10), width=w_percent(20), height=h_percent(10),

            label_text="Précédent",

            style=texture.Button.Style1
        )

        self.previous.add_listener("on_click_release", lambda *_: self.previous_move())

        self.next = self.add_widget(
            widget.Button,
            x=w_percent(60), y=h_percent(10), width=w_percent(20), height=h_percent(10),

            label_text="Suivant",

            style=texture.Button.Style1
        )

        self.next.add_listener("on_click_release", lambda *_: self.next_move())

        self.text_move = self.add_widget(
            widget.Text,
            x=w_percent(50), y=h_percent(12),

            anchor_x="center",

            font_size=28,
        )
        self._refresh_move_text()

    def _refresh_move_text(self):
        self.text_move.text = f"{self.move_number} / {len(self.history)}"
        self._refresh_score_text()

    def previous_move(self):
        # si le mouvement est au minimum, ignore
        if self.move_number <= 0: return

        self.move_number -= 1
        turn, cell = self.history[self.move_number]
        (self.grid_enemy if turn else self.grid_ally).remove_bomb(cell)

        self._refresh_move_text()

    def next_move(self):
        # si le mouvement est au maximum, ignore
        if self.move_number >= len(self.history): return

        self.move_number += 1
        turn, cell = self.history[self.move_number-1]
        (self.grid_enemy if turn else self.grid_ally).place_bomb(cell)

        self._refresh_move_text()
