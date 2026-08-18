from pathlib import Path

from core.parser.parser import PythonParser


class LanguageParser:
    """
    Unified parser for multiple programming languages.

    Python -> Full AST parser

    Other languages -> Structural parser
    """

    PYTHON = {
        ".py"
    }

    JAVA = {
        ".java"
    }

    JAVASCRIPT = {
        ".js",
        ".jsx"
    }

    TYPESCRIPT = {
        ".ts",
        ".tsx"
    }

    CPP = {
        ".cpp",
        ".c",
        ".hpp",
        ".h"
    }

    CSHARP = {
        ".cs"
    }

    GO = {
        ".go"
    }

    PHP = {
        ".php"
    }

    KOTLIN = {
        ".kt"
    }

    SWIFT = {
        ".swift"
    }

    def __init__(self):

        self.python = PythonParser()

    # ===================================================

    def parse(self, filepath):

        filepath = Path(filepath)

        suffix = filepath.suffix.lower()

        if suffix in self.PYTHON:

            return self.python.parse(filepath)

        return self.generic_parse(filepath)

    # ===================================================

    def generic_parse(self, filepath):

        try:

            source = filepath.read_text(

                encoding="utf-8",

                errors="ignore",

            )

        except Exception:

            source = ""

        imports = []

        classes = []

        functions = []

        variables = []

        for line in source.splitlines():

            text = line.strip()

            # -------------------------

            if text.startswith("import "):

                imports.append(text)

            elif text.startswith("from "):

                imports.append(text)

            # -------------------------

            if " class " in f" {text} ":

                classes.append(text)

            elif text.startswith("class "):

                classes.append(text)

            # -------------------------

            keywords = [

                "function",

                "func",

                "void",

                "def",

                "public",

                "private",

                "protected",

            ]

            if any(

                text.startswith(word)

                for word in keywords

            ):

                functions.append(text)

        return {

            "file_name": filepath.name,

            "file_path": str(filepath),

            "language": self.detect_language(filepath),

            "imports": imports,

            "classes": classes,

            "functions": functions,

            "variables": variables,

            "total_lines": len(

                source.splitlines()

            ),

        }

    # ===================================================

    def detect_language(self, filepath):

        ext = Path(filepath).suffix.lower()

        mapping = {

            ".py": "Python",

            ".java": "Java",

            ".js": "JavaScript",

            ".jsx": "React",

            ".ts": "TypeScript",

            ".tsx": "React TS",

            ".cpp": "C++",

            ".c": "C",

            ".cs": "C#",

            ".go": "Go",

            ".php": "PHP",

            ".kt": "Kotlin",

            ".swift": "Swift",

        }

        return mapping.get(

            ext,

            "Unknown"

        )