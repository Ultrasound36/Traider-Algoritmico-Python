from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FinancialAsset:
    symbol: str
    name: str
    market: str = "US"
