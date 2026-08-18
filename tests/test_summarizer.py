from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from core.parser import load_project
from core.llm.summarizer import RepositorySummarizer

files = load_project("sample_project")

engine = RepositorySummarizer()

report = engine.summarize_project(files)

print(report["generated_at"])
print()
print(report["summary"][:500])