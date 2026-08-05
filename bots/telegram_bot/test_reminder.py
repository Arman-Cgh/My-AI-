from database.db import init_db
from services.reminders.engine import ReminderEngine


init_db()


tasks = ReminderEngine.get_due_tasks(
    5383969883
)


print(tasks)