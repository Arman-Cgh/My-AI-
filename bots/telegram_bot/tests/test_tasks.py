import pytest

from database.db import add_user, init_db
from services.tasks.service import TaskService


@pytest.fixture
def test_user():

    init_db()

    user_id = 999999

    add_user(
        user_id=user_id,
        username="task_test_user",
        first_name="Task Test",
    )

    return user_id



def create_test_task(user_id):

    return TaskService.create(
        user_id=user_id,
        message="فردا ساعت 10 یادم بنداز تست انجام شود",
    )



def test_create_task(test_user):

    result = create_test_task(
        test_user
    )

    assert result is not None
    assert result.get("title")



def test_get_pending_tasks(test_user):

    create_test_task(
        test_user
    )

    tasks = TaskService.get_pending(
        test_user
    )

    assert tasks is not None
    assert len(tasks) > 0



def test_complete_task(test_user):

    result = create_test_task(
        test_user
    )

    task_id = result.get(
        "id"
    )

    completed = TaskService.complete(
        task_id=task_id,
        user_id=test_user,
    )

    assert completed is True

    tasks = TaskService.get_pending(
        test_user
    )

    assert all(
        task["id"] != task_id
        for task in tasks
    )



def test_delete_task(test_user):

    result = create_test_task(
        test_user
    )

    task_id = result.get(
        "id"
    )

    deleted = TaskService.delete(
        task_id=task_id,
        user_id=test_user,
    )

    assert deleted is True

    tasks = TaskService.get_all(
        test_user
    )

    assert all(
        task["id"] != task_id
        for task in tasks
    )



def test_invalid_task(test_user):

    with pytest.raises(ValueError):

        TaskService.create(
            user_id=test_user,
            message="",
        )