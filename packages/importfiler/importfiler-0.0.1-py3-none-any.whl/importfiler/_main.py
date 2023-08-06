from ._cli import parse_args
from ._runner import get_all_modules_importtime
from ._runner import get_dependencies_importtime


def _format_submodules(submodules):
    if not submodules:
        return ""
    submodules = iter(submodules)
    res = next(submodules)
    while len(res) < 60:
        try:
            res += ", " + next(submodules)
        except StopIteration:
            return res
    return res + ", ..."


def main():
    args = parse_args()
    _UNIT_OPERATIONS = {
        "s": lambda x: x / 1_000_000,
        "ms": lambda x: x / 1_000,
        "us": lambda x: x,
        "%": lambda x: x / result.total_time * 100,
    }
    if args.mode == "all_modules":
        result = get_all_modules_importtime(args.module_name)
        rows = [["modules:", f"time({args.unit})", "submodules"]]
        for module_name, import_time in sorted(
            result.import_times.items(), key=lambda x: -x[1]
        ):
            import_time = _UNIT_OPERATIONS[args.unit](import_time)
            if import_time <= 1:
                continue
            rows.append(
                [
                    f"{module_name}",
                    f"{int(import_time)} {args.unit}",
                    _format_submodules(result.submodules[module_name]),
                ]
            )
        padding_0 = max(len(x[0]) for x in rows) + 1
        padding_1 = max(len(x[1]) for x in rows) + 1
        rows.insert(1, ["-" * padding_0, "-" * padding_1, "-" * 20])
        for module, imp_time, modules in rows:
            print(
                f"{module.ljust(padding_0)} {imp_time.ljust(padding_1)} {modules}"
            )
    elif args.mode == "dependencies":
        result = get_dependencies_importtime(args.module_name)
        rows = [["modules:", f"time({args.unit})"]]
        for module_name, import_time in sorted(
            result.import_times.items(), key=lambda x: -x[1]
        ):
            import_time = _UNIT_OPERATIONS[args.unit](import_time)
            if import_time <= 1:
                continue
            rows.append(
                [
                    f"{module_name}",
                    f"{int(import_time)} {args.unit}",
                ]
            )
        padding_0 = max(len(x[0]) for x in rows) + 1
        padding_1 = max(len(x[1]) for x in rows) + 1
        rows.insert(1, ["-" * padding_0, "-" * padding_1])
        for module, imp_time in rows:
            print(
                f"{module.ljust(padding_0)} {imp_time.ljust(padding_1)}"
            )
