from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)


class PDFExporter:

    def __init__(self):

        self.styles = getSampleStyleSheet()

        self.styles["Title"].alignment = TA_CENTER

    def generate(

        self,

        project_name,

        project,

        result,

        stats,

        scores,

        analyses=None,

        ai_review=None,

        security_score=None,

        security_issues=None

    ):

        buffer = BytesIO()

        doc = SimpleDocTemplate(

            buffer,

            rightMargin=30,

            leftMargin=30,

            topMargin=30,

            bottomMargin=30

        )

        story = []

        title = self.styles["Title"]
        h1 = self.styles["Heading1"]
        h2 = self.styles["Heading2"]
        body = self.styles["BodyText"]

        # =====================================================
        # COVER PAGE
        # =====================================================

        story.append(
            Paragraph(
                "CodeInsight AI",
                title
            )
        )

        story.append(
            Paragraph(
                "Professional Static Code Analysis Report",
                h1
            )
        )

        story.append(Spacer(1, 25))

        story.append(
            Paragraph(
                f"<b>Project :</b> {project_name}",
                body
            )
        )

        story.append(
            Paragraph(
                f"<b>Date :</b> {datetime.now().strftime('%d-%m-%Y %H:%M')}",
                body
            )
        )

        story.append(
            Paragraph(
                f"<b>Total Files :</b> {project['file_count']}",
                body
            )
        )

        story.append(
            Paragraph(
                f"<b>Total Lines :</b> {project['total_lines']}",
                body
            )
        )

        story.append(PageBreak())

        # =====================================================
        # PROJECT OVERVIEW
        # =====================================================

        story.append(
            Paragraph(
                "Project Overview",
                h1
            )
        )

        overview = [

            ["Metric", "Value"],

            ["Project Name", project_name],

            ["Total Files", project["file_count"]],

            ["Lines of Code", project["total_lines"]],

            ["Functions", result["functions"]],

            ["Classes", result["classes"]]

        ]

        table = Table(
            overview,
            colWidths=[220, 220]
        )

        table.setStyle(

            TableStyle([

                ("BACKGROUND", (0,0), (-1,0), colors.darkblue),

                ("TEXTCOLOR", (0,0), (-1,0), colors.white),

                ("GRID", (0,0), (-1,-1), 1, colors.black),

                ("BACKGROUND", (0,1), (-1,-1), colors.beige),

                ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold")

            ])

        )

        story.append(table)

        story.append(Spacer(1, 20))

        # =====================================================
        # EXECUTIVE SUMMARY
        # =====================================================

        story.append(
            Paragraph(
                "Executive Summary",
                h1
            )
        )

        summary = f"""
<b>{project_name}</b> contains
<b>{project['file_count']}</b> source files with
<b>{project['total_lines']}</b> lines of code.<br/><br/>

<b>Total Functions :</b> {result['functions']}<br/>
<b>Total Classes :</b> {result['classes']}<br/>
<b>Imports :</b> {stats['imports']}<br/>
<b>Overall Quality :</b> {scores['overall']}/100
"""

        story.append(
            Paragraph(
                summary,
                body
            )
        )

        story.append(Spacer(1, 20))

        # =====================================================
        # PROJECT HEALTH
        # =====================================================

        story.append(
            Paragraph(
                "Project Health",
                h1
            )
        )

        health = [

            ["Metric", "Value"],

            ["Imports", stats["imports"]],

            ["Docstrings", stats["docstrings"]],

            ["Large Functions", stats["large_functions"]],

            ["Async Functions", stats["async_functions"]]

        ]

        table = Table(
            health,
            colWidths=[220,220]
        )

        table.setStyle(

            TableStyle([

                ("BACKGROUND",(0,0),(-1,0),colors.darkgreen),

                ("TEXTCOLOR",(0,0),(-1,0),colors.white),

                ("GRID",(0,0),(-1,-1),1,colors.black),

                ("BACKGROUND",(0,1),(-1,-1),colors.beige),

                ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold")

            ])

        )

        story.append(table)

        story.append(PageBreak())

        # =====================================================
        # QUALITY SCORE
        # =====================================================

        story.append(
            Paragraph(
                "Quality Score",
                h1
            )
        )

        quality = [

            ["Metric","Score"],

            ["Overall", scores["overall"]],

            ["Architecture", scores["architecture"]],

            ["Maintainability", scores["maintainability"]],

            ["Documentation", scores["documentation"]],

            ["Readability", scores["readability"]]

        ]

        table = Table(
            quality,
            colWidths=[220,220]
        )

        table.setStyle(

            TableStyle([

                ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

                ("TEXTCOLOR",(0,0),(-1,0),colors.white),

                ("GRID",(0,0),(-1,-1),1,colors.black),

                ("BACKGROUND",(0,1),(-1,-1),colors.beige),

                ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold")

            ])

        )

        story.append(table)

        story.append(Spacer(1,20))

        # =====================================================
        # SECURITY ANALYSIS
        # =====================================================

        story.append(
            Paragraph(
                "Security Analysis",
                h1
            )
        )

        security_data = [

            ["Metric", "Value"],

            [
                "Security Score",
                security_score if security_score is not None else "N/A"
            ],

            [
                "Security Issues",
                len(security_issues) if security_issues else 0
            ]

        ]

        table = Table(
            security_data,
            colWidths=[220, 220]
        )

        table.setStyle(

            TableStyle([

                ("BACKGROUND",(0,0),(-1,0),colors.darkred),

                ("TEXTCOLOR",(0,0),(-1,0),colors.white),

                ("GRID",(0,0),(-1,-1),1,colors.black),

                ("BACKGROUND",(0,1),(-1,-1),colors.beige),

                ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold")

            ])

        )

        story.append(table)

        story.append(Spacer(1,20))

        # =====================================================
        # DETECTED SECURITY ISSUES
        # =====================================================

        story.append(
            Paragraph(
                "Detected Security Issues",
                h2
            )
        )

        if security_issues:

            issue_table = [

                ["Type", "Severity", "Line", "Description"]

            ]

            for issue in security_issues:

                issue_table.append([

                    issue.get("type", "-"),

                    issue.get("severity", "-"),

                    str(issue.get("line", "-")),

                    issue.get("message", "-")

                ])

            table = Table(

                issue_table,

                colWidths=[100,70,50,220]

            )

            table.setStyle(

                TableStyle([

                    ("BACKGROUND",(0,0),(-1,0),colors.red),

                    ("TEXTCOLOR",(0,0),(-1,0),colors.white),

                    ("GRID",(0,0),(-1,-1),0.5,colors.black),

                    ("BACKGROUND",(0,1),(-1,-1),colors.beige),

                    ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),

                    ("VALIGN",(0,0),(-1,-1),"TOP")

                ])

            )

            story.append(table)

        else:

            story.append(

                Paragraph(

                    "✅ No security issues detected.",

                    body

                )

            )

        story.append(PageBreak())

        # =====================================================
        # DETAILED FILE ANALYSIS
        # =====================================================

        if analyses:

            story.append(

                Paragraph(

                    "Detailed File Analysis",

                    h1

                )

            )

            story.append(Spacer(1,20))

            for analysis in analyses:

                story.append(
                    Paragraph(
                        f"<b>📄 {analysis.file_name}</b>",
                        h2
                    )
                )

                story.append(
                    Paragraph(
                        f"Language : {analysis.language}",
                        body
                    )
                )

                story.append(
                    Paragraph(
                        f"Lines of Code : {analysis.total_lines}",
                        body
                    )
                )

                story.append(Spacer(1,10))

                # ==========================================
                # IMPORTS
                # ==========================================

                story.append(
                    Paragraph(
                        "<b>Imports</b>",
                        body
                    )
                )

                if analysis.imports:

                    for imp in analysis.imports:

                        story.append(
                            Paragraph(
                                f"• {imp}",
                                body
                            )
                        )

                else:

                    story.append(
                        Paragraph(
                            "No imports detected.",
                            body
                        )
                    )

                story.append(Spacer(1,10))

                # ==========================================
                # VARIABLES
                # ==========================================

                story.append(
                    Paragraph(
                        "<b>Variables</b>",
                        body
                    )
                )

                if analysis.variables:

                    for var in analysis.variables:

                        story.append(
                            Paragraph(
                                f"• {var}",
                                body
                            )
                        )

                else:

                    story.append(
                        Paragraph(
                            "No variables detected.",
                            body
                        )
                    )

                story.append(Spacer(1,10))

                # ==========================================
                # FUNCTIONS
                # ==========================================

                story.append(
                    Paragraph(
                        "<b>Functions</b>",
                        body
                    )
                )

                if analysis.functions:

                    function_table = [

                        ["Name", "Parameters", "Return", "Line"]

                    ]

                    for func in analysis.functions:

                        function_table.append([

                            func.name,

                            ", ".join(func.parameters)
                            if func.parameters else "None",

                            func.return_type
                            if func.return_type else "-",

                            str(func.line_number)

                        ])

                    table = Table(
                        function_table,
                        colWidths=[120,170,90,60]
                    )

                    table.setStyle(

                        TableStyle([

                            ("BACKGROUND",(0,0),(-1,0),colors.darkblue),

                            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

                            ("GRID",(0,0),(-1,-1),0.5,colors.black),

                            ("BACKGROUND",(0,1),(-1,-1),colors.beige),

                            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold")

                        ])

                    )

                    story.append(table)

                else:

                    story.append(
                        Paragraph(
                            "No functions detected.",
                            body
                        )
                    )

                story.append(Spacer(1,15))

                # =====================================================
                # CLASSES
                # =====================================================

                story.append(
                    Paragraph(
                        "<b>Classes</b>",
                        body
                    )
                )

                if analysis.classes:

                    class_table = [

                        ["Class", "Inheritance", "Methods", "Line"]

                    ]

                    for cls in analysis.classes:

                        class_table.append([

                            cls.name,

                            ", ".join(cls.bases)
                            if cls.bases else "None",

                            ", ".join(cls.methods)
                            if cls.methods else "None",

                            str(cls.line_number)

                        ])

                    table = Table(
                        class_table,
                        colWidths=[110,110,170,50]
                    )

                    table.setStyle(
                        TableStyle([

                            ("BACKGROUND",(0,0),(-1,0),colors.darkgreen),

                            ("TEXTCOLOR",(0,0),(-1,0),colors.white),

                            ("GRID",(0,0),(-1,-1),0.5,colors.black),

                            ("BACKGROUND",(0,1),(-1,-1),colors.beige),

                            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold")

                        ])
                    )

                    story.append(table)

                else:

                    story.append(
                        Paragraph(
                            "No classes detected.",
                            body
                        )
                    )

                story.append(Spacer(1,10))

                # =====================================================
                # DOCUMENTATION
                # =====================================================

                documented = sum(
                    1 for f in analysis.functions
                    if getattr(f, "docstring", None)
                )

                async_count = sum(
                    1 for f in analysis.functions
                    if getattr(f, "is_async", False)
                )

                story.append(
                    Paragraph(
                        f"<b>Documented Functions :</b> {documented}/{len(analysis.functions)}",
                        body
                    )
                )

                story.append(
                    Paragraph(
                        f"<b>Async Functions :</b> {async_count}",
                        body
                    )
                )

                story.append(PageBreak())

        # =====================================================
        # AI REVIEW
        # =====================================================

        if ai_review:

            story.append(
                Paragraph(
                    "AI Project Review",
                    h1
                )
            )

            story.append(Spacer(1,10))

            for line in ai_review.split("\n"):

                if line.strip():

                    story.append(
                        Paragraph(
                            line,
                            body
                        )
                    )

            story.append(PageBreak())

        # =====================================================
        # FINAL RECOMMENDATION
        # =====================================================

        story.append(
            Paragraph(
                "Final Recommendation",
                h1
            )
        )

        overall = scores["overall"]

        if overall >= 90:

            recommendation = """
<b>Excellent Project</b><br/><br/>

• Enterprise-grade Architecture<br/>
• Excellent Maintainability<br/>
• Production Ready<br/>
• Resume Ready<br/>
• Internship Ready
"""

        elif overall >= 75:

            recommendation = """
<b>Very Good Project</b><br/><br/>

• Good Architecture<br/>
• Minor Improvements Recommended<br/>
• Resume Ready
"""

        elif overall >= 60:

            recommendation = """
<b>Average Project</b><br/><br/>

• Improve Documentation<br/>
• Reduce Complexity<br/>
• Add More Tests
"""

        else:

            recommendation = """
<b>Needs Improvement</b><br/><br/>

• Improve Architecture<br/>
• Improve Maintainability<br/>
• Add Documentation
"""

        story.append(
            Paragraph(
                recommendation,
                body
            )
        )

        story.append(Spacer(1,20))

        story.append(
            Paragraph(
                "Generated by <b>CodeInsight AI</b>",
                body
            )
        )

        # =====================================================
        # BUILD PDF
        # =====================================================

        doc.build(story)

        pdf = buffer.getvalue()

        buffer.close()

        return pdf