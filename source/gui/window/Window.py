from typing import Type, TYPE_CHECKING

import pyglet

from source.gui.event import EventPropagationMixin

if TYPE_CHECKING:
    from source.gui.scene.abc import Scene


class Window(pyglet.window.Window, EventPropagationMixin):  # NOQA
    """
    A window. Based on the pyglet window object.
    Scene can be added to the window
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._scenes: list["Scene"] = list()

    # Event Propagation

    @property
    def childs(self):
        return self._scenes

    # Scene Managing

    def set_scene(self, scene_class: Type["Scene"], *scene_args, **scene_kwargs) -> "Scene":
        """
        Set the scene of the window.
        :scene_class: the class of the scene to add.
        :scene_args: args for the creation of the scene object.
        :scene_kwargs: kwargs for the creation of the scene object.
        :return: the new created scene.
        """

        self.clear_scene()
        return self.add_scene(scene_class, *scene_args, **scene_kwargs)

    def add_scene(self, scene_class: Type["Scene"], priority: int = 0, **scene_kwargs) -> "Scene":
        """
        Add a scene of the window.
        :scene_class: the class of the scene to add.
        :scene_kwargs: kwargs for the creation of the scene object.
        :return: the new created scene.
        """

        scene: "Scene" = scene_class(window=self, **scene_kwargs)
        self._scenes.insert(priority, scene)
        return scene

    def remove_scene(self, scene: "Scene") -> None:
        """
        Remove a scene from the window.
        :scene: the scene to remove.
        """

        self._scenes.remove(scene)

    def clear_scene(self) -> None:
        """
        Clear the window from all the scenes.
        """

        self._scenes.clear()

    # Base Event

    def on_draw(self):  # NOQA
        self.clear()
