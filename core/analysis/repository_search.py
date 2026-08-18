from pathlib import Path
import re
import time


class RepositorySearch:
    """
    Repository-wide source code search engine.

    Searches only supported source-code files and ignores
    virtual environments, caches, build folders and IDE folders.
    """

    IGNORE = {
        ".git",
        ".venv",
        "__pycache__",
        "node_modules",
        ".idea",
        ".vscode",
        "env",
        "venv",
        "dist",
        "build",
    }

    DEFAULT_EXTENSIONS = {
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

    def __init__(self):
        self.last_search_time = 0

    # ==========================================================
    # SEARCH
    # ==========================================================

    def search(
        self,
        project_folder,
        keyword,
        extensions=None,
        case_sensitive=False,
        regex=False,
        whole_word=False,
    ):
        project_folder = Path(project_folder)

        if not project_folder.exists():
            return []

        if not project_folder.is_dir():
            return []

        if not keyword or not keyword.strip():
            return []

        keyword = keyword.strip()

        if extensions is None:
            extensions = self.DEFAULT_EXTENSIONS

        # Normalize extensions
        extensions = {
            ext.lower() if ext.startswith(".") else f".{ext.lower()}"
            for ext in extensions
        }

        results = []

        start = time.perf_counter()

        # ======================================================
        # BUILD SEARCH PATTERN
        # ======================================================

        pattern = None

        if regex:

            flags = (
                0
                if case_sensitive
                else re.IGNORECASE
            )

            try:
                pattern = re.compile(
                    keyword,
                    flags,
                )
            except re.error:
                self.last_search_time = round(
                    time.perf_counter() - start,
                    4,
                )
                return []

        elif whole_word:

            flags = (
                0
                if case_sensitive
                else re.IGNORECASE
            )

            pattern = re.compile(
                rf"\b{re.escape(keyword)}\b",
                flags,
            )

        else:

            if not case_sensitive:
                keyword = keyword.lower()

        # ======================================================
        # SEARCH FILES
        # ======================================================

        for file in project_folder.rglob("*"):

            # Ignore directories such as .git, __pycache__, etc.
            if any(
                part in self.IGNORE
                for part in file.parts
            ):
                continue

            if not file.is_file():
                continue

            if file.suffix.lower() not in extensions:
                continue

            try:
                lines = file.read_text(
                    encoding="utf-8",
                    errors="ignore",
                ).splitlines()

            except (
                OSError,
                UnicodeError,
            ):
                continue

            # ==================================================
            # SEARCH EACH LINE
            # ==================================================

            for lineno, line in enumerate(
                lines,
                start=1,
            ):

                if pattern:

                    matched = bool(
                        pattern.search(line)
                    )

                elif case_sensitive:

                    matched = keyword in line

                else:

                    matched = (
                        keyword in line.lower()
                    )

                if not matched:
                    continue

                try:

                    relative_path = (
                        file.relative_to(
                            project_folder
                        )
                        .as_posix()
                    )

                except ValueError:

                    relative_path = file.as_posix()

                results.append(
                    {
                        "file": relative_path,
                        "line": lineno,
                        "content": line.strip(),
                        "preview": line.strip()[:150],
                    }
                )

        # ======================================================
        # SORT RESULTS
        # ======================================================

        results.sort(
            key=lambda item: (
                item["file"].lower(),
                item["line"],
            )
        )

        self.last_search_time = round(
            time.perf_counter() - start,
            4,
        )

        return results

    # ==========================================================
    # STATISTICS
    # ==========================================================

    def statistics(self, results):

        unique_files = {
            result["file"]
            for result in results
        }

        return {
            "matches": len(results),
            "files": len(unique_files),
            "search_time": getattr(
                self,
                "last_search_time",
                0,
            ),
        }

    # ==========================================================
    # TOP FILES
    # ==========================================================

    def top_files(
        self,
        results,
        limit=10,
    ):

        counts = {}

        for result in results:

            file = result["file"]

            counts[file] = (
                counts.get(file, 0) + 1
            )

        return sorted(
            counts.items(),
            key=lambda item: item[1],
            reverse=True,
        )[:limit]

    # ==========================================================
    # EXPORT MARKDOWN
    # ==========================================================

    def export_markdown(self, results):

        md = "# Repository Search Results\n\n"

        if not results:

            md += "No matches found."

            return md

        for item in results:

            md += (
                f"## {item['file']}\n"
                f"- Line: {item['line']}\n"
                f"- Code: `{item['content']}`\n\n"
            )

        return md


# ==========================================================
# BACKWARD COMPATIBILITY
# ==========================================================

RepositorySearchEngine = RepositorySearch