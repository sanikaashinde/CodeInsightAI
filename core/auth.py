import sqlite3
import hashlib
import secrets
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "data"
DB_DIR.mkdir(exist_ok=True)

DB_PATH = DB_DIR / "codeinsight.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_auth_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            analysis_type TEXT,
            name TEXT,
            time TEXT,
            quality_score REAL,
            security_score REAL,
            complexity REAL,
            functions INTEGER,
            classes INTEGER,
            code_smells INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def hash_password(password):
    salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        120000,
    ).hex()

    return f"{salt}${password_hash}"


def verify_password(password, stored_password):
    try:
        salt, stored_hash = stored_password.split("$")

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            120000,
        ).hex()

        return secrets.compare_digest(
            password_hash,
            stored_hash,
        )

    except (ValueError, AttributeError):
        return False


def register_user(full_name, email, username, password):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO users
            (full_name, email, username, password_hash)
            VALUES (?, ?, ?, ?)
            """,
            (
                full_name.strip(),
                email.strip().lower(),
                username.strip(),
                hash_password(password),
            ),
        )

        conn.commit()

        return True, "Account created successfully."

    except sqlite3.IntegrityError as error:

        if "email" in str(error).lower():
            return False, "Email already registered."

        if "username" in str(error).lower():
            return False, "Username already exists."

        return False, "Unable to create account."

    finally:
        conn.close()


def login_user(identifier, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, full_name, email, username, password_hash
        FROM users
        WHERE lower(email) = lower(?)
           OR lower(username) = lower(?)
        """,
        (
            identifier.strip(),
            identifier.strip(),
        ),
    )

    user = cursor.fetchone()
    conn.close()

    if user is None:
        return None

    if not verify_password(password, user[4]):
        return None

    return {
        "id": user[0],
        "full_name": user[1],
        "email": user[2],
        "username": user[3],
    }


def save_analysis_history(
    user_id,
    analysis_type,
    name,
    quality_score=None,
    security_score=None,
    complexity=None,
    functions=None,
    classes=None,
    code_smells=None,
    time=None,
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO analysis_history (
            user_id,
            analysis_type,
            name,
            time,
            quality_score,
            security_score,
            complexity,
            functions,
            classes,
            code_smells
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            analysis_type,
            name,
            time,
            quality_score,
            security_score,
            complexity,
            functions,
            classes,
            code_smells,
        ),
    )

    cursor.execute(
        """
        DELETE FROM analysis_history
        WHERE user_id = ?
        AND id NOT IN (
            SELECT id
            FROM analysis_history
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT 20
        )
        """,
        (user_id, user_id),
    )

    conn.commit()
    conn.close()


def get_analysis_history(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            time,
            analysis_type,
            name,
            quality_score,
            security_score,
            complexity,
            functions,
            classes,
            code_smells
        FROM analysis_history
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT 20
        """,
        (user_id,),
    )

    rows = cursor.fetchall()
    conn.close()

    history = []

    for row in rows:
        history.append({
            "time": row[0],
            "type": row[1],
            "name": row[2],
            "quality_score": row[3],
            "security_score": row[4],
            "complexity": row[5],
            "functions": row[6],
            "classes": row[7],
            "code_smells": row[8],
        })

    return history


def clear_analysis_history(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM analysis_history WHERE user_id = ?",
        (user_id,),
    )

    conn.commit()
    conn.close()
