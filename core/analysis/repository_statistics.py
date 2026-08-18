from pathlib import Path
from collections import Counter


class RepositoryStatistics:

    SUPPORTED = {
        ".py",
        ".java",
        ".cpp",
        ".c",
        ".js",
        ".ts",
        ".jsx",
        ".tsx",
        ".go",
        ".php",
        ".rb",
        ".cs",
        ".kt",
        ".swift",
    }

    IGNORE = {
        ".git",
        ".venv",
        "__pycache__",
        "node_modules",
        ".idea",
        ".vscode",
        "env",
        "venv",
        "build",
        "dist",
    }

    def analyze(self, project_folder):

        project_folder = Path(project_folder)

        stats = {

            "files": 0,

            "lines": 0,

            "blank_lines": 0,

            "comment_lines": 0,

            "code_lines": 0,

            "largest_file": "",

            "largest_file_lines": 0,

            "smallest_file": "",

            "smallest_file_lines": 999999,

        }

        languages = Counter()

        extensions = Counter()

        file_sizes = []

        for file in project_folder.rglob("*"):

            if any(
                part in self.IGNORE
                for part in file.parts
            ):
                continue

            if (
                not file.is_file()
                or file.suffix.lower()
                not in self.SUPPORTED
            ):
                continue

            try:

                text = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

            except Exception:

                continue

            lines = text.splitlines()

            total = len(lines)

            stats["files"] += 1
            stats["lines"] += total

            ext = file.suffix.lower()

            extensions[ext] += 1

            languages[self.language(ext)] += 1

            if total > stats["largest_file_lines"]:

                stats["largest_file"] = file.name

                stats["largest_file_lines"] = total

            if total < stats["smallest_file_lines"]:

                stats["smallest_file"] = file.name

                stats["smallest_file_lines"] = total

            file_sizes.append(

                {

                    "file": file.relative_to(
                        project_folder
                    ).as_posix(),

                    "lines": total,

                }

            )

            for line in lines:

                stripped = line.strip()

                if not stripped:

                    stats["blank_lines"] += 1

                elif stripped.startswith(

                    (
                        "#",
                        "//",
                        "/*",
                        "*",
                    )

                ):

                    stats["comment_lines"] += 1

                else:

                    stats["code_lines"] += 1

        file_sizes.sort(

            key=lambda x: x["lines"],

            reverse=True,

        )

        stats["average_file_size"] = round(

            stats["lines"] /

            max(stats["files"], 1),

            2,

        )

        return {

            "statistics": stats,

            "languages": languages,

            "extensions": extensions,

            "largest_files": file_sizes[:10],

        }

    def language(self, extension):

        mapping = {

            ".py": "Python",

            ".java": "Java",

            ".cpp": "C++",

            ".c": "C",

            ".js": "JavaScript",

            ".ts": "TypeScript",

            ".jsx": "React",

            ".tsx": "React TS",

            ".go": "Go",

            ".php": "PHP",

            ".rb": "Ruby",

            ".cs": "C#",

            ".kt": "Kotlin",

            ".swift": "Swift",

        }

        return mapping.get(

            extension,

            extension,

        )