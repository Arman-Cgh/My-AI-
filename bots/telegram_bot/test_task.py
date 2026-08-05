from database.db import init_db
from services.tasks.manager import TaskManager


USER_ID = 123456


print("Initializing database...")

init_db()



print("\nCreating task...")

task_id = TaskManager.create(
    USER_ID,
    "تکمیل سیستم حافظه AetherAI",
    "بررسی و بهبود Memory Engine",
    "2026-08-02 10:00"
)


print(
    "Created Task ID:",
    task_id
)



print("\nReading tasks...")

tasks = TaskManager.get_all(
    USER_ID
)


for task in tasks:

    print(task)



print("\nCompleting task...")

TaskManager.complete(
    task_id,
    USER_ID
)



print("\nAfter complete:")

tasks = TaskManager.get_all(
    USER_ID
)


for task in tasks:

    print(task)