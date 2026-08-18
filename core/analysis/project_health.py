from collections import Counter


class ProjectHealth:
    """
    Calculates overall project health statistics.
    """

    def analyze(self, analyses):

        stats = {
            # Basic Metrics
            "files": len(analyses),
            "functions": 0,
            "classes": 0,
            "variables": 0,
            "imports": 0,
            "lines": 0,

            # Documentation
            "docstrings": 0,
            "documentation_percent": 0,

            # Quality
            "large_functions": 0,
            "async_functions": 0,
            "syntax_errors": 0,

            # Comments / TODO
            "todo": 0,
            "fixme": 0,
            "blank_lines": 0,
            "comment_lines": 0,
        }

        libraries = Counter()

        for analysis in analyses:

            stats["functions"] += len(getattr(analysis, "functions", []))
            stats["classes"] += len(getattr(analysis, "classes", []))
            stats["variables"] += len(getattr(analysis, "variables", []))
            stats["imports"] += len(getattr(analysis, "imports", []))
            stats["lines"] += getattr(analysis, "total_lines", 0)

            stats["blank_lines"] += getattr(
                analysis,
                "blank_lines",
                0,
            )

            stats["comment_lines"] += getattr(
                analysis,
                "comment_lines",
                0,
            )

            stats["todo"] += getattr(
                analysis,
                "todo_count",
                0,
            )

            stats["fixme"] += getattr(
                analysis,
                "fixme_count",
                0,
            )

            if getattr(
                analysis,
                "syntax_error",
                False,
            ):
                stats["syntax_errors"] += 1

            for lib in getattr(analysis, "imports", []):

                try:
                    libraries[lib] += 1
                except Exception:
                    pass

            for func in getattr(analysis, "functions", []):

                if getattr(func, "docstring", None):
                    stats["docstrings"] += 1

                if getattr(func, "is_async", False):
                    stats["async_functions"] += 1

                if getattr(func, "length", 0) > 60:
                    stats["large_functions"] += 1

        if stats["functions"]:

            stats["documentation_percent"] = round(
                (stats["docstrings"] / stats["functions"]) * 100,
                2,
            )

        else:

            stats["documentation_percent"] = 100

        return stats, libraries.most_common(20)