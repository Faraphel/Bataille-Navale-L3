from functools import lru_cache
from typing import Type, Callable, TYPE_CHECKING, Any

import pyglet


if TYPE_CHECKING:
    from source.gui.scene.abc import Scene


class Window(pyglet.window.Window):  # NOQA
    """
    A window. Based on the pyglet window object.
    Scene can be added to the window
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._scenes: set["Scene"] = set()

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

    def add_scene(self, scene_class: Type["Scene"], *scene_args, **scene_kwargs) -> "Scene":
        """
        Add a scene of the window.
        :scene_class: the class of the scene to add.
        :scene_args: args for the creation of the scene object.
        :scene_kwargs: kwargs for the creation of the scene object.
        :return: the new created scene.
        """

        scene: "Scene" = scene_class(window=self, *scene_args, **scene_kwargs)
        self._scenes.add(scene)
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

    # Event Handling

    @lru_cache
    def _event_wrapper(self, item: str) -> Callable:
        """
        Un wrapper permettant d'appeler l'événement de toutes les scènes attachées.
        :param name: nom de la fonction à appeler dans la scène.
        :return: une fonction appelant l'événement original ainsi que ceux des scènes.
        """

        func = None
        try: func = super().__getattribute__(item)
        except AttributeError: pass

        def _func(*args, **kwargs) -> None:
            if func is not None: func(*args, **kwargs)
            for scene in self._scenes:
                getattr(scene, item)(*args, **kwargs)

        return _func

    def __getattribute__(self, item: str) -> Any:
        """
        Fonction appelée dès que l'on essaye d'accéder à l'un des attributs de l'objet.
        :param item: nom de l'attribut recherché
        :return: l'attribut de l'objet correspondant.
        """

        # si l'attribut est un événement (commence par "on_"), alors renvoie le dans un wrapper
        return self._event_wrapper(item) if item.startswith("on_") else super().__getattribute__(item)
