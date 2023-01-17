from typing import Optional

import pyglet.text


class Label(pyglet.text.Label):
    def update_size(self, x: int, y: int, width: Optional[int] = None, height: Optional[int] = None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
