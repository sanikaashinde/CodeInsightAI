from pathlib import Path
from difflib import SequenceMatcher
from collections import Counter
import hashlib
import time


class DuplicateCodeDetector:

    SUPPORTED = {
        ".py",
        ".js",
        ".ts",
        ".java",
        ".cpp",
        ".c",
        ".go",
        ".php",
        ".cs",
        ".kt",
    }

    IGNORE = {
        ".git",
        ".venv",
        "__pycache__",
        "node_modules",
        "env",
        "venv",
    }

    # =====================================================
    # CLEAN CODE
    # =====================================================

    def _clean(self, text):

        cleaned = []

        for line in text.splitlines():

            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            cleaned.append(line)

        return "\n".join(cleaned)

    # =====================================================
    # HASH
    # =====================================================

    def _hash(self, text):

        return hashlib.md5(
            text.encode("utf-8")
        ).hexdigest()

    # =====================================================
    # ANALYZE
    # =====================================================

    def analyze(

        self,

        project_folder,

        similarity_threshold=0.85,

        min_lines=5,

    ):

        start = time.time()

        project_folder = Path(project_folder)

        files = []

        duplicates = []

        # -----------------------------------------

        # Read Files

        # -----------------------------------------

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

                source = file.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )

                cleaned = self._clean(source)

                line_count = len(
                    cleaned.splitlines()
                )

                if line_count < min_lines:
                    continue

                files.append(

                    {

                        "path": file.relative_to(
                            project_folder
                        ).as_posix(),

                        "content": cleaned,

                        "lines": line_count,

                        "hash": self._hash(cleaned),

                    }

                )

            except Exception:

                continue

        # -----------------------------------------

        # Compare Files

        # -----------------------------------------

        checked = set()

        for i in range(len(files)):

            for j in range(i + 1, len(files)):

                pair = (
                    files[i]["hash"],
                    files[j]["hash"],
                )

                if pair in checked:
                    continue

                checked.add(pair)

                similarity = SequenceMatcher(

                    None,

                    files[i]["content"],

                    files[j]["content"],

                ).ratio()

                if similarity >= similarity_threshold:

                    duplicates.append(

                        {

                            "file_1": files[i]["path"],

                            "file_2": files[j]["path"],

                            "similarity": round(
                                similarity * 100,
                                2,
                            ),

                            "lines_1": files[i]["lines"],

                            "lines_2": files[j]["lines"],

                        }

                    )

        duplicates.sort(

            key=lambda x: x["similarity"],

            reverse=True,

        )

        elapsed = round(

            time.time() - start,

            2,

        )

        return {

            "duplicates": duplicates,

            "summary": self.summary(
                duplicates
            ),

            "execution_time": elapsed,

        }

    # =====================================================
    # SUMMARY
    # =====================================================

    def summary(self, duplicates):

        # Accept full analyze() result
        if isinstance(duplicates, dict):

            if "duplicates" in duplicates:
                duplicates = duplicates["duplicates"]

        if not duplicates:

            return {
                "duplicate_pairs": 0,
                "highest_similarity": 0,
                "average_similarity": 0,
                "affected_files": 0,
            }

        similarities = [
            d["similarity"]
            for d in duplicates
        ]

        files = Counter()

        for d in duplicates:

            files[d["file_1"]] += 1
            files[d["file_2"]] += 1

        return {

            "duplicate_pairs": len(duplicates),

            "highest_similarity": max(similarities),

            "average_similarity": round(
                sum(similarities) / len(similarities),
                2,
            ),

            "affected_files": len(files),

        }

    # =====================================================
    # MARKDOWN REPORT
    # =====================================================

    def export_markdown(

        self,

        result,

    ):

        summary = result["summary"]

        duplicates = result["duplicates"]

        md = "# Duplicate Code Report\n\n"

        md += f"Duplicate Pairs: {summary['duplicate_pairs']}\n\n"
        md += f"Highest Similarity: {summary['highest_similarity']}%\n\n"
        md += f"Average Similarity: {summary['average_similarity']}%\n\n"
        md += f"Affected Files: {summary['affected_files']}\n\n"

        md += "---\n\n"

        for item in duplicates:

            md += f"## {item['file_1']}\n"
            md += f"Matches: {item['file_2']}\n"
            md += f"Similarity: {item['similarity']}%\n\n"

        return md