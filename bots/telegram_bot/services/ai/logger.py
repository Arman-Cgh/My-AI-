from datetime import datetime


class AILogger:


    @staticmethod
    def log(
        level,
        message
    ):

        time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        print(
            f"[{time}] [{level}] {message}"
        )


    @staticmethod
    def info(message):

        AILogger.log(
            "INFO",
            message
        )


    @staticmethod
    def error(message):

        AILogger.log(
            "ERROR",
            message
        )


    @staticmethod
    def warning(message):

        AILogger.log(
            "WARNING",
            message
        )