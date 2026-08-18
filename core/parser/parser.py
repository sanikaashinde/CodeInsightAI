import ast
from pathlib import Path

from radon.complexity import cc_visit

from schemas.analysis_schema import (
    AnalysisResult,
    FunctionInfo,
    ClassInfo
)


class PythonParser:

    def parse(self, filepath):

        filepath = Path(filepath)

        source = filepath.read_text(
            encoding="utf-8",
            errors="ignore"
        )

        try:
            tree = ast.parse(source)
            syntax_error = False
            syntax_error_message = None
        except SyntaxError as e:
            tree = ast.parse("")
            syntax_error = True
            syntax_error_message = str(e)

        imports = []
        variables = []
        functions = []
        classes = []

        lines = source.splitlines()

        blank_lines = sum(
            1 for line in lines
            if not line.strip()
        )

        comment_lines = sum(
            1 for line in lines
            if line.strip().startswith("#")
        )

        todo_count = sum(
            1 for line in lines
            if "TODO" in line.upper()
        )

        fixme_count = sum(
            1 for line in lines
            if "FIXME" in line.upper()
        )

        # ==================================================
        # AST ANALYSIS
        # ==================================================

        for node in ast.walk(tree):

            if isinstance(node, ast.Import):

                for alias in node.names:
                    imports.append(alias.name)

            elif isinstance(node, ast.ImportFrom):

                if node.module:
                    imports.append(node.module)

            elif isinstance(node, ast.Assign):

                for target in node.targets:

                    if isinstance(target, ast.Name):
                        variables.append(target.id)

            elif isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef)
            ):

                params = [
                    arg.arg
                    for arg in node.args.args
                ]

                decorators = []

                for decorator in node.decorator_list:

                    try:
                        decorators.append(
                            ast.unparse(decorator)
                        )
                    except Exception:
                        pass

                return_type = None

                if node.returns:

                    try:
                        return_type = ast.unparse(
                            node.returns
                        )
                    except Exception:
                        pass

                length = (
                    getattr(node, "end_lineno", node.lineno)
                    - node.lineno
                    + 1
                )

                functions.append(
                    FunctionInfo(
                        name=node.name,
                        parameters=params,
                        return_type=return_type,
                        decorators=decorators,
                        docstring=ast.get_docstring(node),
                        line_number=node.lineno,
                        is_async=isinstance(
                            node,
                            ast.AsyncFunctionDef
                        ),
                        length=length,
                        has_return=any(
                            isinstance(child, ast.Return)
                            for child in ast.walk(node)
                        ),
                    )
                )

            elif isinstance(node, ast.ClassDef):

                bases = []

                for base in node.bases:

                    try:
                        bases.append(
                            ast.unparse(base)
                        )
                    except Exception:
                        pass

                methods = []

                for item in node.body:

                    if isinstance(
                        item,
                        (
                            ast.FunctionDef,
                            ast.AsyncFunctionDef
                        )
                    ):
                        methods.append(item.name)

                classes.append(
                    ClassInfo(
                        name=node.name,
                        bases=bases,
                        methods=methods,
                        docstring=ast.get_docstring(node),
                        line_number=node.lineno,
                        method_count=len(methods),
                    )
                )

        # ==================================================
        # COMPLEXITY
        # ==================================================

        try:

            complexity_results = cc_visit(source)

            complexity_map = {
                item.name: item.complexity
                for item in complexity_results
            }

            for function in functions:

                function.complexity = complexity_map.get(
                    function.name,
                    1
                )

        except Exception:

            for function in functions:
                function.complexity = 1

        # ==================================================
        # RESULT
        # ==================================================

        return AnalysisResult(

            file_name=filepath.name,

            file_path=str(filepath),

            extension=filepath.suffix,

            language="Python",

            imports=imports,

            variables=variables,

            functions=functions,

            classes=classes,

            total_lines=len(lines),

            blank_lines=blank_lines,

            comment_lines=comment_lines,

            file_size=filepath.stat().st_size,

            todo_count=todo_count,

            fixme_count=fixme_count,

            syntax_error=syntax_error,

            syntax_error_message=syntax_error_message,

            total_functions=len(functions),

            total_classes=len(classes),

            total_imports=len(imports),

            total_variables=len(variables),
        )
