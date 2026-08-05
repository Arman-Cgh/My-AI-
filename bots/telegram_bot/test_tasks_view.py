from database.db import init_db
from services.tasks.manager import TaskManager


init_db()


print(
    TaskManager.get_all(1)
)