from pathlib import Path
import ast


class DocumentationGenerator:
    """
    Automatically generates project documentation.

    Generates:
    - Project Overview
    - File Summary
    - Classes
    - Functions
    - Imports
    """

    def generate(self, project_folder):

        project_folder = Path(project_folder)

        markdown = []

        markdown.append("# Project Documentation\n")

        total_files = 0
        total_functions = 0
        total_classes = 0

        for file in sorted(project_folder.rglob("*.py")):

            total_files += 1

            try:

                source = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                tree = ast.parse(source)

            except Exception:

                continue

            imports = []
            functions = []
            classes = []

            # -----------------------------------
            # Walk AST
            # -----------------------------------

            for node in ast.walk(tree):

                if isinstance(node, ast.Import):

                    for alias in node.names:

                        imports.append(alias.name)

                elif isinstance(node, ast.ImportFrom):

                    if node.module:

                        imports.append(node.module)

                elif isinstance(node, ast.FunctionDef):

                    total_functions += 1

                    functions.append(

                        {
                            "name": node.name,
                            "line": node.lineno,
                            "doc": ast.get_docstring(node),
                            "args": [
                                a.arg
                                for a in node.args.args
                            ],
                        }

                    )

                elif isinstance(node, ast.AsyncFunctionDef):

                    total_functions += 1

                    functions.append(

                        {
                            "name": node.name,
                            "line": node.lineno,
                            "doc": ast.get_docstring(node),
                            "args": [
                                a.arg
                                for a in node.args.args
                            ],
                        }

                    )

                elif isinstance(node, ast.ClassDef):

                    total_classes += 1

                    methods = []

                    for item in node.body:

                        if isinstance(
                            item,
                            (
                                ast.FunctionDef,
                                ast.AsyncFunctionDef,
                            ),
                        ):

                            methods.append(item.name)

                    classes.append(

                        {
                            "name": node.name,
                            "line": node.lineno,
                            "doc": ast.get_docstring(node),
                            "methods": methods,
                        }

                    )

            # -----------------------------------
            # File Header
            # -----------------------------------

            markdown.append(
                f"\n---\n# {file.relative_to(project_folder)}\n"
            )

            if imports:

                markdown.append("## Imports\n")

                for imp in sorted(set(imports)):

                    markdown.append(f"- {imp}")

            if classes:

                markdown.append("\n## Classes\n")

                for cls in classes:

                    markdown.append(
                        f"### {cls['name']}"
                    )

                    markdown.append(
                        f"Line: {cls['line']}"
                    )

                    if cls["doc"]:

                        markdown.append(
                            cls["doc"]
                        )

                    if cls["methods"]:

                        markdown.append(
                            "\nMethods:"
                        )

                        for m in cls["methods"]:

                            markdown.append(
                                f"- {m}"
                            )

            if functions:

                markdown.append(
                    "\n## Functions\n"
                )

                for func in functions:

                    markdown.append(
                        f"### {func['name']}"
                    )

                    markdown.append(
                        f"Line: {func['line']}"
                    )

                    if func["args"]:

                        markdown.append(
                            "Parameters: "
                            + ", ".join(func["args"])
                        )

                    if func["doc"]:

                        markdown.append(
                            func["doc"]
                        )

        # ---------------------------------------
        # Project Summary
        # ---------------------------------------

        header = [

            "# CodeInsight AI Documentation\n",

            f"Total Files : {total_files}",

            f"Total Functions : {total_functions}",

            f"Total Classes : {total_classes}",

            "\n---\n",

        ]

        return "\n".join(header + markdown)

    # =======================================

    def statistics(self, markdown):

        return {

            "characters": len(markdown),

            "lines": len(markdown.splitlines()),

            "words": len(markdown.split()),

        }