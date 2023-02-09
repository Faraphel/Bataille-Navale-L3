from typing import TYPE_CHECKING

import pyglet

from source.gui.scene.abc import AbstractScene
from source.gui.widget import WidgetButton

if TYPE_CHECKING:
    from source.gui.window import Window


class TestButtonScene(AbstractScene):
    """
    A scene used to test the Button widget
    """

    def __init__(self):
        super().__init__()

        self.button_atlas = None
        self.background_batch = None
        self.label_batch = None

    def on_window_added(self, window: "Window") -> None:
        normal_texture = pyglet.image.load("./assets/image/button/test_button_normal.png")
        hover_texture = pyglet.image.load("./assets/image/button/test_button_hover.png")
        click_texture = pyglet.image.load("./assets/image/button/test_button_clicking.png")

        self.button_atlas = pyglet.image.atlas.TextureAtlas()
        normal_region = self.button_atlas.add(normal_texture)
        hover_region = self.button_atlas.add(hover_texture)
        click_region = self.button_atlas.add(click_texture)

        self.background_batch = pyglet.graphics.Batch()
        self.label_batch = pyglet.graphics.Batch()

        for x in range(10):
            for y in range(10):
                self.add_widget(WidgetButton(
                    x=x*0.1, y=y*0.1, width=0.1, height=0.1,

                    normal_texture=normal_region,
                    hover_texture=hover_region,
                    click_texture=click_region,

                    label_text=f"TEST TEST CENTERING {x}.{y}",
                    label_multiline=True,

                    label_batch=self.label_batch,
                    background_batch=self.background_batch,
                ))

        super().on_window_added(window)

    def on_draw(self, window: "Window"):
        super().on_draw(window)

        self.background_batch.draw()
        self.label_batch.draw()
