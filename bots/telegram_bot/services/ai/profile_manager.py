from database.db import (
    get_profile,
    update_profile
)


class ProfileManager:


    @staticmethod
    def get(
        user_id: int
    ):

        profile = get_profile(
            user_id
        )

        return profile or {}



    @staticmethod
    def update(
        user_id: int,
        data: dict
    ):

        if not data:
            return



        nickname = data.get(
            "name"
        )


        bio = data.get(
            "job"
        )


        interests = data.get(
            "interests"
        )


        if isinstance(
            interests,
            list
        ):

            interests = ", ".join(
                map(
                    str,
                    interests
                )
            )



        update_profile(
            user_id,
            nickname=nickname,
            bio=bio,
            interests=interests
        )