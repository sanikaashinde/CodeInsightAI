from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from core.analysis import (
    analyze_complexity,
    maintainability_score,
    detect_code_smells,
    project_metrics,
)

code = Path("sample_project/main.py").read_text()

print(analyze_complexity(code))
print(maintainability_score(code))
print(project_metrics(code))
print(detect_code_smells(code))