from database.db import init_db
from services.tasks.service import TaskService



init_db()



user_id = 1



result = TaskService.handle(
    user_id,
    "یادم بنداز فردا پروژه AetherAI رو بررسی کنم"
)



print(
    "CREATE:",
    result
)



print(
    "\nPENDING:"
)


print(
    TaskService.get_pending(
        user_id
    )
)



print(
    "\nDUE:"
)


print(
    TaskService.get_due(
        user_id
    )
)