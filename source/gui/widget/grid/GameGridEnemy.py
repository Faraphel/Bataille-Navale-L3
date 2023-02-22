from typing import Type, TYPE_CHECKING

import pyglet

from source.gui.texture.abc import Style
from source.gui.widget.grid.abc import GameGrid
from source.gui.sprite import Sprite
from source.type import Point2D
from source.utils import dict_filter_prefix

if TYPE_CHECKING:
    from source.gui.scene.abc import Scene


class GameGridEnemy(GameGrid):
    """
    A game grid that represent the enemy grid.
    """

    def __init__(self, scene: "Scene",

                 rows: int,
                 columns: int,

                 grid_style: Type[Style],
                 bomb_style: Type[Style],

                 **kwargs):
        self.cell_sprites: dict[Point2D, "Sprite"] = {}

        super().__init__(scene, rows, columns, grid_style, **kwargs)

        self._bomb_kwargs = dict_filter_prefix("bomb_", kwargs)
        self.bomb_style = bomb_style

        self.add_listener("on_click_release", self.on_click_release)

    def _refresh_size(self):
        super()._refresh_size()

        for (x, y), sprite in self.cell_sprites.items():
            sprite.x = self.x + (self.cell_width * x)
            sprite.y = self.y + (self.cell_height * y)
            sprite.width = self.cell_width
            sprite.height = self.cell_height

    def place_bomb(self, cell: Point2D, touched: bool):
        self.cell_sprites[cell] = Sprite(
            img=self.bomb_style.get("touched" if touched else "missed"),
            **self._bomb_kwargs
        )

        self._refresh_size()

    def on_click_release(self, rel_x: int, rel_y: int, button: int, modifiers: int):
        cell = self.get_cell_from_rel(rel_x, rel_y)

        if button == pyglet.window.mouse.LEFT:
            self.trigger_event("on_request_place_bomb", cell)

    def draw(self):
        self.background.draw()
        for sprite in self.cell_sprites.values(): sprite.draw()
        self.cursor.draw()
        for line in self.lines: line.draw()