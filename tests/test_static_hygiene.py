import ast
import json
from pathlib import Path

ROOT = Path(__file__).parents[1]


def test_all_python_and_json_parse():
    for path in ROOT.rglob("*.py"):
        if ".git" not in path.parts and ".venv" not in path.parts:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for path in ROOT.rglob("*.json"):
        if ".git" not in path.parts and ".venv" not in path.parts:
            json.loads(path.read_text(encoding="utf-8"))


def test_removed_backend_features_are_absent():
    files = ["orthoswift/core/pipeline.py", "orthoswift/core/decisions.py"]
    text = "\n".join((ROOT / name).read_text(encoding="utf-8").lower() for name in files)
    for token in [
        "plantcountconfig",
        "run_multispectral_plant_count_pipeline",
        "build_replant_prescription_gdf",
        "interrowvegetationconfig",
        "export_spot_spray_kmz",
        "trafficability_gdf",
        "catch_berm_compliance_gdf",
    ]:
        assert token.lower() not in text


def test_visible_interface_files_are_present():
    assert (ROOT / "orthoswift/metashape.py").exists()
    assert (ROOT / "orthoswift/install.py").exists()
    assert (ROOT / "orthoswift/runner.py").exists()
    assert (ROOT / "orthoswift/version.py").exists()
    assert (ROOT / "orthoswift/requirements.txt").exists()
    assert (ROOT / "orthoswift/assets/fonts/SpaceGrotesk-Bold.ttf").exists()
    assert (ROOT / "orthoswift/assets/fonts/InterVariable.ttf").exists()
    assert (ROOT / "install-windows.bat").exists()
    assert (ROOT / "install-macos.command").exists()
    assert (ROOT / "install-macos-linux.sh").exists()
    assert (ROOT / "requirements.txt").exists()
    assert (ROOT / "README.md").exists()
    assert (ROOT / "LICENSE").exists()
    assert (ROOT / "SECURITY.md").exists()
    assert (ROOT / "CONTRIBUTING.md").exists()
