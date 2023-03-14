from datetime import datetime
from pathlib import Path


def path_ctime_str(path: Path) -> str:
    """
    Un raccourci permettant d'obtenir la représentation de la date de création d'un fichier
    :param path: le chemin du fichier
    :return: la date correspondante sous la forme d'un texte
    """
    return datetime.fromtimestamp(path.lstat().st_ctime).strftime('%d/%m/%Y %H:%M:%S')
