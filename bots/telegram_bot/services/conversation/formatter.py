from datetime import datetime


class ConversationFormatter:


    MAX_MESSAGE_LENGTH = 4000



    def clean_text(
        self,
        text: str
    ):

        if not text:
            return ""


        text = str(text)

        text = text.strip()


        return text



    def limit_length(
        self,
        text: str
    ):

        if len(text) <= self.MAX_MESSAGE_LENGTH:
            return text


        return (
            text[:self.MAX_MESSAGE_LENGTH]
            +
            "\n...[truncated]"
        )



    def format_message(
        self,
        role: str,
        content: str
    ):

        content = self.clean_text(
            content
        )


        content = self.limit_length(
            content
        )


        return {

            "role": role,

            "content": content,

            "time": datetime.now().isoformat()

        }



    def format_history(
        self,
        messages
    ):

        result = []


        for message in messages:

            result.append(
                {
                    "role": message.get(
                        "role",
                        ""
                    ),

                    "content": self.limit_length(
                        message.get(
                            "content",
                            ""
                        )
                    ),

                    "time": message.get(
                        "time",
                        ""
                    )
                }
            )


        return result