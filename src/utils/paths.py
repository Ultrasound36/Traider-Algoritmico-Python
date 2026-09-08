from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
CSV_DIR = DATA_DIR / "csv"
EXPORTS_DIR = DATA_DIR / "exports"
GRAFICOS_DIR = DATA_DIR / "graficos"
