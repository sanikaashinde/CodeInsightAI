from pathlib import Path

EXTENSION_MAP = {
    ".py": "Python",
    ".java": "Java",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".cpp": "C++",
    ".c": "C",
    ".cs": "C#",
    ".go": "Go",
    ".rb": "Ruby",
    ".php": "PHP",
    ".swift": "Swift",
    ".kt": "Kotlin",
    ".rs": "Rust",
    ".scala": "Scala",
    ".html": "HTML",
    ".css": "CSS",
    ".sql": "SQL",
    ".json": "JSON",
    ".xml": "XML",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".md": "Markdown",
    ".sh": "Shell",
}


def detect_language(file_path: str) -> str:
    """
    Detect programming language from file extension.
    """

    suffix = Path(file_path).suffix.lower()

    return EXTENSION_MAP.get(suffix, "Unknown")