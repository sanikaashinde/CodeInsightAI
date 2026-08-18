from pathlib import Path


class RepositoryInsights:

    def analyze(

        self,

        project,

        analyses,

        complexities,

        security_results,

        quality_scores,

    ):

        insights = {}

        # =====================================
        # Largest File
        # =====================================

        largest_file = None
        largest_lines = 0

        for analysis in analyses:

            if analysis.total_lines > largest_lines:

                largest_lines = analysis.total_lines
                largest_file = analysis.file_name

        insights["largest_file"] = {

            "file": largest_file,
            "lines": largest_lines,

        }

        # =====================================
        # Most Functions
        # =====================================

        max_functions = None
        max_count = 0

        for analysis in analyses:

            if len(analysis.functions) > max_count:

                max_count = len(analysis.functions)
                max_functions = analysis.file_name

        insights["most_functions"] = {

            "file": max_functions,
            "count": max_count,

        }

        # =====================================
        # Most Classes
        # =====================================

        max_classes = None
        class_count = 0

        for analysis in analyses:

            if len(analysis.classes) > class_count:

                class_count = len(analysis.classes)
                max_classes = analysis.file_name

        insights["most_classes"] = {

            "file": max_classes,
            "count": class_count,

        }

        # =====================================
        # Most Complex File
        # =====================================

        complex_file = None
        complex_score = -1

        for index, item in enumerate(complexities):

            avg = item.get("average_complexity", 0)

            if avg > complex_score:

                complex_score = avg

                if index < len(analyses):

                    complex_file = analyses[index].file_name

        insights["most_complex"] = {

            "file": complex_file,
            "complexity": round(complex_score, 2),

        }

        # =====================================
        # Lowest Security
        # =====================================

        lowest_security = 101
        weakest_security_file = None

        for index, sec in enumerate(security_results):

            score = sec.get("score", 100)

            if score < lowest_security:

                lowest_security = score

                if index < len(analyses):

                    weakest_security_file = analyses[index].file_name

        insights["weakest_security"] = {

            "file": weakest_security_file,
            "score": lowest_security,

        }

        # =====================================
        # Best Documentation
        # =====================================

        best_doc_file = None
        best_doc = -1

        for analysis in analyses:

            funcs = len(analysis.functions)

            if funcs == 0:

                continue

            documented = sum(

                1

                for func in analysis.functions

                if func.docstring

            )

            coverage = documented / funcs * 100

            if coverage > best_doc:

                best_doc = coverage
                best_doc_file = analysis.file_name

        insights["best_documentation"] = {

            "file": best_doc_file,
            "coverage": round(best_doc, 1)
            if best_doc >= 0 else 0,

        }

        # =====================================
        # Repository Overview
        # =====================================

        insights["overview"] = {

            "files": project["file_count"],

            "lines": project["total_lines"],

            "functions": sum(
                len(a.functions)
                for a in analyses
            ),

            "classes": sum(
                len(a.classes)
                for a in analyses
            ),

        }

        # =====================================
        # Quality
        # =====================================

        insights["quality"] = quality_scores

        return insights