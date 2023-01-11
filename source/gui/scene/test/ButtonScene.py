import pyglet

from source.gui.scene.base import Scene
from source.gui.widget import Button


class ButtonScene(Scene):
    """
    This is a simple scene to test Button and their adaptable size
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        button_normal_image = pyglet.image.load("./assets/test_button_normal.png")
        button_hover_image = pyglet.image.load("./assets/test_button_hover.png")
        button_click_image = pyglet.image.load("./assets/test_button_clicking.png")

        for x in range(10):
            for y in range(10):
                self.add_widget(Button(
                    x * 0.1, y * 0.1, 0.1, 0.1,

                    text=f"{x}-{y}",
                    font_size=10,
                    on_release=lambda self, *a, **b: print(self, "clicked !"),
                    normal_image=button_normal_image,
                    hover_image=button_hover_image,
                    click_image=button_click_image
                ))
