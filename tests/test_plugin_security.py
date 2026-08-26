from pathlib import Path
import pytest

from orthoswift.install import target_script_dirs
from orthoswift.runner import validate_config


def test_target_script_dirs_resolution():
    dirs = target_script_dirs()
    assert len(dirs) >= 1
    for d in dirs:
        assert isinstance(d, Path)
        assert "Agisoft" in str(d)
        assert "scripts" in str(d)


def test_config_rejects_unbounded_paths(tmp_path):
    with pytest.raises(FileNotFoundError):
        validate_config({
            "out_dir": str(tmp_path / "out"),
            "orthomosaic_path": str(tmp_path / "non_existent_file.tif"),
            "zones": 3,
        })


def test_config_enforces_zone_limits(tmp_path):
    tif = tmp_path / "test.tif"
    tif.write_bytes(b"dummy")
    with pytest.raises(ValueError, match="zones"):
        validate_config({
            "out_dir": str(tmp_path / "out"),
            "orthomosaic_path": str(tif),
            "zones": 1,
        })
    with pytest.raises(ValueError, match="zones"):
        validate_config({
            "out_dir": str(tmp_path / "out"),
            "orthomosaic_path": str(tif),
            "zones": 12,
        })
