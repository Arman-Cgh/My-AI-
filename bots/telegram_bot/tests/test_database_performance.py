import os
import sqlite3
import tempfile


def main():

    fd, db_path = tempfile.mkstemp(
        suffix=".db"
    )

    os.close(fd)

    try:

        conn = sqlite3.connect(
            db_path
        )

        cursor = conn.cursor()

        cursor.execute(
            "PRAGMA foreign_keys=ON"
        )

        cursor.executescript(
            """
            CREATE TABLE users(
                id INTEGER PRIMARY KEY
            );

            CREATE TABLE memory(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                memory_key TEXT NOT NULL,
                memory_value TEXT NOT NULL DEFAULT '',
                UNIQUE(user_id, memory_key),
                FOREIGN KEY(user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE
            );

            CREATE INDEX idx_memory_user_id
            ON memory(user_id);

            CREATE TABLE messages(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT '',
                FOREIGN KEY(user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE
            );

            CREATE INDEX idx_messages_user_id
            ON messages(user_id);

            CREATE TABLE tasks(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT '',
                FOREIGN KEY(user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE
            );

            CREATE INDEX idx_tasks_user_id
            ON tasks(user_id);

            CREATE TABLE usage(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                messages INTEGER NOT NULL DEFAULT 0,
                UNIQUE(user_id, date),
                FOREIGN KEY(user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE
            );

            CREATE TABLE qa_cache(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                normalized_question TEXT NOT NULL,
                prompt_version TEXT NOT NULL,
                provider TEXT NOT NULL,
                model TEXT NOT NULL,
                answer TEXT NOT NULL,
                UNIQUE(
                    user_id,
                    normalized_question,
                    prompt_version,
                    provider,
                    model
                ),
                FOREIGN KEY(user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE
            );
            """
        )

        # ------------------------------------------------
        # Users
        # ------------------------------------------------

        users = [
            (user_id,)
            for user_id in range(1, 101)
        ]

        cursor.executemany(
            "INSERT INTO users(id) VALUES(?)",
            users
        )

        # ------------------------------------------------
        # Memory
        # ------------------------------------------------

        memory_rows = []

        for user_id in range(1, 101):

            for index in range(100):

                memory_rows.append(
                    (
                        user_id,
                        f"key_{index}",
                        f"value_{user_id}_{index}"
                    )
                )

        cursor.executemany(
            """
            INSERT INTO memory
            (
                user_id,
                memory_key,
                memory_value
            )
            VALUES(?,?,?)
            """,
            memory_rows
        )

        # ------------------------------------------------
        # Messages
        # ------------------------------------------------

        message_rows = []

        for user_id in range(1, 101):

            for index in range(100):

                message_rows.append(
                    (
                        user_id,
                        "user",
                        f"message_{index}",
                        ""
                    )
                )

        cursor.executemany(
            """
            INSERT INTO messages
            (
                user_id,
                role,
                message,
                created_at
            )
            VALUES(?,?,?,?)
            """,
            message_rows
        )

        # ------------------------------------------------
        # Tasks
        # ------------------------------------------------

        task_rows = []

        for user_id in range(1, 101):

            for index in range(100):

                task_rows.append(
                    (
                        user_id,
                        f"task_{index}",
                        ""
                    )
                )

        cursor.executemany(
            """
            INSERT INTO tasks
            (
                user_id,
                title,
                created_at
            )
            VALUES(?,?,?)
            """,
            task_rows
        )

        # ------------------------------------------------
        # Usage
        # ------------------------------------------------

        usage_rows = []

        for user_id in range(1, 101):

            for day in range(30):

                usage_rows.append(
                    (
                        user_id,
                        f"2026-08-{day + 1:02d}",
                        day
                    )
                )

        cursor.executemany(
            """
            INSERT INTO usage
            (
                user_id,
                date,
                messages
            )
            VALUES(?,?,?)
            """,
            usage_rows
        )

        # ------------------------------------------------
        # Cache
        # ------------------------------------------------

        cache_rows = []

        for user_id in range(1, 101):

            for index in range(100):

                cache_rows.append(
                    (
                        user_id,
                        f"question_{index}",
                        "1",
                        "openrouter",
                        "test-model",
                        f"answer_{index}"
                    )
                )

        cursor.executemany(
            """
            INSERT INTO qa_cache
            (
                user_id,
                normalized_question,
                prompt_version,
                provider,
                model,
                answer
            )
            VALUES(?,?,?,?,?,?)
            """,
            cache_rows
        )

        conn.commit()

        # ------------------------------------------------
        # Statistics
        # ------------------------------------------------

        print(
            "DATASET CREATED"
        )

        for table in (
            "users",
            "memory",
            "messages",
            "tasks",
            "usage",
            "qa_cache"
        ):

            cursor.execute(
                f"SELECT COUNT(*) FROM {table}"
            )

            print(
                f"{table}:",
                cursor.fetchone()[0]
            )

        # ------------------------------------------------
        # Query Plans
        # ------------------------------------------------

        queries = {

            "MEMORY":
                """
                SELECT memory_key, memory_value
                FROM memory
                WHERE user_id=?
                """,

            "MESSAGES":
                """
                SELECT role, message
                FROM messages
                WHERE user_id=?
                ORDER BY id DESC
                LIMIT 10
                """,

            "TASKS":
                """
                SELECT id, title
                FROM tasks
                WHERE user_id=?
                ORDER BY id DESC
                LIMIT 20
                """,

            "USAGE":
                """
                SELECT messages
                FROM usage
                WHERE user_id=?
                AND date=?
                """,

            "CACHE":
                """
                SELECT answer
                FROM qa_cache
                WHERE user_id=?
                AND normalized_question=?
                AND prompt_version=?
                AND provider=?
                AND model=?
                LIMIT 1
                """
        }

        params = {

            "MEMORY":
                (50,),

            "MESSAGES":
                (50,),

            "TASKS":
                (50,),

            "USAGE":
                (50, "2026-08-17"),

            "CACHE":
                (
                    50,
                    "question_50",
                    "1",
                    "openrouter",
                    "test-model"
                )
        }

        print(
            "\nQUERY PLANS"
        )

        for name, sql in queries.items():

            cursor.execute(
                "EXPLAIN QUERY PLAN " + sql,
                params[name]
            )

            print(
                f"\n{name}:"
            )

            for row in cursor.fetchall():

                print(
                    row
                )

        # ------------------------------------------------
        # Analyze
        # ------------------------------------------------

        cursor.execute(
            "ANALYZE"
        )

        conn.commit()

        print(
            "\nQUERY PLANS AFTER ANALYZE"
        )

        for name, sql in queries.items():

            cursor.execute(
                "EXPLAIN QUERY PLAN " + sql,
                params[name]
            )

            print(
                f"\n{name}:"
            )

            for row in cursor.fetchall():

                print(
                    row
                )

        conn.close()

        print(
            "\nPERFORMANCE TEST PASSED"
        )

    finally:

        if os.path.exists(
            db_path
        ):
            os.remove(
                db_path
            )


if __name__ == "__main__":
    main()