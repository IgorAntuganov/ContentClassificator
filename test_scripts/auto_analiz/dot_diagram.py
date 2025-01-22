import os
import sys
from collections import defaultdict
from analyze_imports import analyze_project, filter_dependencies

EXCLUDED_DIRS = {'test_scripts', 'fonts_test', 'test_scripts\\mandelbrot', 'test_scripts\\auto_analiz'}


def sanitize_name(name: str) -> str:
    return name.replace('.', '_')


def is_builtin_module(module_name: str) -> bool:
    return module_name in sys.builtin_module_names or module_name in sys.stdlib_module_names


def process_dependencies(dependencies: dict[str, list[str]], excluded_dirs: set[str]) -> tuple[
    dict[str, set[str]], dict[str, set[str]], set[str]]:
    modules = defaultdict(set)
    module_dependencies = defaultdict(set)
    builtin_modules = set()

    for file, imports in dependencies.items():
        module = os.path.dirname(file) or 'root'
        if module in excluded_dirs:
            continue
        modules[module].add(file)
        for imp in imports:
            imp_module = imp.split('.')[0]
            if is_builtin_module(imp_module):
                builtin_modules.add(imp_module)
            elif imp_module != module and imp_module not in excluded_dirs:
                module_dependencies[module].add(imp_module)

    return modules, module_dependencies, builtin_modules


def create_builtin_cluster(builtin_modules: set[str]) -> str:
    dot = "    subgraph cluster_builtin {\n"
    dot += "        label = \"Built-in Modules\";\n"
    dot += "        style = filled;\n"
    dot += "        color = lightyellow;\n"
    for module in builtin_modules:
        safe_module = sanitize_name(module)
        dot += f"        {safe_module} [label=\"{module}\", fillcolor=yellow];\n"
    dot += "    }\n"
    return dot


def create_project_clusters(modules: dict[str, set[str]]) -> str:
    dot = ""
    for module, files in modules.items():
        safe_module = sanitize_name(module)
        dot += f"    subgraph cluster_{safe_module} {{\n"
        dot += f"        label = \"{module}\";\n"
        dot += "        style = filled;\n"
        dot += "        color = lightgrey;\n"
        for file in files:
            file_id = sanitize_name(os.path.basename(file))
            dot += f"        {file_id} [label=\"{os.path.basename(file)}\"];\n"
        dot += "    }\n"
    return dot


def create_edges(module_dependencies: dict[str, set[str]]) -> str:
    dot = ""
    for module, deps in module_dependencies.items():
        safe_module = sanitize_name(module)
        for dep in deps:
            safe_dep = sanitize_name(dep)
            if is_builtin_module(dep):
                dot += f"    {safe_module} -> {safe_dep};\n"
            else:
                dot += f"    {safe_module} -> {safe_dep} [lhead=cluster_{safe_dep}, ltail=cluster_{safe_module}];\n"
    return dot


def generate_graphviz(dependencies: dict[str, list[str]]) -> str:

    modules, module_dependencies, builtin_modules = process_dependencies(dependencies, EXCLUDED_DIRS)

    dot = "digraph DependencyGraph {\n"
    dot += "    rankdir=TB;\n"
    dot += "    node [shape=box, style=filled, fillcolor=lightblue];\n"

    dot += create_builtin_cluster(builtin_modules)
    dot += create_project_clusters(modules)
    dot += create_edges(module_dependencies)

    dot += "}\n"
    return dot


def main(project_path) -> None:
    raw_dependencies: dict[str, list[str]] = analyze_project(project_path)
    filtered_dependencies: dict[str, list[str]] = filter_dependencies(raw_dependencies)

    graphviz_output = generate_graphviz(filtered_dependencies)
    print(graphviz_output)


if __name__ == "__main__":
    main(r"C:\Users\Игорь\PycharmProjects\ContentClassificator")
