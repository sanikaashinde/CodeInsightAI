from __future__ import annotations

import logging
import os
import time
from typing import Optional

import streamlit as st
from dotenv import load_dotenv
from google import genai


load_dotenv()

logger = logging.getLogger(__name__)


class GeminiClient:

    # Prefer the current fast Gemini model, with fallback models.
    MODELS = [
        "gemini-3.6-flash",
        "gemini-3.5-flash",
        "gemini-2.0-flash",
    ]

    def __init__(self):

        api_key = None

        # -------------------------------------------------
        # Streamlit Cloud / Streamlit secrets
        # -------------------------------------------------

        try:
            api_key = st.secrets.get("GEMINI_API_KEY")
        except Exception:
            api_key = None

        # -------------------------------------------------
        # Environment / .env fallback
        # -------------------------------------------------

        if not api_key:
            api_key = os.getenv("GEMINI_API_KEY")

        self.client = None

        if api_key:
            try:
                self.client = genai.Client(
                    api_key=api_key
                )

            except Exception as e:
                logger.exception(
                    "Failed to initialize Gemini client: %s",
                    e,
                )

                self.client = None

        else:
            logger.warning(
                "GEMINI_API_KEY not found. "
                "Gemini AI features are disabled."
            )

    def is_available(self) -> bool:

        return self.client is not None

    def _generate_with_model(
        self,
        model: str,
        prompt: str,
    ) -> Optional[str]:

        if self.client is None:
            return None

        retries = 2

        for attempt in range(retries):

            try:

                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt,
                )

                if response is not None:

                    text = getattr(
                        response,
                        "text",
                        None,
                    )

                    if text:
                        return text.strip()

                return None

            except Exception as e:

                error = str(e)

                logger.warning(
                    "%s failed: %s",
                    model,
                    error,
                )

                # Retry temporary server/rate-limit failures.
                if (
                    "503" in error
                    or "429" in error
                    or "temporarily" in error.lower()
                ):

                    if attempt < retries - 1:

                        wait = 2 ** attempt

                        time.sleep(wait)

                        continue

                # Model not available.
                if "404" in error:
                    return None

                return None

        return None

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
    ) -> str:

        if self.client is None:

            return (
                "Gemini AI is not configured.\n\n"
                "Please add GEMINI_API_KEY to Streamlit Secrets "
                "or your local .env file."
            )

        final_prompt = prompt

        if system_prompt:

            final_prompt = (
                f"{system_prompt}\n\n"
                f"{prompt}"
            )

        for model in self.MODELS:

            result = self._generate_with_model(
                model=model,
                prompt=final_prompt,
            )

            if result:

                logger.info(
                    "Gemini response generated using %s",
                    model,
                )

                return result

        return (
            "Gemini could not generate a response.\n\n"
            "Please verify your API key, model availability, "
            "quota, and network connection."
        )

    def summarize_code(
        self,
        code: str,
        language: str,
    ) -> str:

        prompt = f"""
You are an expert software engineer.

Analyze the following {language} code.

Provide a clear natural-language explanation containing:

1. Project/code purpose
2. What the code is doing
3. Main workflow
4. Important functions and classes
5. Inputs
6. Important transformations or processing
7. Outputs
8. Security or quality concerns
9. Complexity considerations
10. Recommended improvements

Make the explanation understandable to a developer reviewing
the project for the first time.

CODE:

{code}
"""

        return self.generate(prompt)

    def explain_function(
        self,
        function_code: str,
    ) -> str:

        prompt = f"""
Explain this function clearly.

Include:

- Purpose
- Parameters
- Return value
- Internal workflow
- Important conditions or logic
- Time complexity
- Possible improvements

FUNCTION:

{function_code}
"""

        return self.generate(prompt)

    def review_code(
        self,
        code: str,
    ) -> str:

        prompt = f"""
Review the following code as a senior software engineer.

Provide:

- Purpose and behavior
- Bugs or correctness risks
- Security issues
- Performance problems
- Code smells
- Maintainability concerns
- Best practices
- Refactoring suggestions
- Final assessment

CODE:

{code}
"""

        return self.generate(prompt)

    def chat(
        self,
        message: str,
    ) -> str:

        return self.generate(message)
