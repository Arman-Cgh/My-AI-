from services.ai.memory_manager import MemoryManager
from database.db import get_memories, init_db


USER_ID = 999999


def main():

    print("Initializing database...")
    init_db()


    print("\nSaving memory...")

    MemoryManager.update(
        USER_ID,
        {
            "name": "یونس",
            "projects": "AetherAI",
            "goal": "ساخت یک دستیار هوشمند شخصی",
            "interests": "پایتون, برنامه نویسی"
        }
    )


    print("\nReading memory...")

    memories = get_memories(USER_ID)


    for item in memories:
        print(item)


if __name__ == "__main__":
    main()