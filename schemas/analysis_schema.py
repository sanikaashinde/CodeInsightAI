from typing import List, Optional
from pydantic import BaseModel, Field


# ==========================================================
# FUNCTION INFO
# ==========================================================

class FunctionInfo(BaseModel):
    name: str
    parameters: List[str] = Field(default_factory=list)
    return_type: Optional[str] = None
    decorators: List[str] = Field(default_factory=list)
    docstring: Optional[str] = None
    line_number: int
    is_async: bool = False

    # New Fields
    complexity: int = 0
    length: int = 0
    has_return: bool = False


# ==========================================================
# CLASS INFO
# ==========================================================

class ClassInfo(BaseModel):
    name: str
    bases: List[str] = Field(default_factory=list)
    methods: List[str] = Field(default_factory=list)
    docstring: Optional[str] = None
    line_number: int

    # New Fields
    method_count: int = 0
    attribute_count: int = 0


# ==========================================================
# ANALYSIS RESULT
# ==========================================================

class AnalysisResult(BaseModel):

    # -------------------------------
    # File Information
    # -------------------------------

    file_name: str
    file_path: Optional[str] = None
    extension: Optional[str] = None
    language: str

    # -------------------------------
    # Parsed Data
    # -------------------------------

    imports: List[str] = Field(default_factory=list)
    variables: List[str] = Field(default_factory=list)
    functions: List[FunctionInfo] = Field(default_factory=list)
    classes: List[ClassInfo] = Field(default_factory=list)

    # -------------------------------
    # Statistics
    # -------------------------------

    total_lines: int = 0
    blank_lines: int = 0
    comment_lines: int = 0

    # -------------------------------
    # File Metadata
    # -------------------------------

    file_size: int = 0

    # -------------------------------
    # Code Quality
    # -------------------------------

    todo_count: int = 0
    fixme_count: int = 0

    syntax_error: bool = False
    syntax_error_message: Optional[str] = None

    # -------------------------------
    # Summary
    # -------------------------------

    total_functions: int = 0
    total_classes: int = 0
    total_imports: int = 0
    total_variables: int = 0