import json
from pathlib import Path

import numpy as np
import rasterio
from affine import Affine
from PIL import Image

from orthoswift.core.pipeline import run_agriculture_pipeline


def _write_stack(path: Path, *, scale: float = 1.0, size: int = 64) -> Path:
    y, x = np.indices((size, size), dtype="float32")
    red = scale * (0.10 + 0.04 * x / size)
    green = scale * (0.15 + 0.02 * y / size)
    blue = scale * (0.08 + 0.01 * x / size)
    nir = scale * (0.55 + 0.12 * (x < size / 2))
    red_edge = scale * (0.31 + 0.04 * x / size)
    with rasterio.open(
        path,
        "w",
        driver="GTiff",
        height=size,
        width=size,
        count=5,
        dtype="float32",
        crs="EPSG:32633",
        transform=Affine(1, 0, 500_000, 0, -1, 1_000),
    ) as dataset:
        dataset.write(np.stack([red, green, blue, nir, red_edge]))
        dataset.descriptions = ("Red", "Green", "Blue", "NIR", "RedEdge")
    return path


def _run(tmp_path: Path, *, scale: float = 1.0) -> dict:
    raster = _write_stack(tmp_path / "stack.tif", scale=scale)
    preview = tmp_path / "preview.png"
    Image.new("RGB", (8, 8), "green").save(preview)
    return run_agriculture_pipeline(
        ortho_preview=preview,
        out_dir=tmp_path / "output",
        multispectral_path=raster,
        k_range=(2, 2),
        export_kml=False,
        export_relative_application_packages=False,
        bundle_basemap_in_controller_archives=False,
    )


def test_index_and_audit_stage_characterization(tmp_path):
    outputs = _run(tmp_path)
    with rasterio.open(outputs["ndvi_tif"]) as dataset:
        actual = dataset.read(1, masked=True).filled(np.nan)
    with rasterio.open(tmp_path / "stack.tif") as dataset:
        red, nir = dataset.read([1, 4])
    expected = (nir - red) / (nir + red)

    assert np.nanmax(np.abs(actual - expected)) < 1e-6
    audit = json.loads(Path(outputs["input_band_audit_json"]).read_text())
    assert audit["mode"] == "stacked"
    assert audit["resolved_band_map"] == {
        "blue": 3,
        "green": 2,
        "nir": 4,
        "red": 1,
        "red_edge": 5,
    }
    assert audit["absolute_reflectance_gate"]["passed"] is True
    assert outputs["zones_n"] == 2


def test_radiometry_gate_blocks_controller_stage(tmp_path):
    outputs = _run(tmp_path, scale=0.001)
    methodology = json.loads(Path(outputs["pipeline_methodology_json"]).read_text())

    assert methodology["absolute_reflectance_valid"] is False
    assert methodology["prescription_qc_passed"] is False
    assert "controller_packages_dir" not in outputs
    assert any(
        "Absolute-reflectance gate failed" in item for item in outputs["warnings"]
    )
