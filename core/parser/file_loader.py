from pathlib import Path


SUPPORTED_EXTENSIONS = {
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


def load_file(file_path: str):
    """
    Load code from a source file.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(path)

    if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported file: {path.name}")

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        code = f.read()

    return {
        "filename": path.name,
        "path": str(path),
        "extension": path.suffix,
        "code": code,
        "size": path.stat().st_size,
    }