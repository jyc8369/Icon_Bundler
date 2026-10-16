from __future__ import annotations

import json
from functools import lru_cache
from importlib.resources import files

DEFAULT_LANGUAGE = "en"
_LOCALES_DIR = files("icon_bundler").joinpath("locales")
SUPPORTED_LANGUAGES = tuple(
    sorted(path.name[:-5] for path in _LOCALES_DIR.iterdir() if path.name.endswith(".json"))
)


@lru_cache(maxsize=None)
def _load_language(language: str) -> dict[str, str]:
    resource = _LOCALES_DIR.joinpath(f"{language}.json")
    return json.loads(resource.read_text(encoding="utf-8"))


def get_text(language: str, key: str) -> str:
    lang = language if language in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE
    return _load_language(lang)[key]
