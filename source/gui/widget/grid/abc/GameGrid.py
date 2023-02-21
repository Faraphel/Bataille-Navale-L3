from typing import TYPE_CHECKING, Type

import pyglet.shapes

from source.gui.sprite import Sprite
from source.gui.texture.abc import Style
from source.gui.widget.abc import BoxWidget
from source.type import Distance
from source.utils import dict_filter_prefix

if TYPE_CHECKING:
    from source.gui.scene.abc import Scene


class GameGrid(BoxWidget):
    def __init__(self, scene: "Scene",

                 rows: int,
                 columns: int,

                 style: Type[Style],

                 x: Distance = 0,
                 y: Distance = 0,
                 width: Distance = None,
                 height: Distance = None,

                 **kwargs):
        super().__init__(scene, x, y, width, height)

        self.rows = rows
        self.columns = columns

        self.style = style

        self.background = Sprite(
            img=style.get("background"),
            **dict_filter_prefix("background_", kwargs)
        )

        self.lines: list[pyglet.shapes.Line] = [
            pyglet.shapes.Line(
                0, 0, 0, 0,
                **dict_filter_prefix("line_", kwargs)
            )
            for _ in range((self.columns - 1) + (self.rows - 1))
        ]

        self.cursor = pyglet.shapes.Rectangle(
            0, 0, 0, 0,
            color=(0, 0, 0, 100),
            **dict_filter_prefix("cursor_", kwargs)
        )

        self.add_listener("on_hover_leave", lambda *_: self.hide_cursor())
        self.add_listener("on_hover", self._refresh_cursor)

        self._refresh_size()

    def get_cell_from_rel(self, rel_x: int, rel_y: int) -> tuple[int, int]:
        """
        Return the cell of the grid from a point relative position
        """

        return (
            int((rel_x-1) / self.cell_width),
            int((rel_y-1) / self.cell_height)
        )

    # refresh

    def _refresh_size(self):
        self.background.x, self.background.y = self.xy
        self.background.width, self.background.height = self.size

        for column, line in enumerate(self.lines[:self.columns - 1], start=1):
            line.x = self.x + self.cell_width * column
            line.x2 = line.x
            line.y = self.y
            line.y2 = self.y2

        for row, line in enumerate(self.lines[-self.rows + 1:], start=1):
            line.x = self.x
            line.x2 = self.x2
            line.y = self.y + self.cell_height * row
            line.y2 = line.y

    def _refresh_cursor(self, rel_x: int, rel_y: int):
        cell_x, cell_y = self.get_cell_from_rel(rel_x, rel_y)

        self.cursor.x = self.x + cell_x * self.width / self.columns
        self.cursor.y = self.y + cell_y * self.height / self.rows
        self.cursor.width, self.cursor.height = self.cell_size

    def hide_cursor(self):
        self.cursor.width, self.cursor.height = 0, 0

    # property

    @property
    def cell_width(self) -> float:
        return self.width / self.columns

    @property
    def cell_height(self) -> float:
        return self.height / self.rows

    @property
    def cell_size(self) -> tuple[float, float]:
        return self.cell_width, self.cell_height

    # event

    def on_resize(self, width: int, height: int):
        self._refresh_size()

    def draw(self):
        self.background.draw()
        self.cursor.draw()
        for line in self.lines: line.draw()
