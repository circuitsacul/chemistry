from __future__ import annotations

from dataclasses import dataclass

from chemistry.elements.electron_config import ElectronConfiguration


@dataclass(frozen=True)
class Element:
    atomic_number: int
    weight: float
    symbol: str
    name: str

    @property
    def electron_config(self) -> ElectronConfiguration:
        return ElectronConfiguration.from_element_meta(self)
