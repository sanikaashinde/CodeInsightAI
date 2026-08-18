def summarize_project(
    self,
    project_files: List[Dict],
) -> Dict:

    logger.info("Building repository context...")

    project_context = self.builder.build_project_context(
        project_files
    )

    llm_context = self.builder.build_llm_context(
        project_context
    )

    llm_context = self._truncate(llm_context)

    logger.info("Generating complete repository report...")

    prompt = f"""
You are a Senior Software Architect and Code Reviewer.

Analyze the following repository.

Generate a professional report using these sections.

# Repository Overview

# Main Purpose

# Folder Structure

# Important Components

# Technologies Used

# Repository Workflow

# Architecture

# Design Patterns

# Strengths

# Weaknesses

# Technical Debt

# Security Concerns

# Performance Suggestions

# Maintainability

# Executive Summary

Repository:

{llm_context}
"""

    full_report = self._cached_generate(prompt)

    return {
        "generated_at": datetime.now().isoformat(),
        "report": full_report,
        "statistics": project_context["summary"],
        "files": project_context["files"],
    }