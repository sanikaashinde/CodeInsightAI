from pathlib import Path

IGNORE = {
    "__pycache__",
    ".git",
    ".idea",
    ".vscode",
    "node_modules",
    ".venv",
    "venv",
    "env",
    "build",
    "dist",
}

def scan_project(folder):
    folder = Path(folder)
    files = []

    for path in folder.rglob("*"):

        if any(part in IGNORE for part in path.parts):
            continue

        if path.is_file():
            files.append(path)

    return {
        "files": files,
        "file_count": len(files),
    }
