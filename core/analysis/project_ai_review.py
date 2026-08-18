class AIProjectReview:
    """
    Metric-based project review engine.

    Produces a deterministic review from the parsed project analyses.
    No external AI service is required.
    """

    def review(self, project_name, analyses):

        total_files = len(analyses)

        total_functions = sum(
            len(getattr(a, "functions", []))
            for a in analyses
        )

        total_classes = sum(
            len(getattr(a, "classes", []))
            for a in analyses
        )

        total_lines = sum(
            getattr(a, "total_lines", 0)
            for a in analyses
        )

        total_docstrings = sum(
            1
            for a in analyses
            for f in getattr(a, "functions", [])
            if getattr(f, "docstring", None)
        )

        total_async = sum(
            1
            for a in analyses
            for f in getattr(a, "functions", [])
            if getattr(f, "is_async", False)
        )

        total_todo = sum(
            getattr(a, "todo_count", 0)
            for a in analyses
        )

        total_fixme = sum(
            getattr(a, "fixme_count", 0)
            for a in analyses
        )

        syntax_errors = sum(
            1
            for a in analyses
            if getattr(a, "syntax_error", False)
        )

        large_functions = sum(
            1
            for a in analyses
            for f in getattr(a, "functions", [])
            if getattr(f, "length", 0) > 60
        )

        # --------------------------------------------------
        # Documentation
        # --------------------------------------------------

        if total_functions:
            documentation = round(
                (total_docstrings / total_functions) * 100,
                1
            )
        else:
            documentation = 100.0

        # --------------------------------------------------
        # Complexity
        # --------------------------------------------------

        complexity_values = [
            getattr(f, "complexity", 0)
            for a in analyses
            for f in getattr(a, "functions", [])
            if getattr(f, "complexity", 0) > 0
        ]

        if complexity_values:
            average_complexity = round(
                sum(complexity_values) / len(complexity_values),
                2
            )
            highest_complexity = max(complexity_values)
        else:
            average_complexity = 0.0
            highest_complexity = 0

        if average_complexity <= 5:
            complexity_score = 100
        elif average_complexity <= 10:
            complexity_score = 85
        elif average_complexity <= 15:
            complexity_score = 70
        else:
            complexity_score = 50

        # --------------------------------------------------
        # Maintainability
        # --------------------------------------------------

        maintainability = 100.0

        maintainability -= min(
            large_functions * 5,
            25
        )

        maintainability -= min(
            total_todo * 2,
            10
        )

        maintainability -= min(
            total_fixme * 3,
            15
        )

        maintainability -= min(
            syntax_errors * 20,
            40
        )

        maintainability = round(
            max(0, min(100, maintainability)),
            1
        )

        # --------------------------------------------------
        # Architecture
        # --------------------------------------------------

        architecture = 60.0

        if total_classes >= 1:
            architecture += 10

        if total_classes >= 3:
            architecture += 10

        if total_classes >= 5:
            architecture += 10

        if total_functions >= 5:
            architecture += 10

        architecture = round(
            min(100, architecture),
            1
        )

        # --------------------------------------------------
        # Readability
        # --------------------------------------------------

        readability = (
            documentation * 0.40
            + complexity_score * 0.35
            + maintainability * 0.25
        )

        readability = round(
            max(0, min(100, readability)),
            1
        )

        # --------------------------------------------------
        # Security
        #
        # Security analysis is handled separately by the
        # dashboard. Keep this review neutral rather than
        # inventing security findings.
        # --------------------------------------------------

        security = 100.0

        if syntax_errors:
            security -= min(
                syntax_errors * 10,
                30
            )

        security = round(
            max(0, min(100, security)),
            1
        )

        # --------------------------------------------------
        # Overall Score
        # --------------------------------------------------

        score = round(
            documentation * 0.20
            + readability * 0.20
            + maintainability * 0.20
            + architecture * 0.15
            + complexity_score * 0.15
            + security * 0.10,
            1
        )

        # --------------------------------------------------
        # Strengths
        # --------------------------------------------------

        strengths = []

        if documentation >= 80:
            strengths.append(
                "Strong documentation coverage."
            )

        if complexity_score >= 85:
            strengths.append(
                "Low overall code complexity."
            )

        if maintainability >= 85:
            strengths.append(
                "Good maintainability with limited technical debt indicators."
            )

        if architecture >= 80:
            strengths.append(
                "Good project structure and modular architecture."
            )

        if syntax_errors == 0:
            strengths.append(
                "No Python syntax errors detected."
            )

        if large_functions == 0:
            strengths.append(
                "No large functions detected."
            )

        if not strengths:
            strengths.append(
                "Core project structure and source code were analyzed successfully."
            )

        # --------------------------------------------------
        # Improvements
        # --------------------------------------------------

        improvements = []

        if documentation < 80:
            improvements.append(
                f"Increase function documentation coverage from {documentation}%."
            )

        if average_complexity > 10:
            improvements.append(
                f"Reduce average cyclomatic complexity ({average_complexity})."
            )

        if large_functions > 0:
            improvements.append(
                f"Refactor {large_functions} large function(s)."
            )

        if total_classes < 3 and total_functions >= 5:
            improvements.append(
                "Consider further modularization where appropriate."
            )

        if total_todo > 0:
            improvements.append(
                f"Resolve {total_todo} TODO item(s)."
            )

        if total_fixme > 0:
            improvements.append(
                f"Resolve {total_fixme} FIXME item(s)."
            )

        if syntax_errors > 0:
            improvements.append(
                f"Fix {syntax_errors} syntax error(s)."
            )

        if not improvements:
            improvements.append(
                "Only minor improvements remain."
            )

        # --------------------------------------------------
        # Recommendation
        # --------------------------------------------------

        if score >= 90:
            recommendation = "Production Ready"
        elif score >= 80:
            recommendation = "Strong Internship / Resume Project"
        elif score >= 70:
            recommendation = "Good Internship Project"
        elif score >= 60:
            recommendation = "Good Student Project"
        else:
            recommendation = "Needs Improvement"

        # --------------------------------------------------
        # Report
        # --------------------------------------------------

        report = f"""
# AI Project Review

## Project

**{project_name}**

---

## Overall Score

**{score}/100**

---

## Statistics

- Files : {total_files}
- Lines : {total_lines}
- Functions : {total_functions}
- Classes : {total_classes}
- Documentation : {documentation}%
- Async Functions : {total_async}
- Average Complexity : {average_complexity}
- Highest Complexity : {highest_complexity}
- Large Functions : {large_functions}
- Syntax Errors : {syntax_errors}
- TODO : {total_todo}
- FIXME : {total_fixme}

---

## Quality Breakdown

| Metric | Score |
|---|---:|
| Documentation | {documentation}% |
| Readability | {readability}% |
| Maintainability | {maintainability}% |
| Architecture | {architecture}% |
| Complexity Health | {complexity_score}% |
| Security Baseline | {security}% |

---

## Strengths

"""

        for strength in strengths:
            report += f"- {strength}\n"

        report += """
---

## Improvements

"""

        for improvement in improvements:
            report += f"- {improvement}\n"

        report += f"""
---

## Recommendation

**{recommendation}**

This review was generated by CodeInsight AI's
metric-based local analysis engine.

No external AI service was used.
"""

        return report
