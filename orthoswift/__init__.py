"""OrthoSWIFT adapter for Agisoft Metashape Professional."""

from .version import __version__

__author__ = "OrthoSWIFT"
__all__ = ["__version__", "run", "run_agriculture_pipeline"]


def __getattr__(name: str):
    """Load the geospatial runtime only when an API entry point is requested."""
    if name == "run":
        from .runner import run

        return run
    if name == "run_agriculture_pipeline":
        from .core.pipeline import run_agriculture_pipeline

        return run_agriculture_pipeline
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
