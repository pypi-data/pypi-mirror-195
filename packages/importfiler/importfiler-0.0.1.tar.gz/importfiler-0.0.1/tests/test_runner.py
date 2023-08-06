from importfiler import _runner


def test_module_math_only_contains_math():
    res = _runner.get_all_modules_importtime("math")
    assert res.module == "math"
    assert ["math"] == list(res.import_times)
    assert [] == list(res.submodules)
    assert res.total_time > 0


def test_module_pytest():
    res = _runner.get_all_modules_importtime("black")

    # check import times
    for module in {"black", "click"}:
        assert module in res.import_times, module
    heaviest_modules = [
        x for x, _ in sorted(res.import_times.items(), key=lambda x: -x[1])
    ][:5]
    assert "black" in heaviest_modules
    assert "click" in heaviest_modules

    # check submodules
    assert "black.mode" == res.submodules["black"][0]
    assert "click.core" == res.submodules["click"][0]


def test_dependencies_math_only_contains_math():
    res = _runner.get_dependencies_importtime("math")
    assert res.module == "math"
    assert ["math"] == list(res.import_times)
    assert res.total_time > 0


def test_dependencies_json():
    res = _runner.get_dependencies_importtime("click")
    assert "datetime" in res.import_times
    assert "_datetime" not in res.import_times