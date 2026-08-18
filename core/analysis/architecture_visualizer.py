from pathlib import Path
from collections import defaultdict
import ast


class ArchitectureVisualizer:

    IGNORE = {
        ".git",
        ".venv",
        "__pycache__",
        "node_modules",
        ".idea",
        ".vscode",
        "env",
        "venv",
        "build",
        "dist",
    }

    # =======================================================
    # Analyze Repository
    # =======================================================

    def analyze(self, project_folder):

        project_folder = Path(project_folder)

        folders = defaultdict(list)

        imports = defaultdict(list)

        packages = defaultdict(int)

        modules = []

        tree = []

        total_python_files = 0

        for file in project_folder.rglob("*"):

            if any(part in self.IGNORE for part in file.parts):
                continue

            relative = file.relative_to(project_folder)

            if file.is_dir():

                folders[str(relative.parent)].append(relative.name)

                continue

            tree.append(str(relative))

            if file.suffix != ".py":
                continue

            total_python_files += 1

            module = relative.with_suffix("").as_posix().replace("/", ".")

            modules.append(module)

            packages[module.split(".")[0]] += 1

            try:

                source = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                ast_tree = ast.parse(source)

            except Exception:

                continue

            imported = []

            for node in ast.walk(ast_tree):

                if isinstance(node, ast.Import):

                    for alias in node.names:

                        imported.append(alias.name)

                elif isinstance(node, ast.ImportFrom):

                    if node.module:

                        imported.append(node.module)

            imports[module] = sorted(set(imported))

        return {

            "folders": dict(folders),

            "imports": dict(imports),

            "packages": dict(packages),

            "modules": sorted(modules),

            "tree": sorted(tree),

            "summary": {

                "modules": len(modules),

                "packages": len(packages),

                "python_files": total_python_files,

            }

        }

    # =======================================================
    # Folder Tree
    # =======================================================

    def folder_tree(self, result):

        return result["tree"]

    # =======================================================
    # Module Dependency
    # =======================================================

    def dependency_table(self, result):

        rows = []

        for module, imports in result["imports"].items():

            rows.append({

                "Module": module,

                "Imports": len(imports),

                "Dependencies": ", ".join(imports)

            })

        return rows

    # =======================================================
    # Package Summary
    # =======================================================

    def package_summary(self, result):

        rows = []

        for package, count in sorted(

            result["packages"].items(),

            key=lambda x: x[1],

            reverse=True,

        ):

            rows.append({

                "Package": package,

                "Modules": count,

            })

        return rows

    # =======================================================
    # Largest Package
    # =======================================================

    def largest_package(self, result):

        if not result["packages"]:

            return None

        package = max(

            result["packages"],

            key=result["packages"].get,

        )

        return {

            "package": package,

            "modules": result["packages"][package],

        }

    # =======================================================
    # Root Modules
    # =======================================================

    def root_modules(self, result):

        roots = []

        for module in result["modules"]:

            if "." not in module:

                roots.append(module)

        return sorted(roots)

    # =======================================================
    # Leaf Modules
    # =======================================================

    def leaf_modules(self, result):

        leaves = []

        imported = set()

        for deps in result["imports"].values():

            imported.update(deps)

        for module in result["modules"]:

            if module not in imported:

                leaves.append(module)

        return sorted(leaves)

    # =======================================================
    # Markdown Export
    # =======================================================

    def markdown(self, result):

        md = "# Project Architecture\n\n"

        md += "## Summary\n\n"

        md += f"- Python Files: {result['summary']['python_files']}\n"

        md += f"- Packages: {result['summary']['packages']}\n"

        md += f"- Modules: {result['summary']['modules']}\n\n"

        md += "## Project Tree\n\n"

        for item in result["tree"]:

            md += f"- {item}\n"

        md += "\n"

        md += "## Module Dependencies\n\n"

        for module, deps in result["imports"].items():

            md += f"### {module}\n"

            if deps:

                for dep in deps:

                    md += f"- {dep}\n"

            else:

                md += "- No Imports\n"

            md += "\n"

        return md