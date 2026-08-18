from core.llm.llm_client import GeminiClient


class AIRefactorAdvisor:
    """
    Uses Gemini to generate professional
    refactoring suggestions for source code.
    """

    def __init__(self):

        self.client = GeminiClient()

    # ========================================

    def suggest(self, code, language="Python"):

        prompt = f"""
You are a Senior Software Architect,
Google Staff Engineer and Code Reviewer.

Review the following {language} code.

Your job is to provide ONLY constructive
refactoring suggestions.

Return markdown.

Include:

# Overall Code Quality

Rate from 1-10.

# Code Smells

Explain every smell.

# Performance Improvements

Suggest optimizations.

# Readability Improvements

Suggest naming improvements.

# SOLID Principle Violations

List violations.

# Design Improvements

Explain architectural improvements.

# Security Improvements

Mention vulnerabilities.

# Maintainability

Explain how maintainability can improve.

# Best Practices

Professional recommendations.

DO NOT rewrite the code.

Code:

{code}
"""

        return self.client.generate(prompt)

    # ========================================

    def review_project(self, analyses):

        report = []

        for analysis in analyses:

            try:

                with open(
                    analysis.file_path,
                    encoding="utf-8",
                    errors="ignore",
                ) as f:

                    code = f.read()

                report.append(

                    {

                        "file": analysis.file_name,

                        "review": self.suggest(

                            code,

                            analysis.language,

                        ),

                    }

                )

            except Exception:

                continue

        return report