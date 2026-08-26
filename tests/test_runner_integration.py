import json
import zipfile
from pathlib import Path

import numpy as np
import pytest
import rasterio
from affine import Affine

from orthoswift.runner import run, validate_config


def write_multispectral(path, size=180):
    y, x = np.indices((size, size))
    red = (0.10 + 0.08 * x / size + 0.01 * np.sin(y / 12)).astype("float32")
    green = (0.14 + 0.03 * y / size).astype("float32")
    blue = (0.08 + 0.02 * x / size).astype("float32")
    nir = (
        np.where(x < size / 3, 0.68, np.where(x < 2 * size / 3, 0.53, 0.40))
        + 0.01 * np.cos(y / 15)
    ).astype("float32")
    red_edge = (0.35 + 0.08 * x / size).astype("float32")
    with rasterio.open(
        path,
        "w",
        driver="GTiff",
        height=size,
        width=size,
        count=5,
        dtype="float32",
        crs="EPSG:32633",
        transform=Affine(1, 0, 500000, 0, -1, 1000),
        nodata=-9999,
    ) as dst:
        dst.write(np.stack([red, green, blue, nir, red_edge]))
        dst.descriptions = ("Red", "Green", "Blue", "NIR", "RedEdge")
    return path


def test_config_rejects_bad_values(tmp_path):
    raster = write_multispectral(tmp_path / "m.tif", 30)
    with pytest.raises(ValueError, match="zones"):
        validate_config(
            {"out_dir": str(tmp_path / "o"), "orthomosaic_path": str(raster), "zones": 9}
        )
    with pytest.raises(ValueError, match="boolean"):
        validate_config(
            {
                "out_dir": str(tmp_path / "o"),
                "orthomosaic_path": str(raster),
                "offline_basemap": "perhaps",
            }
        )


def test_full_runner_outputs_all_visible_deliverables(tmp_path):
    raster = write_multispectral(tmp_path / "m.tif")
    progress = []
    result = run(
        {
            "out_dir": str(tmp_path / "out"),
            "orthomosaic_path": str(raster),
            "zones": 3,
            "offline_basemap": False,
        },
        progress_callback=lambda text, pct: progress.append((text, pct)),
    )
    out = result["core_outputs"]
    for key in [
        "fertilizer_zones_kml",
        "universal_zip",
        "john_deere_rx_zip",
        "case_ih_shapefile_zip",
        "trimble_gfx_zip",
        "ag_leader_root_zip",
        "dji_agras_vra_zip",
        "xag_vra_zip",
        "pdf_report",
        "fertilizer_rate_plan_json",
    ]:
        assert Path(out[key]).exists(), key
    assert Path(result["archive"]).exists()
    assert progress[-1][1] == 100
    with zipfile.ZipFile(result["archive"]) as archive:
        names = archive.namelist()
        assert any(name.endswith("health_report.pdf") for name in names)
        assert any(name.endswith("setup_guide.pdf") for name in names)


def test_physical_rate_plan_reaches_exported_table(tmp_path):
    raster = write_multispectral(tmp_path / "m.tif")
    plan = {
        "mode": "physical",
        "operation": "fertilizer",
        "product_name": "Urea",
        "rate_basis": "product",
        "unit": "KG_HA",
        "strategy": "direct",
        "min_rate": 100,
        "max_rate": 180,
        "approved_by": "Operator",
    }
    result = run(
        {
            "out_dir": str(tmp_path / "out"),
            "orthomosaic_path": str(raster),
            "zones": 3,
            "offline_basemap": False,
            "fertilizer_rate_plan": plan,
        }
    )
    summary = json.loads(Path(result["core_outputs"]["fertilizer_rate_plan_json"]).read_text())
    assert summary["mode"] == "physical"
    assert summary["resolved_min_rate"] == 100
    assert summary["resolved_max_rate"] == 180
