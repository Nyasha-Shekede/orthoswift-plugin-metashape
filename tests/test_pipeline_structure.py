import ast
from pathlib import Path

PIPELINE = Path(__file__).parents[1] / "orthoswift" / "core" / "pipeline.py"
EXPECTED_STAGES = {
    "_prepare_pipeline_run",
    "_load_spectral_inputs",
    "_apply_footprint_and_validate",
    "_project_to_metric_crs",
    "_compute_and_export_indices",
    "_build_and_export_zones",
    "_find_and_export_hotspots",
    "_export_controller_packages",
    "_build_report_and_audit",
}


def _pipeline_function():
    tree = ast.parse(PIPELINE.read_text(encoding="utf-8"))
    return next(
        node
        for node in tree.body
        if isinstance(node, ast.FunctionDef) and node.name == "run_agriculture_pipeline"
    )


def test_public_pipeline_is_branch_free_orchestration():
    function = _pipeline_function()
    decisions = (
        ast.If,
        ast.For,
        ast.AsyncFor,
        ast.While,
        ast.Try,
        ast.IfExp,
        ast.Match,
    )
    assert not any(isinstance(node, decisions) for node in ast.walk(function))


def test_public_pipeline_calls_each_characterized_stage():
    function = _pipeline_function()
    calls = {
        node.func.id
        for node in ast.walk(function)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    assert EXPECTED_STAGES <= calls
