from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from core.parser import load_project
from core.llm.context_builder import ContextBuilder

files = load_project("sample_project")

builder = ContextBuilder()

context = builder.build_project_context(files)

print(context["summary"])

print()

prompt = builder.build_llm_context(context)

print(prompt[:1500])