"""Immutable dates shared by all calendar engines."""
from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class LunarDay:
    solar: date
    year: int
    month: int
    day: int
    leap: bool = False
    solar_term: str = ''
