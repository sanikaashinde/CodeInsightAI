from pathlib import Path
import re

from core.llm.llm_client import GeminiClient
from core.analysis.repository_search import RepositorySearch


class ProjectChat:
    """
    Project-aware chat engine.

    Searches the uploaded project for relevant code before
    sending context to the LLM.
    """

    SUPPORTED_EXTENSIONS = {
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

    STOP_WORDS = {
        "what", "which", "where", "when", "who", "why", "how",
        "is", "are", "was", "were", "the", "a", "an", "and",
        "or", "of", "in", "on", "to", "for", "from", "with",
        "does", "do", "did", "used", "use", "using", "this",
        "that", "project", "file", "files", "code", "tell",
        "me", "about", "explain", "show", "give", "can", "you",
        "contains", "contain", "implemented", "implementation",
    }

    def __init__(self):
        self.client = GeminiClient()
        self.search_engine = RepositorySearch()

    # ======================================================
    # LOAD PROJECT
    # ======================================================

    def load_project(self, project_folder):

        project_folder = Path(project_folder)

        chunks = []

        if not project_folder.exists():
            return chunks

        for file in project_folder.rglob("*"):

            if not file.is_file():
                continue

            if file.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
                continue

            try:
                text = file.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )
            except Exception:
                continue

            try:
                relative_path = (
                    file.relative_to(project_folder)
                    .as_posix()
                )
            except ValueError:
                relative_path = file.name

            chunks.append({
                "file": file.name,
                "path": relative_path,
                "content": text,
            })

        return chunks

    # ======================================================
    # QUESTION KEYWORDS
    # ======================================================

    def _extract_keywords(self, question):

        words = re.findall(
            r"[A-Za-z_][A-Za-z0-9_]*",
            question.lower(),
        )

        keywords = []

        for word in words:

            if word in self.STOP_WORDS:
                continue

            if len(word) < 3:
                continue

            if word not in keywords:
                keywords.append(word)

        # Add useful domain mappings.
        mappings = {
            "machine": ["model", "train", "classifier"],
            "learning": ["model", "train"],
            "churn": ["churn", "prediction"],
            "predict": ["prediction", "model"],
            "prediction": ["predict", "model"],
            "database": ["sqlite", "sqlite3", "database"],
            "customer": ["customer", "customerid"],
            "dashboard": ["streamlit", "st"],
            "security": ["security", "analyze"],
            "model": ["model", "train"],
            "training": ["train", "model"],
            "risk": ["risk"],
            "probability": ["probability"],
            "api": ["fastapi", "endpoint"],
        }

        expanded = list(keywords)

        for keyword in keywords:

            for mapped in mappings.get(keyword, []):

                if mapped not in expanded:
                    expanded.append(mapped)

        return expanded[:15]

    # ======================================================
    # RELEVANT FILE SEARCH
    # ======================================================

    def _find_relevant_files(
        self,
        project_folder,
        question,
        chunks,
    ):

        keywords = self._extract_keywords(question)

        scores = {}

        for chunk in chunks:
            scores[chunk["path"]] = 0

        # --------------------------------------------------
        # Search exact keywords in repository
        # --------------------------------------------------

        for keyword in keywords:

            results = self.search_engine.search(
                project_folder,
                keyword,
                case_sensitive=False,
                regex=False,
                whole_word=False,
            )

            for result in results:

                path = result["file"]

                if path in scores:
                    scores[path] += 1

        # --------------------------------------------------
        # Score file names too
        # --------------------------------------------------

        for chunk in chunks:

            path_lower = chunk["path"].lower()

            for keyword in keywords:

                if keyword.lower() in path_lower:
                    scores[chunk["path"]] += 3

        ranked = sorted(
            scores.items(),
            key=lambda item: item[1],
            reverse=True,
        )

        relevant_paths = [
            path
            for path, score in ranked
            if score > 0
        ]

        return relevant_paths[:8]

    # ======================================================
    # BUILD CONTEXT
    # ======================================================

    def _build_context(
        self,
        chunks,
        relevant_paths,
        max_chars=45000,
    ):

        chunk_map = {
            chunk["path"]: chunk
            for chunk in chunks
        }

        context = ""
        current = 0

        # First add relevant files.
        for path in relevant_paths:

            chunk = chunk_map.get(path)

            if not chunk:
                continue

            part = (
                f"\n\n"
                f"===== FILE: {chunk['path']} =====\n"
                f"{chunk['content']}\n"
                f"===== END FILE =====\n"
            )

            if current + len(part) > max_chars:
                break

            context += part
            current += len(part)

        # If search found nothing, use a limited project overview.
        if not context:

            for chunk in chunks:

                part = (
                    f"\n\n"
                    f"===== FILE: {chunk['path']} =====\n"
                    f"{chunk['content']}\n"
                    f"===== END FILE =====\n"
                )

                if current + len(part) > max_chars:
                    break

                context += part
                current += len(part)

        return context

    # ======================================================
    # ASK
    # ======================================================

    def ask(
        self,
        project_folder,
        question,
    ):

        project_folder = Path(project_folder)

        if not project_folder.exists():
            return "Not found in project."

        chunks = self.load_project(
            project_folder
        )

        if not chunks:
            return "Not found in project."

        relevant_paths = self._find_relevant_files(
            project_folder,
            question,
            chunks,
        )

        context = self._build_context(
            chunks,
            relevant_paths,
        )

        prompt = f"""
You are a Senior Software Architect performing
repository-aware code analysis.

Answer the user's question ONLY using the uploaded
project source code provided below.

IMPORTANT RULES:

1. Do not invent files, functions, libraries, models,
   technologies, or behavior.
2. Base every factual statement on the provided code.
3. Mention exact file names whenever possible.
4. If the answer cannot be determined from the provided
   project code, say exactly:
   "Not found in project."
5. Do not answer using general knowledge when the project
   code does not contain the information.
6. If multiple files are relevant, explain how they are
   connected.

PROJECT FILES:

{context}

USER QUESTION:

{question}

Provide the answer in this format:

### Explanation
Clear answer based on the project code.

### Relevant Files
List the relevant file names and explain their role.

### Suggested Improvements
Give improvements only if they are relevant to the
question and supported by the project context.
"""

        try:
            response = self.client.generate(
                prompt
            )

            if response is None:
                return "Not found in project."

            response = str(response).strip()

            if not response:
                return "Not found in project."

            return response

        except Exception as e:

            return (
                "Project Chat error: "
                f"{type(e).__name__}: {e}"
            )
