from typing import Type

from source.gui.texture.abc import Style
from source.gui.widget.grid.abc import GameGrid


class GameGridEnemy(GameGrid):
    def __init__(self, scene: "Scene", rows: int, columns: int, style: Type[Style], **kwargs):
        super().__init__(scene, rows, columns, style, **kwargs)

