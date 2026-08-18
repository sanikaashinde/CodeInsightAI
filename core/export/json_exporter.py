import json
from datetime import datetime


class JSONExporter:
    """
    Export the complete analysis as JSON.
    Suitable for APIs, CI/CD pipelines,
    automation and future integrations.
    """

    def generate(
        self,
        project_name,
        metrics,
        quality,
        security,
        duplicate_summary,
        todo_summary,
        libraries,
        analyses,
    ):

        report = {

            "project": project_name,

            "generated": datetime.now().isoformat(),

            "metrics": metrics,

            "quality": quality,

            "security": security,

            "duplicate_code": duplicate_summary,

            "todo_summary": todo_summary,

            "libraries": [

                {

                    "library": lib,

                    "usage": count,

                }

                for lib, count in libraries

            ],

            "files": [],

        }

        # ========================================

        for analysis in analyses:

            report["files"].append(

                {

                    "file": analysis.file_name,

                    "path": analysis.file_path,

                    "language": analysis.language,

                    "lines": analysis.total_lines,

                    "imports": analysis.imports,

                    "variables": analysis.variables,

                    "functions": [

                        f.model_dump()

                        for f in analysis.functions

                    ],

                    "classes": [

                        c.model_dump()

                        for c in analysis.classes

                    ],

                }

            )

        return json.dumps(

            report,

            indent=4,

            ensure_ascii=False,

        )