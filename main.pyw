import pyglet

from source.gui.scene import MainMenu
from source.gui.window import GameWindow


from source.path import path_font
from source.gui.better_pyglet import Label


pyglet.font.add_directory(path_font)
Label.default_kwargs["font_name"] = "Century Gothic"  # NOQA: Label à un "default_kwargs" avec la metaclass


# Create a new window
window = GameWindow(resizable=True, vsync=True, caption="Bataille Navale")
window.set_minimum_size(720, 480)
window.add_scene(MainMenu)

# Start the event loop
pyglet.app.run()

