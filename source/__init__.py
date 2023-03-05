from pathlib import Path

path_save: Path = Path(".save")
path_save.mkdir(exist_ok=True)

path_history: Path = Path(".history")
path_history.mkdir(exist_ok=True)
