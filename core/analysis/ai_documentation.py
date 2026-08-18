from pathlib import Path

from core.llm.llm_client import GeminiClient


class AIDocumentationGenerator:
    """
    Generates professional documentation
    using Gemini.
    """

    def __init__(self):

        self.client = GeminiClient()

    # =====================================================

    def generate_for_code(
        self,
        code,
        language="Python",
    ):

        prompt = f"""
You are a Senior Software Documentation Engineer.

Generate professional documentation.

Language:
{language}

Return markdown.

Include:

# Overview

Explain what the code does.

# Functions

Explain every function.

# Classes

Explain every class.

# Inputs

Explain parameters.

# Outputs

Explain return values.

# Internal Workflow

Explain the execution flow.

# Dependencies

Mention imported libraries.

# Usage Example

Provide a simple example.

# Improvements

Suggest documentation improvements.

Code:

{code}
"""

        return self.client.generate(prompt)

    # =====================================================

    def generate_project(
        self,
        analyses,
    ):

        results = []

        for analysis in analyses:

            try:

                source = Path(
                    analysis.file_path
                ).read_text(
                    encoding="utf-8",
                    errors="ignore",
                )

            except Exception:

                continue

            documentation = self.generate_for_code(

                source,

                analysis.language,

            )

            results.append(

                {

                    "file": analysis.file_name,

                    "documentation": documentation,

                }

            )

        return results

    # =====================================================

    def generate_readme(
        self,
        project_name,
        analyses,
    ):

        combined = ""

        for analysis in analyses:

            try:

                combined += Path(
                    analysis.file_path
                ).read_text(
                    encoding="utf-8",
                    errors="ignore",
                )

                combined += "\n\n"

            except Exception:

                pass

        prompt = f"""
Create a professional GitHub README.

Project Name:

{project_name}

Return markdown.

Include:

# Project Overview

# Features

# Folder Structure

# Installation

# Usage

# Technologies

# Architecture

# Future Improvements

# License

Code:

{combined[:35000]}
"""

        return self.client.generate(prompt)