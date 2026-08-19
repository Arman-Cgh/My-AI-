import re

from datetime import datetime, timedelta

from services.tasks.constants import (
    DATE_KEYWORDS,
    EMPTY_TITLE,
    PERSIAN_DIGITS,
    RELATIVE_HOUR_PATTERNS,
    RELATIVE_MINUTE_PATTERNS,
    TASK_REMOVE_WORDS,
)


class TaskParser:

    # ==========================
    # Normalize
    # ==========================

    @staticmethod
    def normalize_text(text: str) -> str:

        text = str(text or "")

        text = text.replace("ي", "ی")
        text = text.replace("ى", "ی")
        text = text.replace("ك", "ک")

        for source, target in PERSIAN_DIGITS.items():
            text = text.replace(source, target)

        text = re.sub(r"\s+", " ", text)

        return text.strip()

    # ==========================
    # Remove trigger
    # ==========================

    @staticmethod
    def remove_trigger(text: str) -> str:

        result = text.strip()

        for word in TASK_REMOVE_WORDS:

            pattern = rf"^{re.escape(word)}(?:\s+|$)"

            result = re.sub(
                pattern,
                "",
                result,
                count=1,
                flags=re.IGNORECASE,
            )

        return result.strip()

    # ==========================
    # Relative minutes
    # ==========================

    @staticmethod
    def parse_relative_minutes(
        text: str,
        now: datetime,
    ):

        for pattern in RELATIVE_MINUTE_PATTERNS:

            match = re.search(
                pattern,
                text,
                flags=re.IGNORECASE,
            )

            if not match:
                continue

            minutes = int(match.group(1))

            target = now + timedelta(
                minutes=minutes
            )

            cleaned = re.sub(
                pattern,
                "",
                text,
                count=1,
                flags=re.IGNORECASE,
            )

            return (
                target.strftime("%Y-%m-%d"),
                target.strftime("%H:%M"),
                cleaned,
            )

        return "", "", text

    # ==========================
    # Relative hours
    # ==========================

    @staticmethod
    def parse_relative_hours(
        text: str,
        now: datetime,
    ):

        for pattern in RELATIVE_HOUR_PATTERNS:

            match = re.search(
                pattern,
                text,
                flags=re.IGNORECASE,
            )

            if not match:
                continue

            hours = int(match.group(1))

            target = now + timedelta(
                hours=hours
            )

            cleaned = re.sub(
                pattern,
                "",
                text,
                count=1,
                flags=re.IGNORECASE,
            )

            return (
                target.strftime("%Y-%m-%d"),
                target.strftime("%H:%M"),
                cleaned,
            )

        return "", "", text

    # ==========================
    # Date
    # ==========================

    @staticmethod
    def parse_date(
        text: str,
        now: datetime,
    ):

        for keyword, days in DATE_KEYWORDS.items():

            if keyword not in text:
                continue

            target = now + timedelta(
                days=days
            )

            cleaned = text.replace(
                keyword,
                "",
                1,
            )

            return (
                target.strftime("%Y-%m-%d"),
                cleaned,
            )

        return "", text

    # ==========================
    # Time
    # ==========================

    @staticmethod
    def parse_time(
        text: str,
        now: datetime,
        existing_date: str,
    ):

        # --------------------------
        # HH:MM
        # --------------------------

        match = re.search(
            r"(?:ساعت\s*)?(\d{1,2}):(\d{2})",
            text,
            flags=re.IGNORECASE,
        )

        if match:

            hour = int(match.group(1))
            minute = int(match.group(2))

            if not (
                0 <= hour <= 23
                and
                0 <= minute <= 59
            ):

                return (
                    existing_date,
                    "",
                    text,
                )

            due_time = f"{hour:02d}:{minute:02d}"

            due_date = existing_date

            if not due_date:

                candidate = now.replace(
                    hour=hour,
                    minute=minute,
                    second=0,
                    microsecond=0,
                )

                if candidate < now:
                    candidate += timedelta(days=1)

                due_date = candidate.strftime(
                    "%Y-%m-%d"
                )

            cleaned = re.sub(
                re.escape(match.group(0)),
                "",
                text,
                count=1,
            )

            return (
                due_date,
                due_time,
                cleaned,
            )

        # --------------------------
        # ساعت HH
        # --------------------------

        match = re.search(
            r"ساعت\s+(\d{1,2})(?!\d)",
            text,
            flags=re.IGNORECASE,
        )

        if match:

            hour = int(match.group(1))

            if not 0 <= hour <= 23:
                return (
                    existing_date,
                    "",
                    text,
                )

            due_time = f"{hour:02d}:00"

            due_date = existing_date

            if not due_date:

                candidate = now.replace(
                    hour=hour,
                    minute=0,
                    second=0,
                    microsecond=0,
                )

                if candidate < now:
                    candidate += timedelta(days=1)

                due_date = candidate.strftime(
                    "%Y-%m-%d"
                )

            cleaned = re.sub(
                re.escape(match.group(0)),
                "",
                text,
                count=1,
            )

            return (
                due_date,
                due_time,
                cleaned,
            )

        return (
            existing_date,
            "",
            text,
        )

    # ==========================
    # Cleanup title
    # ==========================

    @staticmethod
    def cleanup_title(title: str) -> str:

        title = re.sub(
            r"\s+",
            " ",
            title,
        ).strip()

        title = re.sub(
            r"^(امروز|فردا|پس فردا)\s+",
            "",
            title,
            flags=re.IGNORECASE,
        )

        title = re.sub(
            r"^(ساعت)\s*$",
            "",
            title,
            flags=re.IGNORECASE,
        )

        title = re.sub(
            r"\s+",
            " ",
            title,
        ).strip()

        return title or EMPTY_TITLE

    # ==========================
    # Parse
    # ==========================

    @classmethod
    def parse(
        cls,
        message: str,
    ):

        now = datetime.now()

        text = cls.normalize_text(
            message
        )

        text = cls.remove_trigger(
            text
        )

        title = text

        due_date = ""
        due_time = ""

        # ==========================
        # Relative minutes
        # ==========================

        (
            relative_date,
            relative_time,
            title,
        ) = cls.parse_relative_minutes(
            title,
            now,
        )

        if relative_date:

            due_date = relative_date
            due_time = relative_time

        # ==========================
        # Relative hours
        # ==========================

        if not due_date:

            (
                relative_date,
                relative_time,
                title,
            ) = cls.parse_relative_hours(
                title,
                now,
            )

            if relative_date:

                due_date = relative_date
                due_time = relative_time

        # ==========================
        # Explicit date
        # ==========================

        if not due_date:

            due_date, title = cls.parse_date(
                title,
                now,
            )

        # ==========================
        # Explicit time
        # ==========================

        (
            due_date,
            parsed_time,
            title,
        ) = cls.parse_time(
            title,
            now,
            due_date,
        )

        if parsed_time:
            due_time = parsed_time

        # ==========================
        # Final title
        # ==========================

        title = cls.cleanup_title(
            title
        )

        return {
            "title": title,
            "due_date": due_date,
            "due_time": due_time,
        }