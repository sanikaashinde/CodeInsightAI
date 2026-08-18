from pathlib import Path

from .language_detector import detect_language


IGNORE_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    ".idea",
    ".vscode",
    "dist",
    "build",
    "env",
}

SUPPORTED = {
    ".py",
    ".java",
    ".js",
    ".ts",
    ".cpp",
    ".c",
    ".go",
    ".rb",
    ".php",
    ".cs",
    ".kt",
    ".swift",
    ".rs",
}


def load_project(project_path: str):

    project = Path(project_path)

    files = []

    for file in project.rglob("*"):

        if not file.is_file():
            continue

        if any(part in IGNORE_DIRS for part in file.parts):
            continue

        if file.suffix.lower() not in SUPPORTED:
            continue

        try:

            code = file.read_text(
                encoding="utf-8",
                errors="ignore",
            )

            files.append(
                {
                    "filename": file.name,
                    "path": str(file),
                    "language": detect_language(file),
                    "code": code,
                    "lines": len(code.splitlines()),
                    "size": file.stat().st_size,
                }
            )

        except Exception:

            continue

    return files