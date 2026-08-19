from database.db import (
    get_connection,
    add_user,
)


TEST_USER_ID = 777777


def run_test(
    name,
    callback,
    should_fail=False
):
    try:
        callback()

        if should_fail:
            print(
                f"{name}: FAILED - duplicate was allowed"
            )
        else:
            print(
                f"{name}: OK"
            )

    except Exception as exc:

        if should_fail:
            print(
                f"{name}: BLOCKED - "
                f"{type(exc).__name__}"
            )
        else:
            print(
                f"{name}: FAILED - "
                f"{type(exc).__name__}: {exc}"
            )


def main():

    add_user(
        TEST_USER_ID,
        "constraint_test",
        "Constraint"
    )

    conn = get_connection()
    cursor = conn.cursor()

    try:

        # ==================================================
        # Memory UNIQUE(user_id, memory_key)
        # ==================================================

        cursor.execute(
            """
            INSERT INTO memory
            (
                user_id,
                memory_key,
                memory_value
            )
            VALUES
            (
                ?,
                ?,
                ?
            )
            """,
            (
                TEST_USER_ID,
                "same_key",
                "one"
            )
        )

        conn.commit()

        print("MEMORY FIRST INSERT: OK")

        run_test(
            "MEMORY DUPLICATE",
            lambda: cursor.execute(
                """
                INSERT INTO memory
                (
                    user_id,
                    memory_key,
                    memory_value
                )
                VALUES
                (
                    ?,
                    ?,
                    ?
                )
                """,
                (
                    TEST_USER_ID,
                    "same_key",
                    "two"
                )
            ),
            should_fail=True
        )

        conn.rollback()

        # ==================================================
        # Usage UNIQUE(user_id, date)
        # ==================================================

        cursor.execute(
            """
            INSERT INTO usage
            (
                user_id,
                date,
                messages
            )
            VALUES
            (
                ?,
                ?,
                ?
            )
            """,
            (
                TEST_USER_ID,
                "2026-08-17",
                1
            )
        )

        conn.commit()

        print("USAGE FIRST INSERT: OK")

        run_test(
            "USAGE DUPLICATE",
            lambda: cursor.execute(
                """
                INSERT INTO usage
                (
                    user_id,
                    date,
                    messages
                )
                VALUES
                (
                    ?,
                    ?,
                    ?
                )
                """,
                (
                    TEST_USER_ID,
                    "2026-08-17",
                    2
                )
            ),
            should_fail=True
        )

        conn.rollback()

        # ==================================================
        # Subscriptions UNIQUE(user_id)
        # ==================================================

        cursor.execute(
            """
            INSERT INTO subscriptions
            (
                user_id,
                plan,
                start_date,
                duration_days,
                status
            )
            VALUES
            (
                ?,
                ?,
                ?,
                ?,
                ?
            )
            """,
            (
                TEST_USER_ID,
                "pro",
                "2026-08-17",
                30,
                "active"
            )
        )

        conn.commit()

        print(
            "SUBSCRIPTION FIRST INSERT: OK"
        )

        run_test(
            "SUBSCRIPTION DUPLICATE",
            lambda: cursor.execute(
                """
                INSERT INTO subscriptions
                (
                    user_id,
                    plan,
                    start_date,
                    duration_days,
                    status
                )
                VALUES
                (
                    ?,
                    ?,
                    ?,
                    ?,
                    ?
                )
                """,
                (
                    TEST_USER_ID,
                    "ultra",
                    "2026-08-17",
                    30,
                    "active"
                )
            ),
            should_fail=True
        )

        conn.rollback()

    finally:

        cursor.execute(
            """
            DELETE FROM users
            WHERE id=?
            """,
            (
                TEST_USER_ID,
            )
        )

        conn.commit()
        conn.close()

        print(
            "TEST USER CLEANED"
        )


if __name__ == "__main__":

    main()