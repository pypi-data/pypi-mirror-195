from pathlib import Path

from dynaconf import LazySettings

SETTINGS_TOML_PATH = Path(__file__).parent.joinpath("settings.toml")

settings = LazySettings(settings_files=[SETTINGS_TOML_PATH], environments=True)
