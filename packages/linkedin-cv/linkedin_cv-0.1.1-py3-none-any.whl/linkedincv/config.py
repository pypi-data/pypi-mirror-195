from typing import Any

import toml

from linkedincv.cv.models.core import CV

Content = dict[str, Any]


def read_config(path: str) -> CV:
    with open(path, encoding="utf-8") as f:
        content: Content = toml.load(f)
        return CV(**content)
