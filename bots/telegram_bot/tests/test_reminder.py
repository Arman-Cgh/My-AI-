from datetime import datetime, timedelta

import pytest

from database.db import add_user, init_db
from services.tasks.manager import TaskManager
from services.tasks.reminder import ReminderEngine


@pytest.fixture
def test_user():

    init_db()

    user_id = 888888

    add_user(
        user_id=user_id,
        username="reminder_test_user",
        first_name="Reminder Test",
    )

    return user_id



def test_due_task_detection(test_user):

    past_time = (
        datetime.now() - timedelta(minutes=5)
    ).strftime(
        "%Y-%m-%d %H:%M"
    )

    task_id = TaskManager.create(
        user_id=test_user,
        title="Reminder Test",
        description="",
        due_date=past_time,
    )

    tasks = ReminderEngine.get_due_tasks(
        test_user
    )

    ids = [
        task["id"]
        for task in tasks
    ]

    assert task_id in ids



def test_future_task_not_due(test_user):

    future_time = (
        datetime.now() + timedelta(hours=5)
    ).strftime(
        "%Y-%m-%d %H:%M"
    )

    task_id = TaskManager.create(
        user_id=test_user,
        title="Future Reminder Test",
        description="",
        due_date=future_time,
    )

    tasks = ReminderEngine.get_due_tasks(
        test_user
    )

    ids = [
        task["id"]
        for task in tasks
    ]

    assert task_id not in ids



def test_task_without_date_not_due(test_user):

    task_id = TaskManager.create(
        user_id=test_user,
        title="No Date Task",
        description="",
        due_date="",
    )

    tasks = ReminderEngine.get_due_tasks(
        test_user
    )

    ids = [
        task["id"]
        for task in tasks
    ]

    assert task_id not in ids