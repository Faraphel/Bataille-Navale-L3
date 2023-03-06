from pathlib import Path

path_save: Path = Path("./.save")
path_save.mkdir(exist_ok=True)

path_history: Path = Path("./.history")
path_history.mkdir(exist_ok=True)

path_assets: Path = Path("./assets")
path_sound: Path = path_assets / "sound"
path_image: Path = path_assets / "image"
path_font: Path = path_assets / "font"
