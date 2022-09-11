from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum

from typing_extensions import TypeGuard

from chemistry.elements.element import Element
from chemistry.utils import superscript


class SubShellType(IntEnum):
    S = 1
    P = 3
    D = 5
    F = 7

    def __str__(self) -> str:
        return str(self.name).lower()


@dataclass(frozen=True)
class SubShell:
    type: SubShellType
    principal: int

    @property
    def max_electrons(self) -> int:
        return self.type.value * 2

    def __eq__(self, ot: object) -> bool:
        return (
            isinstance(ot, SubShell)
            and ot.type == self.type
            and ot.principal == self.principal
        )

    def __hash__(self) -> int:
        return hash((self.type, self.principal))

    def __str__(self) -> str:
        return f"{self.principal}{self.type}"


class ElectronConfiguration:
    ENERGY_ORDERINGS = [
        SubShell(SubShellType.S, 1),
        SubShell(SubShellType.S, 2),
        SubShell(SubShellType.P, 2),
        SubShell(SubShellType.S, 3),
        SubShell(SubShellType.P, 3),
        SubShell(SubShellType.S, 4),
        SubShell(SubShellType.D, 3),
        SubShell(SubShellType.P, 4),
        SubShell(SubShellType.S, 5),
        SubShell(SubShellType.D, 4),
        SubShell(SubShellType.P, 5),
        SubShell(SubShellType.S, 6),
        SubShell(SubShellType.F, 4),
        SubShell(SubShellType.D, 5),
        SubShell(SubShellType.P, 6),
        SubShell(SubShellType.S, 7),
        SubShell(SubShellType.F, 5),
        SubShell(SubShellType.D, 6),
    ]

    def __init__(self, config: dict[SubShell, int]) -> None:
        self.config = config

    @property
    def highest_principal(self) -> int:
        return max(s.principal for s in self.config.keys())

    @property
    def valence_electrons(self) -> ElectronConfiguration:
        highest_principal = self.highest_principal
        config = {
            subshell: electrons
            for subshell, electrons in self.config.items()
            if subshell.principal == highest_principal
        }
        return type(self)(config)

    @property
    def total_electrons(self) -> int:
        return sum(self.config.values())

    @classmethod
    def from_element_meta(cls, meta: Element) -> ElectronConfiguration:
        config = {}
        electrons_left = meta.atomic_number
        for subshell in cls.ENERGY_ORDERINGS:
            if not electrons_left:
                break

            electrons = subshell.max_electrons
            if electrons > electrons_left:
                electrons = electrons_left
            electrons_left -= electrons
            config[subshell] = electrons

        return cls(config)

    def _guard_self(self, ot: object) -> TypeGuard[ElectronConfiguration]:
        return isinstance(ot, ElectronConfiguration)

    def __sub__(self, ot: object) -> ElectronConfiguration:
        if not self._guard_self(ot):
            raise TypeError(f"Unsupported type {type(ot)}.")

        new_config = self.config.copy()
        for subshell, electrons in ot.config.items():
            self_has = new_config.get(subshell, 0)
            if electrons > self_has:
                raise ValueError(
                    "Cannot subtract ElectronConfiguration containing "
                    f"{subshell}{superscript(str(electrons))}, as this "
                    "instance only has "
                    f"{subshell}{superscript(str(self_has))}"
                )

            if leftover := self_has - electrons:
                new_config[subshell] = leftover
            else:
                del new_config[subshell]

        return type(self)(new_config)

    def __repr__(self) -> str:
        return repr(self.config)

    def _pretty(self) -> str:
        return "".join(
            str(subshell) + superscript(str(electrons))
            for subshell, electrons in sorted(
                self.config.items(),
                key=lambda v: self.ENERGY_ORDERINGS.index(v[0]),
            )
        )

    def __str__(self) -> str:
        return self._pretty()
