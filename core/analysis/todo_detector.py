from pathlib import Path
import re


class TodoDetector:
    """
    Detects:

    TODO
    FIXME
    BUG
    HACK
    NOTE
    XXX
    OPTIMIZE
    """

    PATTERNS = [
        "TODO",
        "FIXME",
        "BUG",
        "HACK",
        "NOTE",
        "XXX",
        "OPTIMIZE",
    ]

    def analyze(self, project_folder):

        project_folder = Path(project_folder)

        results = []

        for file in project_folder.rglob("*"):

            if not file.is_file():
                continue

            if file.suffix.lower() not in {
                ".py",
                ".java",
                ".cpp",
                ".c",
                ".js",
                ".ts",
                ".tsx",
                ".jsx",
                ".go",
                ".php",
                ".cs",
                ".kt",
                ".swift",
            }:
                continue

            try:

                lines = file.read_text(
                    encoding="utf-8",
                    errors="ignore",
                ).splitlines()

            except Exception:

                continue

            for line_number, line in enumerate(
                lines,
                start=1,
            ):

                for keyword in self.PATTERNS:

                    if keyword in line.upper():

                        results.append(

                            {

                                "file": file.relative_to(
                                    project_folder
                                ).as_posix(),

                                "line": line_number,

                                "type": keyword,

                                "text": line.strip(),

                            }

                        )

        return results

    # ===================================

    def summary(self, results):

        summary = {

            "total": len(results)

        }

        for keyword in self.PATTERNS:

            summary[keyword] = sum(

                1

                for item in results

                if item["type"] == keyword

            )

        return summary

    # ===================================

    def search(self, results, keyword):

        keyword = keyword.upper()

        return [

            item

            for item in results

            if item["type"] == keyword

        ]
    
# ==========================================================
# Backward Compatibility
# ==========================================================

def scan(self, project_folder):
    """
    Backward-compatible alias for older dashboard code.
    """
    return self.analyze(project_folder)


# Attach scan() to the class
TodoDetector.scan = scan


class TodoScanner(TodoDetector):
    """
    Backward-compatible alias.
    """
    pass