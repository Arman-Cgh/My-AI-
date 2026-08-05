from database.db import init_db, get_memories, get_state
from services.ai.memory_manager import MemoryManager
from services.ai.state_manager import StateManager


USER_ID = 555555


def main():

    init_db()


    MemoryManager.update(
        USER_ID,
        {
            "name": "یونس",
            "projects": "AetherAI"
        }
    )


    StateManager.update(
        USER_ID,
        {
            "active_project": "AetherAI",
            "current_goal": "ساخت دستیار هوشمند شخصی"
        }
    )


    print("MEMORY:")
    print(get_memories(USER_ID))


    print("\nSTATE:")
    print(get_state(USER_ID))


if __name__ == "__main__":
    main()