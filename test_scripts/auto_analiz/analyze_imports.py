import os
import ast

def get_imports(file_path: str) -> list[str]:
    if 'venv' in file_path:
        return []

    with open(file_path, 'r', encoding='utf-8') as file:
        tree = ast.parse(file.read())

    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ''
            imports.extend(f"{module}.{alias.name}" for alias in node.names)

    return imports


def analyze_project(project_path: str) -> dict[str, list[str]]:
    dependencies: dict[str, list[str]] = {}
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                if 'venv' not in file_path:
                    relative_path = os.path.relpath(file_path, project_path)
                    imports = get_imports(file_path)
                    if imports:
                        dependencies[relative_path] = imports

    return dependencies


def filter_dependencies(dependencies: dict[str, list[str]]) -> dict[str, list[str]]:
    filtered: dict[str, list[str]] = {}
    for file, imports in dependencies.items():
        project_imports = [imp for imp in imports if
                           not imp.startswith(('django', 'rest_framework', 'numpy', 'pandas'))]
        if project_imports:
            filtered[file] = project_imports
    return filtered


def print_dependencies(dependencies: dict[str, list[str]]) -> None:
    files_count = len(dependencies.keys())
    print('Total files:', files_count)
    import_count = sum([len(x) for x in dependencies.values()])
    print('Total imports:', import_count)

    sorted_files = sorted(list(dependencies.keys()), key=lambda k: len(dependencies[k]), reverse=True)
    for file in sorted_files:
        import_count = len(dependencies[file])
        print(f"\n{file}: {import_count} import")
        imports = dependencies[file]
        for imp in imports:
            print(f'  - {imp}')


def main(project_path: str) -> None:
    raw_dependencies: dict[str, list[str]] = analyze_project(project_path)
    filtered_dependencies: dict[str, list[str]] = filter_dependencies(raw_dependencies)
    print_dependencies(filtered_dependencies)


if __name__ == "__main__":
    main(r"C:\Users\Игорь\PycharmProjects\ContentClassificator")
