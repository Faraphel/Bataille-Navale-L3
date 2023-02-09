from typing import TYPE_CHECKING

import pyglet

from source.gui.scene.abc import AbstractScene
from source.gui.widget import WidgetLabel

if TYPE_CHECKING:
    from source.gui.window import Window


class TestLabelScene(AbstractScene):
    """
    A scene used to test the Label widget
    """

    def __init__(self):
        super().__init__()

        self.label_batch = None

    def on_window_added(self, window: "Window") -> None:
        self.label_batch = pyglet.graphics.Batch()

        for x in range(10):
            for y in range(10):
                self.add_widget(WidgetLabel(
                    x=x*0.1, y=y*0.1, width=0.1, height=0.1,

                    text=f"{x}.{y}",

                    label_batch=self.label_batch,
                ))

        super().on_window_added(window)

    def on_draw(self, window: "Window"):
        super().on_draw(window)

        self.label_batch.draw()
