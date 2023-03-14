from typing import Callable, Any


def dict_filter(filter_func: Callable[[Any, Any], bool], dictionary: dict[Any, Any]) -> dict[Any, Any]:
    """
    Filtre les objets d'un dictionnaire avec la fonction de filtre donnée.
    :param filter_func: La fonction utilisée pour le filtre. Reçois l'argument clé et valeur
    :param dictionary: Le dictionnaire à filtrer
    :return: Le dictionnaire filtrer

    Exemple :
    filter_func = lambda key, value: key.startswith("valeur")
    dictionary = {"valeur1": 1, "valeur2": 2, "clé1": None}
    -> {"valeur1": 1, "valeur2": 2}
    """

    return {
        k: v for k, v in filter(
            lambda d: filter_func(d[0], d[1]),
            dictionary.items()
        )
    }


def dict_filter_prefix(prefix: str, dictionary: dict[str, Any]) -> dict[str, Any]:
    """
    Ne garde que les clés qui commencent avec ce préfixe dans le dictionnaire et retire leur préfixe.
    :param prefix: le préfixe à utiliser
    :param dictionary: le dictionnaire à filtrer
    :return: le dictionnaire avec le préfixe

    Exemple :
    prefix = "button"
    dictionary = {"button1": 1, "button2": 2, "label1": None}
    -> {"1": 1, "2": 2}
    """

    return {
        k.removeprefix(prefix): v for k, v in dict_filter(
            lambda k, v: k.startswith(prefix),
            dictionary
        ).items()
    }


def dict_add_prefix(prefix: str, dictionary: dict[str, Any]) -> dict[str, Any]:
    """
    Ajoute un préfixe à toute les clés d'un dictionnaire
    :param prefix: le préfixe à ajouter
    :param dictionary: le dictionnaire à modifier
    :return: le dictionnaire avec le préfixe à chaque clé
    """

    return {
        prefix + k: v
        for k, v in dictionary.items()
    }
