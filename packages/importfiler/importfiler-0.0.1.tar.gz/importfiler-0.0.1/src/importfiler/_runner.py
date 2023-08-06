import collections
import dataclasses
import re
import subprocess
import sys

IMPORT_RE = re.compile(r"^import time: +(\d+) \| +(\d+) \|( +)([^ ]+)$")


@dataclasses.dataclass
class ModuleProfileReport:
    module: str
    total_time: int
    import_times: dict[str, int]
    submodules: dict[str, list[str]]

@dataclasses.dataclass
class DependenciesProfileReport:
    module: str
    total_time: int
    import_times: dict[str, int]


def _is_namespace_package(module):
    if not hasattr(module, "__path__"):
        return False
    if module.__path__.__class__.__name__ == "_NamespacePath":
        return True
    return False


def _find_top_level_modules():
    modules_to_report = tuple()
    for module_name, module in sorted(sys.modules.items(), key=lambda x: len(x[0])):
        if _is_namespace_package(module):
            continue
        if module_name.startswith(modules_to_report):
            continue  # Part of a package we have already reported
        modules_to_report = (*modules_to_report, module_name + ".")
    return {m[:-1] for m in modules_to_report}


def _get_importtime_output(module_name):
    return subprocess.run(
        [sys.executable, "-X", "importtime", "-c", f"import {module_name}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ).stderr


def get_all_modules_importtime(module_name):
    """Gets self time for all modules"""
    import_times = {}
    total_time = None
    found_site = False
    lines = _get_importtime_output(module_name).splitlines()
    for line in lines:
        if not(match := IMPORT_RE.match(line)):
            continue
        if match.group(4) == "site":
            found_site = True
            continue
        if not found_site:
            continue
        if match.group(4) == module_name:
            total_time = int(match.group(2))
        import_times[match.group(4)] = int(match.group(1))

    __import__(module_name)
    top_level_modules = _find_top_level_modules() & set(import_times)
    res_import_times = collections.defaultdict(int)
    submodules = collections.defaultdict(list)
    for module, import_time in sorted(import_times.items(), key=lambda x: -x[1]):
        for tm in top_level_modules:
            if f"{module}.".startswith(f"{tm}."):
                break
        else:
            continue
        res_import_times[tm] += import_time
        if module != tm:
            submodules[tm].append(module)
    return ModuleProfileReport(module_name, total_time, res_import_times, submodules)



def get_dependencies_importtime(module_name):
    """Gets total time for dependencies"""
    import_times = {}
    total_time = None
    found_site = False
    lines = _get_importtime_output(module_name).splitlines()
    modules_hierarchy = []
    for line in lines:
        if not(match := IMPORT_RE.match(line)):
            continue
        if match.group(4) == "site":
            found_site = True
            continue
        if not found_site:
            continue
        if match.group(4) == module_name:
            total_time = int(match.group(2))
        import_times[match.group(4)] = int(match.group(2))
        modules_hierarchy.append((len(match.group(3)), match.group(4)))

    def is_a_dependency(candidate):
        """Checks if module_name depends in candidate directly"""
        if f"{candidate}.".startswith(f"{module_name}."):
            return False
        candidate_indent = None
        for indent, module in modules_hierarchy:
            if module == candidate:
                candidate_indent = indent
                continue
            if candidate_indent is None:
                continue
            # Found the module, look for parent
            if indent >= candidate_indent:
                continue
            if f"{module}.".startswith(f"{module_name}."):
                return True
            else:
                candidate_indent = None
        return False

    result_times = {
        module: import_time
        for module, import_time
        in import_times.items()
        if is_a_dependency(module) or module == module_name
    }

    return DependenciesProfileReport(
        module_name,
        total_time,
        result_times,
    )
