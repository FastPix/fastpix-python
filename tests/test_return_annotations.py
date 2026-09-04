"""Every resource method's declared return type must be the class it actually
unmarshals on the success path. Guards against annotations drifting from the
`{success, data}` envelope the API returns."""

import ast
import pathlib

import pytest

PKG = pathlib.Path(__file__).resolve().parent.parent / "fastpix_python"
SKIP = {"basesdk.py", "sdk.py", "httpclient.py", "sdkconfiguration.py", "_version.py", "__init__.py"}


def _success_unmarshal_class(fn: ast.FunctionDef) -> str | None:
    """Return the models.X class passed to unmarshal_json_response inside the
    `if utils.match_response(http_res, "2xx", ...)` branch, if any."""
    for node in ast.walk(fn):
        if not isinstance(node, ast.If):
            continue
        test = node.test
        if not (isinstance(test, ast.Call) and getattr(test.func, "attr", "") == "match_response"):
            continue
        status = test.args[1] if len(test.args) > 1 else None
        if not (isinstance(status, ast.Constant) and str(status.value).startswith("2")):
            continue
        for inner in ast.walk(node):
            if isinstance(inner, ast.Return) and isinstance(inner.value, ast.Call):
                call = inner.value
                if getattr(call.func, "id", "") == "unmarshal_json_response" and call.args:
                    return ast.unparse(call.args[0])
    return None


def _cases():
    for path in sorted(PKG.glob("*.py")):
        if path.name in SKIP:
            continue
        tree = ast.parse(path.read_text())
        for cls in (n for n in tree.body if isinstance(n, ast.ClassDef)):
            for fn in (n for n in cls.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))):
                if fn.name.startswith("_") or fn.returns is None:
                    continue
                actual = _success_unmarshal_class(fn)
                if actual:
                    yield pytest.param(path.name, fn.name, ast.unparse(fn.returns), actual, id=f"{path.stem}.{fn.name}")


CASES = list(_cases())


def test_scan_found_methods():
    assert len(CASES) > 100


@pytest.mark.parametrize("module,method,declared,actual", CASES)
def test_return_annotation_matches_unmarshaled_class(module, method, declared, actual):
    assert declared == actual, f"{module}::{method} declares {declared} but unmarshals {actual}"
