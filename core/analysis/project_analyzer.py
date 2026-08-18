from pathlib import Path


class ProjectAnalyzer:

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
        ".pytest_cache",
        ".mypy_cache",
    }

    def scan(self, root: Path):

        files = []
        all_files = []

        total_lines = 0
        total_size = 0

        language_count = {}
        extension_count = {}

        for path in root.rglob("*"):

            if any(part in self.IGNORE for part in path.parts):
                continue

            if not path.is_file():
                continue

            # Count EVERY project file
            all_files.append(path)

            suffix = path.suffix.lower()

            # Only source files are sent to AST/static analysis
            if suffix not in self.SUPPORTED:
                continue

            files.append(path)

            try:
                text = path.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                total_lines += len(text.splitlines())

            except Exception:
                pass

            try:
                total_size += path.stat().st_size

            except Exception:
                pass

            language = self.detect_language(suffix)

            language_count[language] = (
                language_count.get(language, 0) + 1
            )

            extension_count[suffix] = (
                extension_count.get(suffix, 0) + 1
            )

        return {
            # ALL files in uploaded project
            "files": all_files,
            "file_count": len(all_files),

            # Source files supported by analyzer
            "source_files": files,
            "source_file_count": len(files),

            "total_lines": total_lines,
            "total_size": total_size,

            "languages": language_count,
            "extensions": extension_count,
        }

    # =====================================================
    # Language Detector
    # =====================================================

    def detect_language(self, extension):

        mapping = {
            ".py": "Python",
            ".java": "Java",
            ".js": "JavaScript",
            ".ts": "TypeScript",
            ".jsx": "React",
            ".tsx": "React TS",
            ".cpp": "C++",
            ".c": "C",
            ".cs": "C#",
            ".go": "Go",
            ".rb": "Ruby",
            ".php": "PHP",
            ".swift": "Swift",
            ".kt": "Kotlin",
        }

        return mapping.get(extension, "Unknown")
