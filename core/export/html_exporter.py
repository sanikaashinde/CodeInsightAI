from datetime import datetime


class HTMLExporter:
    """
    Generate a professional HTML report for
    CodeInsight AI.
    """

    def generate(
        self,
        project_name,
        metrics,
        quality,
        security_score,
        ai_review,
        libraries,
    ):

        libraries_html = ""

        for lib, count in libraries:

            libraries_html += f"""
            <tr>
                <td>{lib}</td>
                <td>{count}</td>
            </tr>
            """

        html = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<title>{project_name}</title>

<style>

body{{
font-family:Arial;
margin:40px;
background:#fafafa;
}}

h1{{
color:#1f77b4;
}}

table{{
width:100%;
border-collapse:collapse;
margin-top:15px;
}}

th,td{{
border:1px solid #ddd;
padding:10px;
}}

th{{
background:#1f77b4;
color:white;
}}

.card{{
background:white;
padding:20px;
margin-top:20px;
border-radius:10px;
box-shadow:0px 2px 10px rgba(0,0,0,.1);
}}

pre{{
white-space:pre-wrap;
}}

</style>

</head>

<body>

<h1>🚀 CodeInsight AI Report</h1>

Generated:
{datetime.now().strftime("%d %B %Y %H:%M")}

<div class="card">

<h2>Project</h2>

<b>{project_name}</b>

</div>

<div class="card">

<h2>Engineering Metrics</h2>

<table>

<tr>

<th>Metric</th>

<th>Value</th>

</tr>

<tr><td>Files</td><td>{metrics['files']}</td></tr>

<tr><td>Lines</td><td>{metrics['lines']}</td></tr>

<tr><td>Functions</td><td>{metrics['functions']}</td></tr>

<tr><td>Classes</td><td>{metrics['classes']}</td></tr>

<tr><td>Imports</td><td>{metrics['imports']}</td></tr>

<tr><td>Documentation</td><td>{metrics['documentation']}%</td></tr>

<tr><td>Average Complexity</td><td>{metrics['average_complexity']}</td></tr>

<tr><td>Maintainability</td><td>{metrics['maintainability']}</td></tr>

<tr><td>Architecture</td><td>{metrics['architecture']}</td></tr>

</table>

</div>

<div class="card">

<h2>Quality</h2>

<table>

<tr><td>Overall</td><td>{quality['overall']}</td></tr>

<tr><td>Documentation</td><td>{quality['documentation']}</td></tr>

<tr><td>Readability</td><td>{quality['readability']}</td></tr>

<tr><td>Maintainability</td><td>{quality['maintainability']}</td></tr>

<tr><td>Architecture</td><td>{quality['architecture']}</td></tr>

</table>

</div>

<div class="card">

<h2>Security</h2>

Security Score :
<b>{security_score}/100</b>

</div>

<div class="card">

<h2>Top Libraries</h2>

<table>

<tr>

<th>Library</th>

<th>Usage</th>

</tr>

{libraries_html}

</table>

</div>

<div class="card">

<h2>AI Project Review</h2>

<pre>{ai_review}</pre>

</div>

</body>

</html>
"""

        return html