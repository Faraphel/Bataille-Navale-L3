from typing import TYPE_CHECKING, Callable, Type

import pyglet.window

if TYPE_CHECKING:
    from source.gui.scene.abc import AbstractScene


class Window(pyglet.window.Window):  # NOQA
    """
    Similaire à la fenêtre de base de pyglet, mais permet d'ajouter des scènes.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # scene
        self._scenes: list["AbstractScene"] = []

        # a dictionary linking a key pressed to the corresponding event function
        self._on_key_held_events: dict[tuple[int, int], Callable] = {}

        # keys event handler
        self.keys_handler = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keys_handler)

    # scene system

    def set_scene(self, scenes_type: Type["AbstractScene"]) -> "AbstractScene":
        """
        Clear all the previous scene and add a scene to the window
        :param scenes_type: the class of the scene to add
        :return: the scene
        """
        self.clear()
        return self.add_scene(scenes_type)

    def add_scene(self, scene_type: Type["AbstractScene"], priority: int = 0) -> "AbstractScene":
        """
        Add a scene to the window
        :param scene_type: the class of the scene to add
        :param priority: the priority of the scene in the display
        :return: the scene
        """
        scene: "AbstractScene" = scene_type(self)
        self._scenes.insert(priority, scene)
        return scene

    def remove_scene(self, *scenes: "AbstractScene") -> None:
        """
        Remove scenes from the window
        :param scenes: the scenes to remove
        """
        for scene in scenes:
            self._scenes.remove(scene)

    def clear_scene(self) -> None:
        """
        Remove all the scenes from the window
        """
        self.remove_scene(*self._scenes)

    # event

    def scene_event_wrapper(self, name: str, func: Callable) -> Callable:
        """
        Un wrapper permettant d'appeler l'événement de toutes les scènes attachées.
        :param name: nom de la fonction à appeler dans la scène.
        :param func: fonction originale à entourer du wrapper
        :return: une fonction appelant l'événement original ainsi que ceux des scènes.
        """

        def _func(*args, **kwargs):
            func(*args, **kwargs)
            for scene in self._scenes: getattr(scene, name, lambda *_, **__: "pass")(*args, **kwargs)

        return _func

    def __getattribute__(self, item: str):
        """
        Fonction appelée dès que l'on essaye d'accéder à l'un des attributs de l'objet.
        :param item: nom de l'attribut recherché
        :return: l'attribut de l'objet correspondant.
        """

        # print(".", end="")

        attribute = super().__getattribute__(item)

        # si l'attribut est un évenement (commence par "on_"), alors renvoie le dans un wrapper
        return self.scene_event_wrapper(item, attribute) if item.startswith("on_") else attribute

