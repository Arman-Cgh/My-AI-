from database.db import update_profile


def sync_profile(
    user_id: int,
    memory_data: dict
):

    nickname = memory_data.get(
        "name"
    )

    bio = memory_data.get(
        "job"
    )

    interests = memory_data.get(
        "interests"
    )


    if isinstance(interests, list):

        interests = ", ".join(
            interests
        )


    update_profile(
        user_id,
        nickname=nickname,
        bio=bio,
        interests=interests
    )