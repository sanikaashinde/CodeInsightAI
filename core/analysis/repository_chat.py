from core.llm.llm_client import GeminiClient
from core.analysis.repository_context import RepositoryContext


class RepositoryChat:

    def __init__(self):

        self.client = GeminiClient()

        self.context_builder = RepositoryContext()

    def ask(

        self,

        project_folder,

        question,

    ):

        repository = self.context_builder.build(
            project_folder
        )

        codebase = self.context_builder.combine(
            repository
        )

        prompt = f"""
You are an expert software architect.

Answer ONLY using the supplied repository.

If the answer is not present,
say that it is not available.

Repository:

{codebase}

Question:

{question}

Provide:

• Explanation

• File names

• Suggestions
"""

        return self.client.generate(prompt)