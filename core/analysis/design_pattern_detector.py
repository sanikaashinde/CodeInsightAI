import ast
from pathlib import Path


class DesignPatternDetector:
    """
    Detect common software design patterns using
    lightweight AST heuristics.

    Supported patterns:
    - Singleton
    - Factory
    - Builder
    - Strategy
    - Observer
    - Decorator
    - Adapter
    - Facade
    """

    def analyze(self, project_folder):

        project_folder = Path(project_folder)

        patterns = []

        for file in project_folder.rglob("*.py"):

            try:

                source = file.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )

                tree = ast.parse(source)

            except Exception:

                continue

            for node in tree.body:

                if isinstance(node, ast.ClassDef):

                    detected = self._detect_class_patterns(node)

                    for pattern in detected:

                        patterns.append(
                            {
                                "pattern": pattern,
                                "class": node.name,
                                "file": file.relative_to(project_folder).as_posix(),
                                "line": node.lineno,
                            }
                        )

        return patterns

    # ====================================================

    def _detect_class_patterns(self, node):

        found = []

        method_names = []

        assignments = []

        bases = []

        for base in node.bases:

            if isinstance(base, ast.Name):

                bases.append(base.id)

            elif isinstance(base, ast.Attribute):

                bases.append(base.attr)

        for item in node.body:

            if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):

                method_names.append(item.name)

            elif isinstance(item, ast.Assign):

                assignments.extend(item.targets)

        # ---------------------------------------------
        # Singleton
        # ---------------------------------------------

        if "_instance" in [
            getattr(a, "id", "")
            for a in assignments
            if isinstance(a, ast.Name)
        ]:

            found.append("Singleton")

        if "get_instance" in method_names:

            found.append("Singleton")

        # ---------------------------------------------
        # Factory
        # ---------------------------------------------

        if any(

            m.startswith("create")

            or m.startswith("build")

            or m.startswith("make")

            for m in method_names

        ):

            found.append("Factory")

        # ---------------------------------------------
        # Builder
        # ---------------------------------------------

        builder_words = [

            "set",

            "add",

            "append",

            "with",

            "build",

        ]

        builder_count = 0

        for m in method_names:

            if any(

                m.startswith(word)

                for word in builder_words

            ):

                builder_count += 1

        if builder_count >= 3:

            found.append("Builder")

        # ---------------------------------------------
        # Strategy
        # ---------------------------------------------

        if "__call__" in method_names:

            found.append("Strategy")

        # ---------------------------------------------
        # Observer
        # ---------------------------------------------

        observer_methods = {

            "attach",

            "detach",

            "notify",

            "update",

        }

        if observer_methods.intersection(method_names):

            found.append("Observer")

        # ---------------------------------------------
        # Decorator
        # ---------------------------------------------

        if "__getattr__" in method_names:

            found.append("Decorator")

        # ---------------------------------------------
        # Adapter
        # ---------------------------------------------

        if len(bases) >= 1 and "__init__" in method_names:

            found.append("Adapter")

        # ---------------------------------------------
        # Facade
        # ---------------------------------------------

        if len(method_names) > 10:

            found.append("Facade")

        return list(set(found))

    # ====================================================

    def summary(self, patterns):

        counts = {}

        for item in patterns:

            counts[item["pattern"]] = (

                counts.get(item["pattern"], 0)

                + 1

            )

        return counts

    # ====================================================

    def detected_classes(self, patterns):

        return sorted(

            {

                item["class"]

                for item in patterns

            }

        )