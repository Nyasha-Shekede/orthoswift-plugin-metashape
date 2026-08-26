from pathlib import Path


def test_version_consistency():
    root = Path(__file__).parents[1]
    version_vars = {}
    exec((root / "orthoswift" / "version.py").read_text(encoding="utf-8"), version_vars)
    version = version_vars.get("__version__", "1.0.0")

    pyproject_text = (root / "pyproject.toml").read_text(encoding="utf-8")
    assert f'version = "{version}"' in pyproject_text

    readme_text = (root / "README.md").read_text(encoding="utf-8")
    assert version in readme_text


def test_required_assets_and_files_exist():
    root = Path(__file__).parents[1]
    required_files = [
        "orthoswift/__init__.py",
        "orthoswift/install.py",
        "orthoswift/metashape.py",
        "orthoswift/runner.py",
        "orthoswift/version.py",
        "orthoswift/requirements.txt",
        "orthoswift/assets/fonts/SpaceGrotesk-Bold.ttf",
        "orthoswift/assets/fonts/InterVariable.ttf",
        "install-windows.bat",
        "install-macos.command",
        "install-macos-linux.sh",
        "requirements.txt",
        "README.md",
        "LICENSE",
        "SECURITY.md",
        "CONTRIBUTING.md",
        "build_release.py",
    ]
    for rf in required_files:
        assert (root / rf).exists(), f"Missing required file: {rf}"
