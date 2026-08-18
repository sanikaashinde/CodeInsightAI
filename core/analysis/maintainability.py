from statistics import mean


class MaintainabilityAnalyzer:
    """
    Calculates project maintainability metrics.
    """

    def analyze(self, analyses, complexity_results):

        total_lines = 0
        total_functions = 0
        total_classes = 0
        documented_functions = 0

        function_lengths = []
        complexities = []

        for analysis in analyses:

            total_lines += analysis.total_lines
            total_classes += len(analysis.classes)

            for func in analysis.functions:

                total_functions += 1

                if func.docstring:
                    documented_functions += 1

                # Uses end_line if available
                if hasattr(func, "end_line") and func.end_line:

                    function_lengths.append(
                        func.end_line - func.line_number + 1
                    )

        for result in complexity_results:

            complexities.extend(
                f["complexity"]
                for f in result["functions"]
            )

        avg_complexity = (
            round(mean(complexities), 2)
            if complexities else 0
        )

        avg_function_length = (
            round(mean(function_lengths), 2)
            if function_lengths else 0
        )

        documentation = (
            round(
                documented_functions /
                max(total_functions, 1) * 100,
                2
            )
        )

        # ----------------------------------------
        # Maintainability Formula
        # ----------------------------------------

        score = 100

        score -= avg_complexity * 2

        score -= avg_function_length * 0.3

        score += documentation * 0.15

        score = max(0, min(100, round(score, 2)))

        if score >= 85:

            level = "Excellent"

        elif score >= 70:

            level = "Good"

        elif score >= 50:

            level = "Average"

        else:

            level = "Poor"

        return {

            "score": score,

            "level": level,

            "average_complexity": avg_complexity,

            "average_function_length": avg_function_length,

            "documentation": documentation,

            "total_functions": total_functions,

            "total_classes": total_classes,

            "total_lines": total_lines,

        }
    
def maintainability_score(analyses, complexity_results):
    """
    Backward-compatible wrapper.
    """
    return MaintainabilityAnalyzer().analyze(
        analyses,
        complexity_results,
    )