SYSTEM_PROMPT = """
You are CodeInsightAI.

You are an expert software architect.

Always produce professional software engineering analysis.

Focus on

• readability

• maintainability

• security

• scalability

• performance

Never hallucinate.

If information is unavailable, clearly say so.
"""


SUMMARY_PROMPT = """
Summarize the following source code.

Include

1. Purpose

2. Architecture

3. Classes

4. Functions

5. Workflow

6. Suggestions

Code:

{code}
"""


REVIEW_PROMPT = """
Review the following code.

Provide

• Bugs

• Smells

• Complexity

• Security

• Improvements

Code:

{code}
"""


DOCUMENTATION_PROMPT = """
Generate professional documentation.

Include

Overview

Installation

Usage

Functions

Classes

Examples

Code:

{code}
"""