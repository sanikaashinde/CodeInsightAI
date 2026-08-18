from collections import Counter


class ProjectSummary:

    def summarize(self, analyses):

        total_functions = 0
        total_classes = 0
        total_variables = 0
        total_imports = 0
        total_lines = 0

        total_docstrings = 0
        total_async = 0

        imports = Counter()
        languages = Counter()

        for analysis in analyses:

            total_functions += len(analysis.functions)
            total_classes += len(analysis.classes)
            total_variables += len(analysis.variables)
            total_imports += len(analysis.imports)
            total_lines += analysis.total_lines

            languages[analysis.language] += 1

            for lib in analysis.imports:
                imports[lib] += 1

            for func in analysis.functions:

                if func.docstring:
                    total_docstrings += 1

                if func.is_async:
                    total_async += 1

        documentation = 100

        if total_functions:

            documentation = round(
                total_docstrings / total_functions * 100,
                2
            )

        return {

            # -------------------------
            # Main Metrics
            # -------------------------

            "functions": total_functions,

            "classes": total_classes,

            "variables": total_variables,

            "imports": total_imports,

            "lines": total_lines,

            # -------------------------
            # Documentation
            # -------------------------

            "docstrings": total_docstrings,

            "documentation_percent": documentation,

            "async_functions": total_async,

            # -------------------------
            # Statistics
            # -------------------------

            "top_imports": imports.most_common(15),

            "languages": dict(languages),

            # -------------------------
            # Totals
            # -------------------------

            "files": len(analyses)
        }