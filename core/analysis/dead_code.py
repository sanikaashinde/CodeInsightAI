import ast
from pathlib import Path


class DeadCodeAnalyzer:
    """
    Conservative AST-based dead code analyzer.

    Detects:
    - Unused functions
    - Unreachable statements
    - Empty functions
    - Empty classes
    - Unused local/module variables
    - Unused imports

    Designed to reduce false positives from:
    - Framework entry points
    - ORM models
    - Exported module objects
    - Private/internal helpers
    """

    def analyze(self, project_folder):

        project_folder = Path(project_folder)

        definitions = {}
        all_function_calls = set()
        issues = []

        for file in project_folder.rglob("*.py"):

            try:
                source = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                tree = ast.parse(source)

            except (SyntaxError, UnicodeError, OSError):
                continue

            relative_file = file.relative_to(
                project_folder
            ).as_posix()

            visitor = _DeadCodeVisitor()

            # Visit the complete file
            visitor.visit(tree)

            # Finalize exactly ONCE for this file
            visitor.finalize()

            # ------------------------------------------------
            # Store function definitions
            # ------------------------------------------------

            for func in visitor.functions:

                key = (
                    f"{relative_file}:"
                    f"{func['name']}:"
                    f"{func['line']}"
                )

                definitions[key] = {
                    "name": func["name"],
                    "file": relative_file,
                    "line": func["line"],
                }

            # ------------------------------------------------
            # Store function calls
            # ------------------------------------------------

            all_function_calls.update(
                visitor.called_functions
            )

            # ------------------------------------------------
            # Store visitor issues
            # ------------------------------------------------

            for issue in visitor.issues:

                issue["file"] = relative_file

                issues.append(issue)

        # ==================================================
        # UNUSED FUNCTIONS
        # ==================================================

        ignored_framework_functions = {
            "show",
            "run",
            "render",
            "main",
        }

        for _, info in definitions.items():

            function_name = info["name"]

            # Ignore framework entry points
            if function_name in ignored_framework_functions:
                continue

            # Ignore private/dunder functions
            if function_name.startswith("_"):
                continue

            # Function is actually called
            if function_name in all_function_calls:
                continue

            issues.append(
                {
                    "type": "Unused Function",
                    "file": info["file"],
                    "line": info["line"],
                    "message": (
                        f"{function_name}() is never called "
                        "within the analyzed repository"
                    ),
                    "severity": "Medium",
                }
            )

        return issues

    # ==================================================
    # SUMMARY
    # ==================================================

    def summary(self, issues):

        return {
            "total": len(issues),

            "unused_functions": sum(
                1
                for issue in issues
                if issue["type"] == "Unused Function"
            ),

            "unreachable_code": sum(
                1
                for issue in issues
                if issue["type"] == "Unreachable Code"
            ),

            "empty_functions": sum(
                1
                for issue in issues
                if issue["type"] == "Empty Function"
            ),

            "empty_classes": sum(
                1
                for issue in issues
                if issue["type"] == "Empty Class"
            ),

            "unused_variables": sum(
                1
                for issue in issues
                if issue["type"] == "Unused Variable"
            ),

            "unused_imports": sum(
                1
                for issue in issues
                if issue["type"] == "Unused Import"
            ),
        }


# ============================================================
# DEAD CODE VISITOR
# ============================================================


class _DeadCodeVisitor(ast.NodeVisitor):

    def __init__(self):

        self.functions = []

        # Function names that are actually called
        self.called_functions = set()

        # Names that are actually read/used
        self.used_names = set()

        self.issues = []

        self.class_depth = 0
        self.function_depth = 0

        self.imports = []
        self.variables = []

    # ========================================================
    # FUNCTIONS
    # ========================================================

    def visit_FunctionDef(self, node):

        self.functions.append(
            {
                "name": node.name,
                "line": node.lineno,
            }
        )

        # ----------------------------------------------------
        # Empty function detection
        # ----------------------------------------------------

        meaningful_body = [
            statement
            for statement in node.body
            if not (
                isinstance(statement, ast.Expr)
                and isinstance(
                    getattr(statement, "value", None),
                    ast.Constant,
                )
                and isinstance(
                    getattr(statement.value, "value", None),
                    str,
                )
            )
        ]

        if (
            len(meaningful_body) == 1
            and isinstance(
                meaningful_body[0],
                ast.Pass,
            )
        ):

            self.issues.append(
                {
                    "type": "Empty Function",
                    "line": node.lineno,
                    "message": (
                        f"{node.name}() contains only pass"
                    ),
                    "severity": "Low",
                }
            )

        # ----------------------------------------------------
        # Unreachable statements
        # ----------------------------------------------------

        terminated = False

        for statement in node.body:

            if terminated:

                self.issues.append(
                    {
                        "type": "Unreachable Code",
                        "line": getattr(
                            statement,
                            "lineno",
                            0,
                        ),
                        "message": (
                            f"Statement after termination "
                            f"in {node.name}()"
                        ),
                        "severity": "Medium",
                    }
                )

            if isinstance(
                statement,
                (
                    ast.Return,
                    ast.Raise,
                    ast.Break,
                    ast.Continue,
                ),
            ):

                terminated = True

        self.function_depth += 1

        self.generic_visit(node)

        self.function_depth -= 1

    # ========================================================

    def visit_AsyncFunctionDef(self, node):

        self.functions.append(
            {
                "name": node.name,
                "line": node.lineno,
            }
        )

        self.function_depth += 1

        self.generic_visit(node)

        self.function_depth -= 1

    # ========================================================
    # CLASSES
    # ========================================================

    def visit_ClassDef(self, node):

        meaningful_body = [
            statement
            for statement in node.body
            if not (
                isinstance(statement, ast.Expr)
                and isinstance(
                    getattr(statement, "value", None),
                    ast.Constant,
                )
                and isinstance(
                    getattr(statement.value, "value", None),
                    str,
                )
            )
        ]

        if (
            len(meaningful_body) == 1
            and isinstance(
                meaningful_body[0],
                ast.Pass,
            )
        ):

            self.issues.append(
                {
                    "type": "Empty Class",
                    "line": node.lineno,
                    "message": (
                        f"Class {node.name} contains only pass"
                    ),
                    "severity": "Low",
                }
            )

        self.class_depth += 1

        self.generic_visit(node)

        self.class_depth -= 1

    # ========================================================
    # FUNCTION CALLS
    # ========================================================

    def visit_Call(self, node):

        if isinstance(node.func, ast.Name):

            self.called_functions.add(
                node.func.id
            )

        elif isinstance(node.func, ast.Attribute):

            self.called_functions.add(
                node.func.attr
            )

        self.generic_visit(node)

    # ========================================================
    # IMPORTS
    # ========================================================

    def visit_Import(self, node):

        for alias in node.names:

            name = (
                alias.asname
                or alias.name.split(".")[0]
            )

            self.imports.append(
                {
                    "name": name,
                    "line": node.lineno,
                }
            )

        self.generic_visit(node)

    # ========================================================

    def visit_ImportFrom(self, node):

        for alias in node.names:

            if alias.name == "*":
                continue

            name = alias.asname or alias.name

            self.imports.append(
                {
                    "name": name,
                    "line": node.lineno,
                }
            )

        self.generic_visit(node)

    # ========================================================
    # VARIABLE ASSIGNMENTS
    # ========================================================

    def visit_Assign(self, node):

        # Ignore class-level attributes.
        #
        # Example:
        #
        # class Customer:
        #     id = Column(...)
        #     customer_id = Column(...)

        if (
            self.class_depth > 0
            and self.function_depth == 0
        ):

            self.generic_visit(node)
            return

        for target in node.targets:

            self._collect_variable(
                target,
                node.lineno,
            )

        self.generic_visit(node)

    # ========================================================

    def visit_AnnAssign(self, node):

        if (
            self.class_depth > 0
            and self.function_depth == 0
        ):

            self.generic_visit(node)
            return

        self._collect_variable(
            node.target,
            node.lineno,
        )

        self.generic_visit(node)

    # ========================================================

    def visit_AugAssign(self, node):

        if isinstance(node.target, ast.Name):

            self.used_names.add(
                node.target.id
            )

        self.generic_visit(node)

    # ========================================================
    # VARIABLE USAGE
    # ========================================================

    def visit_Name(self, node):

        if isinstance(node.ctx, ast.Load):

            self.used_names.add(
                node.id
            )

        self.generic_visit(node)

    # ========================================================
    # VARIABLE COLLECTION
    # ========================================================

    def _collect_variable(self, target, line):

        # Ignore:
        # self.x = ...
        # object.x = ...

        if isinstance(target, ast.Attribute):
            return

        # Ignore:
        # data[index] = ...

        if isinstance(target, ast.Subscript):
            return

        if isinstance(target, ast.Name):

            name = target.id

            # Ignore throw-away variables
            if name.startswith("_"):
                return

            self.variables.append(
                {
                    "name": name,
                    "line": line,
                    "function_depth": self.function_depth,
                }
            )

        elif isinstance(
            target,
            (ast.Tuple, ast.List),
        ):

            for element in target.elts:

                self._collect_variable(
                    element,
                    line,
                )

    # ========================================================
    # FINALIZE
    # ========================================================

    def finalize(self):

        # ==================================================
        # UNUSED IMPORTS
        # ==================================================

        reported_imports = set()

        for item in self.imports:

            name = item["name"]

            if name in reported_imports:
                continue

            if name not in self.used_names:

                self.issues.append(
                    {
                        "type": "Unused Import",
                        "line": item["line"],
                        "message": (
                            f"Imported name '{name}' "
                            "is never used within "
                            "the analyzed scope"
                        ),
                        "severity": "Low",
                    }
                )

                reported_imports.add(name)

        # ==================================================
        # UNUSED VARIABLES
        # ==================================================

        reported_variables = set()

        ignored_module_objects = {
            "app",
            "router",
            "engine",
            "SessionLocal",
            "Base",
            "metadata",
        }

        for item in self.variables:

            name = item["name"]

            # Report each variable only once
            if name in reported_variables:
                continue

            # Ignore common module-level exported objects
            if (
                item["function_depth"] == 0
                and name in ignored_module_objects
            ):
                continue

            if name not in self.used_names:

                self.issues.append(
                    {
                        "type": "Unused Variable",
                        "line": item["line"],
                        "message": (
                            f"Variable '{name}' "
                            "is assigned but never used "
                            "within the analyzed scope"
                        ),
                        "severity": "Low",
                    }
                )

                reported_variables.add(name)


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

DeadCodeDetector = DeadCodeAnalyzer