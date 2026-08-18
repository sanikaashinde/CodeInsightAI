from pathlib import Path
from datetime import datetime

try:
    from git import Repo
except Exception:
    Repo = None


class GitAnalyzer:
    """
    Analyze Git repository statistics.

    Requires:
        pip install GitPython
    """

    def analyze(self, project_folder):

        project_folder = Path(project_folder)

        if Repo is None:

            return {
                "available": False,
                "message": "GitPython not installed."
            }

        try:

            repo = Repo(project_folder)

        except Exception:

            return {
                "available": False,
                "message": "Not a Git repository."
            }

        commits = list(repo.iter_commits())

        branches = [b.name for b in repo.branches]

        contributors = {}

        for commit in commits:

            author = commit.author.name

            contributors[author] = (

                contributors.get(author, 0)

                + 1

            )

        latest = None

        if commits:

            latest = {

                "hash": commits[0].hexsha[:8],

                "author": commits[0].author.name,

                "message": commits[0].message.strip(),

                "date": datetime.fromtimestamp(

                    commits[0].committed_date

                ).strftime("%Y-%m-%d %H:%M"),

            }

        return {

            "available": True,

            "total_commits": len(commits),

            "branches": branches,

            "contributors": contributors,

            "latest_commit": latest,

        }

    # =====================================

    def top_contributors(self, result):

        if not result["available"]:

            return []

        ranking = list(

            result["contributors"].items()

        )

        ranking.sort(

            key=lambda x: x[1],

            reverse=True,

        )

        return ranking

    # =====================================

    def repository_health(self, result):

        if not result["available"]:

            return "Unknown"

        commits = result["total_commits"]

        contributors = len(result["contributors"])

        if commits >= 100 and contributors >= 5:

            return "Excellent"

        if commits >= 50:

            return "Good"

        if commits >= 10:

            return "Average"

        return "Small Project"