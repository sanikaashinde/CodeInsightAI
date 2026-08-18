from __future__ import annotations

import logging
import os
import time
from typing import Optional

from dotenv import load_dotenv
from google import genai

load_dotenv()

logger = logging.getLogger(__name__)


class GeminiClient:

    MODELS = [
        "gemini-3.5-flash",
        "gemini-3.1-flash-lite",
        "gemini-2.0-flash",
    ]

    def __init__(self):

        api_key = os.getenv("GEMINI_API_KEY")

        self.client = None

        if api_key:
            self.client = genai.Client(api_key=api_key)
        else:
            logger.warning(
                "GEMINI_API_KEY not found. Gemini AI features are disabled."
            )

    def _generate_with_model(
        self,
        model: str,
        prompt: str,
    ) -> Optional[str]:

        retries = 3

        for attempt in range(retries):

            try:

                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt,
                )

                if hasattr(response, "text") and response.text:
                    return response.text.strip()

                return "No response generated."

            except Exception as e:

                error = str(e)

                logger.warning(f"{model} failed: {error}")

                if "404" in error:
                    break

                if "503" in error:

                    if attempt < retries - 1:
                        wait = 2 ** attempt
                        logger.info(f"Retrying in {wait}s...")
                        time.sleep(wait)
                        continue

                    break

                if "429" in error:
                    break

                break

        return None

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
    ) -> str:

        if self.client is None:
            return (
                "Gemini AI features are currently unavailable.\n\n"
                "Please configure GEMINI_API_KEY in your .env file "
                "to enable AI-powered features."
            )

        if system_prompt:
            prompt = f"{system_prompt}\n\n{prompt}"

        for model in self.MODELS:

            result = self._generate_with_model(
                model=model,
                prompt=prompt,
            )

            if result:
                logger.info(f"Using model: {model}")
                return result

        return (
            "Unable to generate response.\n\n"
            "Possible reasons:\n"
            "- Gemini servers are busy (503)\n"
            "- API quota exceeded (429)\n"
            "- Model unavailable\n"
        )

    def summarize_code(
        self,
        code: str,
        language: str,
    ) -> str:

        prompt = f"""
Analyze the following {language} code.

Explain:

1. Purpose
2. Classes
3. Functions
4. Workflow
5. Time Complexity
6. Space Complexity
7. Improvements

Code:

{code}
"""

        return self.generate(prompt)

    def explain_function(
        self,
        function_code: str,
    ) -> str:

        prompt = f"""
Explain this function.

Include:

- Purpose
- Parameters
- Return Value
- Internal Workflow
- Time Complexity
- Possible Improvements

Function:

{function_code}
"""

        return self.generate(prompt)

    def review_code(
        self,
        code: str,
    ) -> str:

        prompt = f"""
Review the following code.

Mention:

- Bugs
- Security Issues
- Performance Problems
- Code Smells
- Best Practices
- Refactoring Suggestions

Code:

{code}
"""

        return self.generate(prompt)

    def chat(
        self,
        message: str,
    ) -> str:

        return self.generate(message)
