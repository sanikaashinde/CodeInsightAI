import ast


class ContextBuilder:

    MAX_FILE_CONTENT = 500


    def _extract_python_info(self, code: str):

        classes = []
        functions = []
        imports = []

        try:
            tree = ast.parse(code)

            for node in ast.walk(tree):

                if isinstance(node, ast.ClassDef):
                    classes.append(node.name)

                elif isinstance(node, ast.FunctionDef):
                    functions.append(node.name)

                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)

                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    imports.append(module)

        except Exception:
            pass

        return classes, functions, imports


    def build_llm_context(self, project_context):

        output = []

        output.append("# Repository Summary\n")

        summary = project_context["summary"]

        output.append(
            f"""
Total Files : {summary['total_files']}
Python Files : {summary['python_files']}
Directories : {summary['directories']}
"""
        )

        output.append("\n=============================\n")

        for file in project_context["files"]:

            path = file["path"]

            content = file.get("content", "")

            classes, functions, imports = self._extract_python_info(content)

            snippet = content[:self.MAX_FILE_CONTENT]

            output.append(
                f"""
File:
{path}

Imports:
{", ".join(imports) if imports else "None"}

Classes:
{", ".join(classes) if classes else "None"}

Functions:
{", ".join(functions) if functions else "None"}

Preview:
{snippet}

--------------------------------------------
"""
            )

        return "\n".join(output)