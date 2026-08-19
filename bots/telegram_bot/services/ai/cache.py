import hashlib

from datetime import datetime, timedelta

from database.db import (
    get_connection,
    save_cached_answer,
)


class AICache:

    PROMPT_VERSION = "1"

    DEFAULT_TTL_SECONDS = (
        60 * 60 * 24
    )


    BYPASS_INTENTS = (
        "task",
        "memory",
    )


    CHAT_BYPASS_PATTERNS = (

        "continue",
        "continue please",
        "explain more",
        "another example",
        "what do you mean",
        "what did we discuss",
        "what is my name",
        "do you remember",
        "remember",
        "save this",
        "today",
        "tomorrow",
        "profile",
        "memory",
        "history",
        "state",
        "task",
        "my project",
        "current goal",
        "who am i",

        "یادم بنداز",
        "یادم بیار",
        "یادت باشه",
        "ذخیره کن",
        "یادت هست",
        "یادته",
        "چی گفتیم",
        "ادامه بده",
        "بیشتر توضیح بده",
        "مثال دیگه",
        "اسمم چیه",
        "من کی هستم",
        "منو میشناسی",
        "درباره من",
        "حافظه من",
        "پروژه من",
        "هدف من",
        "امروز",
        "دیروز",
        "فردا",
        "الان",
    )


    def __init__(
        self,
        prompt_version=None,
        default_ttl=None,
    ):

        self.prompt_version = (
            prompt_version
            or self.PROMPT_VERSION
        )


        self.default_ttl = (
            default_ttl
            if default_ttl is not None
            else self.DEFAULT_TTL_SECONDS
        )


    @staticmethod
    def _normalize_text(
        text
    ):

        text = str(
            text or ""
        )


        text = (
            text
            .replace("ي", "ی")
            .replace("ى", "ی")
            .replace("ك", "ک")
        )


        return (
            " ".join(
                text
                .strip()
                .lower()
                .split()
            )
        )


    @staticmethod
    def _expires_at(
        ttl
    ):

        if ttl is None:

            return ""


        try:

            ttl = int(ttl)

        except Exception:

            return ""


        if ttl <= 0:

            return ""


        return (
            datetime.now()
            +
            timedelta(
                seconds=ttl
            )
        ).isoformat()



    def generate_key(
        self,
        user_message,
        intent,
        model,
        prompt_version=None,
        provider="",
    ):

        message = (
            self._normalize_text(
                user_message
            )
        )


        version = (
            prompt_version
            or self.prompt_version
        )


        raw = (
            f"{version}|"
            f"{provider}|"
            f"{intent}|"
            f"{model}|"
            f"{message}"
        )


        return hashlib.sha256(
            raw.encode("utf-8")
        ).hexdigest()



    def is_cacheable(
        self,
        intent,
        user_message,
    ):

        message = (
            self._normalize_text(
                user_message
            )
        )


        if not message:

            return False


        if intent in self.BYPASS_INTENTS:

            return False


        if intent == "code":

            return True


        if intent != "chat":

            return False



        for pattern in self.CHAT_BYPASS_PATTERNS:

            if (
                self._normalize_text(pattern)
                in message
            ):

                return False


        return True



    async def get(
        self,
        user_id,
        cache_key,
    ):

        if not cache_key:

            return None


        conn = get_connection()


        try:

            cursor = conn.cursor()


            cursor.execute(
                """
                SELECT
                    answer,
                    expires_at

                FROM qa_cache

                WHERE user_id=?

                AND normalized_question=?

                LIMIT 1
                """,
                (
                    user_id,
                    cache_key,
                ),
            )


            row = cursor.fetchone()


            if not row:

                return None


            answer = row[0]

            expires_at = (
                row[1]
                or ""
            )


            if expires_at:

                try:

                    expire_time = (
                        datetime.fromisoformat(
                            expires_at
                        )
                    )


                    if datetime.now() >= expire_time:

                        cursor.execute(
                            """
                            DELETE FROM qa_cache

                            WHERE user_id=?

                            AND normalized_question=?
                            """,
                            (
                                user_id,
                                cache_key,
                            ),
                        )


                        conn.commit()


                        return None


                except Exception:

                    return None



            return answer


        finally:

            conn.close()



    async def set(
        self,
        user_id,
        cache_key,
        value,
        ttl=None,
        provider="",
        model="",
        prompt_version=None,
    ):

        if not cache_key:

            return


        if value is None:

            return


        version = (
            prompt_version
            or self.prompt_version
        )


        expires_at = self._expires_at(
            self.default_ttl
            if ttl is None
            else ttl
        )


        save_cached_answer(
            user_id=user_id,
            question=cache_key,
            answer=value,
            prompt_version=version,
            provider=provider,
            model=model,
            expires_at=expires_at,
        )



    async def delete(
        self,
        user_id,
        cache_key,
    ):

        if not cache_key:

            return


        conn = get_connection()


        try:

            cursor = conn.cursor()


            cursor.execute(
                """
                DELETE FROM qa_cache

                WHERE user_id=?

                AND normalized_question=?
                """,
                (
                    user_id,
                    cache_key,
                ),
            )


            conn.commit()


        finally:

            conn.close()



    async def clear_user(
        self,
        user_id,
    ):

        conn = get_connection()


        try:

            cursor = conn.cursor()


            cursor.execute(
                """
                DELETE FROM qa_cache

                WHERE user_id=?
                """,
                (
                    user_id,
                ),
            )


            conn.commit()


        finally:

            conn.close()



    async def cleanup_expired(
        self
    ):

        now = (
            datetime.now()
            .isoformat()
        )


        conn = get_connection()


        try:

            cursor = conn.cursor()


            cursor.execute(
                """
                DELETE FROM qa_cache

                WHERE expires_at != ''

                AND expires_at <= ?
                """,
                (
                    now,
                ),
            )


            deleted = (
                cursor.rowcount
            )


            conn.commit()


            return deleted


        finally:

            conn.close()



    async def count(
        self,
        user_id=None,
    ):

        conn = get_connection()


        try:

            cursor = conn.cursor()


            if user_id is None:

                cursor.execute(
                    """
                    SELECT COUNT(*)

                    FROM qa_cache
                    """
                )

            else:

                cursor.execute(
                    """
                    SELECT COUNT(*)

                    FROM qa_cache

                    WHERE user_id=?
                    """,
                    (
                        user_id,
                    ),
                )


            row = cursor.fetchone()


            return (
                row[0]
                if row
                else 0
            )


        finally:

            conn.close()