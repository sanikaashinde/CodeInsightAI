from pathlib import Path

LANGUAGES = {
    ".py": "Python",
    ".java": "Java",
    ".js": "JavaScript",
    ".jsx": "React",
    ".ts": "TypeScript",
    ".tsx": "React TS",
    ".cpp": "C++",
    ".c": "C",
    ".hpp": "C++",
    ".h": "C/C++",
    ".cs": "C#",
    ".go": "Go",
    ".php": "PHP",
    ".kt": "Kotlin",
    ".swift": "Swift",
}

def detect_language(file_path):
    file_path = Path(file_path)

    return LANGUAGES.get(
        file_path.suffix.lower(),
        "Unknown"
    )
