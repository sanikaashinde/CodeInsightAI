from pathlib import Path

from core.analysis.complexity import ComplexityAnalyzer
from core.analysis.security import SecurityAnalyzer
from core.analysis.code_smells import detect_code_smells


class TechnicalDebtAnalyzer:

    """
    Enterprise Technical Debt Analyzer

    Estimates:
    - Technical Debt Score
    - Cleanup Time
    - Risk Level
    - Major Reasons
    """

    def __init__(self):

        self.complexity = ComplexityAnalyzer()
        self.security = SecurityAnalyzer()

    # ==========================================================
    # MAIN ANALYSIS
    # ==========================================================

    def analyze(self, project_folder, analyses):

        project_folder = Path(project_folder)

        debt = 0

        reasons = []

        total_docstrings = 0
        total_functions = 0

        total_smells = 0

        high_complexity = 0

        security_issues = 0

        large_files = 0

        # ======================================================
        # ANALYSE PARSED FILES
        # ======================================================

        for analysis in analyses:

            total_functions += len(analysis.functions)

            for func in analysis.functions:

                if func.docstring:
                    total_docstrings += 1

        # ======================================================
        # ANALYSE PROJECT FILES
        # ======================================================

        for file in project_folder.rglob("*.py"):

            try:

                code = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

            except Exception:

                continue

            # ---------------------------------------------
            # Complexity
            # ---------------------------------------------

            complexity = self.complexity.analyze(code)

            for func in complexity["functions"]:

                if func["complexity"] >= 10:

                    high_complexity += 1

            # ---------------------------------------------
            # Security
            # ---------------------------------------------

            security = self.security.analyze(file)

            security_issues += len(
                security["issues"]
            )

            # ---------------------------------------------
            # Smells
            # ---------------------------------------------

            smells = detect_code_smells(code)

            total_smells += len(smells)

            # ---------------------------------------------
            # File Size
            # ---------------------------------------------

            if len(code.splitlines()) > 500:

                large_files += 1

        # ======================================================
        # DOCUMENTATION
        # ======================================================

        documentation = 100

        if total_functions:

            documentation = round(

                total_docstrings
                / total_functions
                * 100,

                1,

            )

        # ======================================================
        # PENALTIES
        # ======================================================

        if documentation < 80:

            penalty = (80 - documentation) * 0.4

            debt += penalty

            reasons.append(

                f"Documentation coverage is only {documentation}%"

            )

        if total_smells:

            debt += total_smells * 2

            reasons.append(

                f"{total_smells} code smells detected"

            )

        if high_complexity:

            debt += high_complexity * 3

            reasons.append(

                f"{high_complexity} high complexity functions"

            )

        if security_issues:

            debt += security_issues * 5

            reasons.append(

                f"{security_issues} security issues"

            )

        if large_files:

            debt += large_files * 2

            reasons.append(

                f"{large_files} very large files"

            )

        debt = round(min(debt, 100), 1)

        # ======================================================
        # CLEANUP ESTIMATE
        # ======================================================

        cleanup_hours = round(

            debt * 0.25,

            1,

        )

        # ======================================================
        # RISK
        # ======================================================

        if debt <= 25:

            risk = "LOW"

        elif debt <= 50:

            risk = "MEDIUM"

        elif debt <= 75:

            risk = "HIGH"

        else:

            risk = "CRITICAL"

        # ======================================================
        # RETURN
        # ======================================================

        return {

            "score": debt,

            "cleanup_hours": cleanup_hours,

            "risk": risk,

            "documentation": documentation,

            "code_smells": total_smells,

            "high_complexity": high_complexity,

            "security_issues": security_issues,

            "large_files": large_files,

            "reasons": reasons,

        }