from importlib.metadata import version

try:
    __version__ = version("robotframework-implicitcontext")
except Exception:  # pragma: no cover
    pass
