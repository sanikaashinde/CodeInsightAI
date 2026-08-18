import math


class ProjectMetrics:

    """
    Calculates project-wide engineering metrics.
    """

    def analyze(self, analyses, complexities):

        total_files = len(analyses)

        total_lines = 0
        total_functions = 0
        total_classes = 0
        total_imports = 0

        documented = 0

        async_functions = 0

        for analysis in analyses:

            total_lines += analysis.total_lines
            total_functions += len(analysis.functions)
            total_classes += len(analysis.classes)
            total_imports += len(analysis.imports)

            for func in analysis.functions:

                if func.docstring:
                    documented += 1

                if func.is_async:
                    async_functions += 1

        documentation = 100

        if total_functions:

            documentation = round(

                documented / total_functions * 100,

                2,

            )

        average_complexity = 0

        complexity_values = []

        for result in complexities:

            complexity_values.extend(

                f["complexity"]

                for f in result["functions"]

            )

        if complexity_values:

            average_complexity = round(

                sum(complexity_values)

                / len(complexity_values),

                2,

            )

        density = 0

        if total_lines:

            density = round(

                total_functions

                / total_lines

                * 100,

                2,

            )

        maintainability = max(

            0,

            round(

                100

                - average_complexity * 3

                + documentation * 0.15,

                2,

            ),

        )

        architecture = round(

            min(

                100,

                60
                + total_classes
                + math.log(total_imports + 1) * 8,

            ),

            2,

        )

        return {

            "files": total_files,

            "lines": total_lines,

            "functions": total_functions,

            "classes": total_classes,

            "imports": total_imports,

            "documentation": documentation,

            "async": async_functions,

            "average_complexity": average_complexity,

            "code_density": density,

            "maintainability": maintainability,

            "architecture": architecture,

        }
    
def project_metrics(analyses, complexities):
    """
    Backward-compatible wrapper.
    """
    return ProjectMetrics().analyze(
        analyses,
        complexities,
    )