def repository_metrics(project_files):

    total_files = len(project_files)

    total_lines = sum(
        f["lines"]
        for f in project_files
    )

    languages = {}

    for file in project_files:

        lang = file["language"]

        languages[lang] = languages.get(lang, 0) + 1

    return {
        "files": total_files,
        "lines": total_lines,
        "languages": languages,
    }