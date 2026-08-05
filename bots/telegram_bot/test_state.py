from database.db import init_db, get_state
from services.ai.state_manager import StateManager


USER_ID = 777777


def main():

    init_db()


    StateManager.update(
        USER_ID,
        {
            "active_project": "AetherAI",
            "current_goal": "ساخت دستیار هوشمند شخصی",
            "preferences": {
                "language": "fa"
            }
        }
    )


    result = get_state(
        USER_ID
    )


    print(result)


if __name__ == "__main__":
    main()