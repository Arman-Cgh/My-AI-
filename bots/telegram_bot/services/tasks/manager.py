from datetime import datetime

from database.db import get_connection



class TaskManager:


    @staticmethod
    def create(
        user_id: int,
        title: str,
        description: str = "",
        due_date: str = ""
    ):

        title = (title or "").strip()


        if not title:
            raise ValueError(
                "Task title cannot be empty"
            )


        conn = get_connection()
        cursor = conn.cursor()


        cursor.execute(
            """
            INSERT INTO tasks
            (
                user_id,
                title,
                description,
                due_date,
                status,
                created_at
            )

            VALUES(?,?,?,?,?,?)
            """,
            (
                user_id,
                title,
                description or "",
                due_date or "",
                "pending",
                datetime.now().isoformat()
            )
        )


        task_id = cursor.lastrowid


        conn.commit()
        conn.close()


        return task_id



    @staticmethod
    def get_all(
        user_id:int
    ):

        conn = get_connection()
        cursor = conn.cursor()


        cursor.execute(
            """
            SELECT
                id,
                title,
                description,
                due_date,
                status,
                created_at

            FROM tasks

            WHERE user_id=?

            ORDER BY id DESC
            """,
            (
                user_id,
            )
        )


        rows = cursor.fetchall()

        conn.close()



        return [

            {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "due_date": row[3],
                "status": row[4],
                "created_at": row[5],
            }

            for row in rows

        ]



    @staticmethod
    def get_pending(
        user_id:int
    ):


        conn = get_connection()
        cursor = conn.cursor()


        cursor.execute(
            """
            SELECT
                id,
                title,
                description,
                due_date,
                status,
                created_at

            FROM tasks

            WHERE user_id=?

            AND status='pending'

            ORDER BY id DESC
            """,
            (
                user_id,
            )
        )


        rows = cursor.fetchall()

        conn.close()


        return [

            {
                "id": row[0],
                "title": row[1],
                "description": row[2],
                "due_date": row[3],
                "status": row[4],
                "created_at": row[5],
            }

            for row in rows

        ]



    @staticmethod
    def complete(
        task_id:int,
        user_id:int
    ):


        conn = get_connection()
        cursor = conn.cursor()


        cursor.execute(
            """
            UPDATE tasks

            SET status='done'

            WHERE id=?

            AND user_id=?
            """,
            (
                task_id,
                user_id
            )
        )


        updated = cursor.rowcount


        conn.commit()
        conn.close()


        return updated > 0



    @staticmethod
    def delete(
        task_id:int,
        user_id:int
    ):


        conn = get_connection()
        cursor = conn.cursor()


        cursor.execute(
            """
            DELETE FROM tasks

            WHERE id=?

            AND user_id=?
            """,
            (
                task_id,
                user_id
            )
        )


        deleted = cursor.rowcount


        conn.commit()
        conn.close()


        return deleted > 0