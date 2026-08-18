from pathlib import Path


class RepositoryContext:

    SUPPORTED = {
        ".py",
        ".js",
        ".ts",
        ".java",
        ".cpp",
        ".c",
        ".go",
        ".php",
        ".cs",
        ".kt",
    }

    def build(self, project_folder):

        project_folder = Path(project_folder)

        context = []

        for file in project_folder.rglob("*"):

            if not file.is_file():
                continue

            if file.suffix.lower() not in self.SUPPORTED:
                continue

            try:

                code = file.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )

            except Exception:

                continue

            context.append({

                "file": file.relative_to(
                    project_folder
                ).as_posix(),

                "content": code,

            })

        return context

    def combine(

        self,

        repository,

        limit=60000,

    ):

        text = ""

        for item in repository:

            block = (
                f"\n\n### FILE : {item['file']}\n\n"
                + item["content"]
            )

            if len(text) + len(block) > limit:

                break

            text += block

        return text