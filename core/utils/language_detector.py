from pathlib import Path

LANGUAGES = {
    ".py": "Python",

    ".java": "Java",
    ".js": "JavaScript",
    ".jsx": "React",
    ".ts": "TypeScript",
    ".tsx": "React TS",

    ".cpp": "C++",
    ".cc": "C++",
    ".cxx": "C++",
    ".hpp": "C++",

    ".c": "C",
    ".h": "C/C++",

    ".cs": "C#",
    ".go": "Go",
    ".php": "PHP",
    ".kt": "Kotlin",
    ".swift": "Swift",

    ".rs": "Rust",
    ".rb": "Ruby",
    ".scala": "Scala",
    ".sh": "Shell",
    ".bash": "Shell",
    ".sql": "SQL",

    ".html": "HTML",
    ".htm": "HTML",
    ".css": "CSS",

    ".md": "Markdown",
    ".rst": "reStructuredText",
    ".txt": "Text",

    ".json": "JSON",
    ".xml": "XML",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".toml": "TOML",
    ".ini": "INI",
    ".cfg": "Configuration",
    ".conf": "Configuration",
}


def detect_language(file_path):
    file_path = Path(file_path)

    return LANGUAGES.get(
        file_path.suffix.lower(),
        "Unknown"
    )
