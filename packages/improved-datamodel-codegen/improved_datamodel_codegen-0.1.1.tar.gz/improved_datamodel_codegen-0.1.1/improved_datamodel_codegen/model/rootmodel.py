from __future__ import annotations

from typing import ClassVar

from improved_datamodel_codegen.model import DataModel


class RootModel(DataModel):
    TEMPLATE_FILE_PATH: ClassVar[str] = 'root.jinja2'
