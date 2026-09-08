from pathlib import Path

from src.utils.paths import CSV_DIR, DATA_DIR, EXPORTS_DIR, PROJECT_ROOT


def test_project_paths_point_to_workspace_data_directory():
    assert PROJECT_ROOT == Path(__file__).resolve().parents[1]
    assert DATA_DIR == PROJECT_ROOT / "data"
    assert CSV_DIR == DATA_DIR / "csv"
    assert EXPORTS_DIR == DATA_DIR / "exports"
