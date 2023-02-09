from typing import TYPE_CHECKING, Optional

import pyglet

from source.gui.scene.abc import AbstractScene
from source.gui.widget import WidgetLabel, WidgetButton

if TYPE_CHECKING:
    from source.gui.window import Window


class MainMenuScene(AbstractScene):
    def __init__(self):
        super().__init__()
        self._title: Optional[WidgetLabel] = None
        self._room_create: Optional[WidgetButton] = None
        self._room_join: Optional[WidgetButton] = None

    def on_window_added(self, window: "Window"):
        normal_texture = pyglet.image.load("./assets/image/button/test_button_normal.png")
        hover_texture = pyglet.image.load("./assets/image/button/test_button_hover.png")
        click_texture = pyglet.image.load("./assets/image/button/test_button_clicking.png")

        self.button_atlas = pyglet.image.atlas.TextureAtlas()
        normal_region = self.button_atlas.add(normal_texture)
        hover_region = self.button_atlas.add(hover_texture)
        click_region = self.button_atlas.add(click_texture)

        self.background_batch = pyglet.graphics.Batch()
        self.label_batch = pyglet.graphics.Batch()

        self._title = WidgetLabel(
            x=0.1, y=0.9, width=0.2, height=0.1,
            text="Bataille Navale",
            font_size=30,
            label_batch=self.label_batch,
        )
        self.add_widget(self._title)

        self._room_create = WidgetButton(
            x=0.1, y=0.5, width=0.3, height=0.1,
            label_text="Créer une salle",

            normal_texture=normal_region,
            hover_texture=hover_region,
            click_texture=click_region,

            label_batch=self.label_batch,
            background_batch=self.background_batch,
        )
        self.add_widget(self._room_create)

        self._room_join = WidgetButton(
            x=0.1, y=0.4, width=0.3, height=0.1,
            label_text="Rejoindre une salle",

            normal_texture=normal_region,
            hover_texture=hover_region,
            click_texture=click_region,

            label_batch=self.label_batch,
            background_batch=self.background_batch,
        )
        self.add_widget(self._room_join)

        super().on_window_added(window)

    def on_draw(self, window: "Window"):
        super().on_draw(window)

        self.background_batch.draw()
        self.label_batch.draw()
