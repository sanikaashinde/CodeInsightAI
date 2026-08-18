from core.parser import load_project

files = load_project("sample_project")

print("=" * 50)

print("Files Found:", len(files))

for f in files:
    print(f["filename"], "-", f["language"], "-", f["lines"])