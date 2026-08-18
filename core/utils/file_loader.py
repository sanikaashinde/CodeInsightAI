from pathlib import Path
import zipfile
import shutil

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


class FileLoader:

    def save_uploaded_file(self, uploaded_file):
        save_path = UPLOAD_DIR / uploaded_file.name

        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        return save_path

    def extract_zip(self, zip_path):

        extract_folder = UPLOAD_DIR / zip_path.stem

        # Remove old extracted folder
        if extract_folder.exists():
            shutil.rmtree(extract_folder, ignore_errors=True)

        # Create fresh folder
        extract_folder.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(zip_path, "r") as zip_ref:

            for member in zip_ref.infolist():

                filename = member.filename

                # Ignore unwanted folders
                if (
                    filename.startswith(".git/")
                    or "/.git/" in filename
                    or filename.startswith("__MACOSX/")
                    or "/__pycache__/" in filename
                    or "/.venv/" in filename
                    or "/venv/" in filename
                    or "/node_modules/" in filename
                ):
                    continue

                try:
                    zip_ref.extract(member, extract_folder)
                except FileExistsError:
                    # Ignore duplicate directory entries
                    pass

        return extract_folder