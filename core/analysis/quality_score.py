class ProjectQualityScore:

    def calculate(self, analyses):

        total_functions = 0
        documented_functions = 0

        large_functions = 0
        async_functions = 0
        syntax_errors = 0
        todo_count = 0
        complexity_score = 100

        for analysis in analyses:

            if getattr(analysis, "syntax_error", False):
                syntax_errors += 1

            todo_count += getattr(
                analysis,
                "todo_count",
                0
            )

            for func in analysis.functions:

                total_functions += 1

                if func.docstring:
                    documented_functions += 1

                if func.is_async:
                    async_functions += 1

                if getattr(func, "length", 0) > 60:
                    large_functions += 1

                complexity = getattr(
                    func,
                    "complexity",
                    1
                )

                if complexity > 10:
                    complexity_score -= 2

        # -----------------------------------
        # Documentation
        # -----------------------------------

        if total_functions:

            documentation = round(

                documented_functions
                / total_functions
                * 100,

                2

            )

        else:

            documentation = 100

        # -----------------------------------
        # Maintainability
        # -----------------------------------

        maintainability = 100

        maintainability -= large_functions * 3

        maintainability -= syntax_errors * 10

        maintainability -= todo_count

        maintainability = max(
            0,
            maintainability
        )

        # -----------------------------------
        # Readability
        # -----------------------------------

        readability = documentation

        if total_functions > 100:
            readability -= 5

        readability = max(
            0,
            readability
        )

        # -----------------------------------
        # Architecture
        # -----------------------------------

        architecture = 100

        total_classes = sum(
            len(a.classes)
            for a in analyses
        )

        if total_classes < 3:
            architecture -= 10

        if total_functions < 10:
            architecture -= 10

        architecture = max(
            0,
            architecture
        )

        # -----------------------------------
        # Complexity
        # -----------------------------------

        complexity_score = max(
            0,
            complexity_score
        )

        # -----------------------------------
        # Overall Score
        # -----------------------------------

        overall = round(

            (

                documentation

                + maintainability

                + readability

                + architecture

                + complexity_score

            )

            / 5,

            2

        )

        return {

            "overall": overall,

            "documentation": documentation,

            "maintainability": maintainability,

            "readability": readability,

            "architecture": architecture,

            "complexity": complexity_score,

            "syntax_errors": syntax_errors,

            "async_functions": async_functions,

            "large_functions": large_functions,

            "documented_functions": documented_functions,

            "total_functions": total_functions,
        }