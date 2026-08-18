from pathlib import Path
from radon.complexity import cc_visit, cc_rank

class ComplexityAnalyzer:
    """Cyclomatic Complexity Analyzer."""

    def analyze(self, source):
        try:
            if isinstance(source, Path):
                code = source.read_text(encoding="utf-8", errors="ignore")
            elif isinstance(source, str):
                possible_path = Path(source)
                if possible_path.exists() and possible_path.is_file():
                    code = possible_path.read_text(
                        encoding="utf-8",
                        errors="ignore"
                    )
                else:
                    code = source
            else:
                code = str(source)

            results = cc_visit(code)

        except Exception as e:
            return {
                "average_complexity": 0,
                "highest_complexity": 0,
                "total_functions": 0,
                "functions": [],
                "error": str(e),
            }

        functions = []

        for item in results:
            # Exclude class-level complexity.
            # Keep Function and Method objects.
            if item.__class__.__name__ == "Class":
                continue

            complexity = int(item.complexity)

            functions.append({
                "name": item.name,
                "complexity": complexity,
                "rank": cc_rank(complexity),
                "lineno": getattr(item, "lineno", 0),
                "line": getattr(item, "lineno", 0),
                "endline": getattr(item, "endline", 0),
                "end_line": getattr(item, "endline", 0),
            })

        functions.sort(
            key=lambda x: x["complexity"],
            reverse=True
        )

        total = sum(
            item["complexity"]
            for item in functions
        )

        highest = max(
            (item["complexity"] for item in functions),
            default=0
        )

        average = round(
            total / len(functions),
            2
        ) if functions else 0

        return {
            "average_complexity": average,
            "highest_complexity": highest,
            "total_functions": len(functions),
            "functions": functions,
        }


def analyze_complexity(source):
    """Backward-compatible helper."""
    return ComplexityAnalyzer().analyze(source)
