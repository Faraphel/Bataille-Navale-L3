from datetime import datetime
from pathlib import Path


def path_ctime_str(path: Path):
    return datetime.fromtimestamp(path.lstat().st_ctime).strftime('%d/%m/%Y %H:%M:%S')
