from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BacktestResult:
    total_return: float
    win_rate: float
    sharpe_ratio: float | None = None


class BacktestEngine:
    """Motor base para evaluar estrategias con datos históricos."""

    def __init__(self, data):
        self.data = data

    def run(self) -> BacktestResult:
        return BacktestResult(total_return=0.0, win_rate=0.0)
