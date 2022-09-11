from __future__ import annotations

from dataclasses import dataclass

from chemistry.elements.electron_config import ElectronConfiguration


@dataclass
class ElementMeta:
    atomic_number: int
    weight: float
    symbol: str
    name: str

    @property
    def electron_config(self) -> ElectronConfiguration:
        return ElectronConfiguration.from_element_meta(self)


class Element:
    def __init__(self, meta: ElementMeta) -> None:
        self.meta = meta
