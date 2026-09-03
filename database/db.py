import sqlite3
import os


# ==============================
# DATABASE PATH
# ==============================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DB_PATH = os.path.join(
    BASE_DIR,
    "database",
    "interview.db"
)


# ==============================
# GET DATABASE CONNECTION
# ==============================

def get_connection():

    return sqlite3.connect(DB_PATH)


# ==============================
# CREATE TABLE
# ==============================

def create_table():

    conn = get_connection()

    cursor = conn.cursor()

    # ==============================
    # INTERVIEWS TABLE
    # ==============================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interviews (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            candidate_name TEXT,

            role TEXT,

            experience TEXT,

            difficulty TEXT,

            answer_score REAL,

            vision_score REAL,

            ml_score REAL,

            eye_contact REAL,

            posture REAL,

            resume_match REAL,

            interview_date TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ==============================
    # USERS TABLE
    # ==============================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL,

            created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ==============================
    # UPDATE OLD DATABASE
    # ==============================

    cursor.execute(
        "PRAGMA table_info(interviews)"
    )

    columns = [
        column[1]
        for column in cursor.fetchall()
    ]

    if "user_id" not in columns:

        cursor.execute("""
            ALTER TABLE interviews
            ADD COLUMN user_id INTEGER
        """)

    conn.commit()

    conn.close()


# ==============================
# SAVE INTERVIEW
# ==============================

def save_interview(
    user_id,
    candidate_name,
    role,
    experience,
    difficulty,
    answer_score,
    vision_score,
    ml_score,
    eye_contact,
    posture,
    resume_match
):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO interviews (

            user_id,
            candidate_name,
            role,
            experience,
            difficulty,
            answer_score,
            vision_score,
            ml_score,
            eye_contact,
            posture,
            resume_match

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        user_id,
        candidate_name,
        role,
        experience,
        difficulty,
        answer_score,
        vision_score,
        ml_score,
        eye_contact,
        posture,
        resume_match

    ))

    conn.commit()

    conn.close()


# ==============================
# GET INTERVIEW HISTORY
# ==============================

def get_interview_history(user_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            candidate_name,
            role,
            experience,
            difficulty,
            answer_score,
            vision_score,
            ml_score,
            eye_contact,
            posture,
            resume_match,
            interview_date

        FROM interviews

        WHERE user_id = ?

        ORDER BY id DESC
    """, (user_id,))

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==============================
# REGISTER USER
# ==============================

def register_user(name, email, password):

    conn = get_connection()

    cursor = conn.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO users (
                name,
                email,
                password
            )

            VALUES (?, ?, ?)
            """,
            (
                name,
                email,
                password
            )
        )

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


# ==============================
# LOGIN USER
# ==============================

def login_user(email, password):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            name,
            email

        FROM users

        WHERE email = ?
        AND password = ?
        """,
        (
            email,
            password
        )
    )

    user = cursor.fetchone()

    conn.close()

    return user


# ==============================
# INITIALIZE DATABASE
# ==============================

create_table()