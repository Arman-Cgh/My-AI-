from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from services.tasks.manager import TaskManager


class ReminderEngine:
    """
    موتور یادآوری پیشرفته با پشتیبانی از انواع فرمت‌های دیتا
    """

    @staticmethod
    def get_due_tasks(user_id: int) -> List[Dict[str, Any]]:
        """
        دریافت لیست تسک‌های سررسید شده

        Args:
            user_id: شناسه کاربر

        Returns:
            List[Dict]: لیست تسک‌های معوق
        """
        try:
            tasks = TaskManager.get_all(user_id)
            today = datetime.now().date()
            due_tasks = []

            if not tasks:
                return []

            for task in tasks:
                try:
                    # پردازش دیکشنری
                    if isinstance(task, dict):
                        if task.get("status") != "pending":
                            continue

                        due_date = task.get("due_date")
                        if not due_date:
                            continue

                        task_date = ReminderEngine._parse_date(due_date)
                        if not task_date:
                            continue

                        if task_date <= today:
                            due_tasks.append({
                                "id": task.get("id"),
                                "title": task.get("title", "بدون عنوان"),
                                "due_date": due_date,
                                "description": task.get("description", "")
                            })

                    # پردازش تاپل
                    elif isinstance(task, (tuple, list)):
                        if len(task) < 6:
                            print(f"⚠️ فرمت تاپل نامعتبر: {task}")
                            continue

                        task_id, title, description, due_date, status, created_at = task[:6]

                        if status != "pending":
                            continue

                        if not due_date:
                            continue

                        task_date = ReminderEngine._parse_date(due_date)
                        if not task_date:
                            continue

                        if task_date <= today:
                            due_tasks.append({
                                "id": task_id,
                                "title": title,
                                "due_date": due_date,
                                "description": description
                            })

                    else:
                        print(f"⚠️ نوع داده نامشخص: {type(task)}")

                except Exception as e:
                    print(f"❌ خطا در پردازش تسک: {e}")
                    continue

            return due_tasks

        except Exception as e:
            print(f"❌ خطا در دریافت تسک‌ها: {e}")
            return []

    @staticmethod
    def _parse_date(date_str: str) -> Optional[datetime]:
        """
        تبدیل رشته تاریخ به آبجکت datetime با پشتیبانی از فرمت‌های مختلف

        Args:
            date_str: رشته تاریخ

        Returns:
            Optional[datetime]: آبجکت تاریخ یا None
        """
        if not date_str:
            return None

        date_str = str(date_str).strip()

        # فرمت‌های پشتیبانی شده
        formats = [
            "%Y-%m-%d",
            "%Y-%m-%d %H:%M:%S",
            "%Y/%m/%d",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%d-%m-%Y",
            "%d/%m/%Y"
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_str[:10], fmt).date()
            except (ValueError, TypeError):
                continue

        print(f"⚠️ تاریخ نامعتبر: {date_str}")
        return None

    @staticmethod
    def get_overdue_tasks(user_id: int) -> List[Dict[str, Any]]:
        """
        دریافت تسک‌های عقب‌افتاده (بیش از امروز)

        Args:
            user_id: شناسه کاربر

        Returns:
            List[Dict]: لیست تسک‌های عقب‌افتاده
        """
        due_tasks = ReminderEngine.get_due_tasks(user_id)
        today = datetime.now().date()

        overdue = []
        for task in due_tasks:
            task_date = ReminderEngine._parse_date(task["due_date"])
            if task_date and task_date < today:
                overdue.append(task)

        return overdue

    @staticmethod
    def get_today_tasks(user_id: int) -> List[Dict[str, Any]]:
        """
        دریافت تسک‌های امروز

        Args:
            user_id: شناسه کاربر

        Returns:
            List[Dict]: لیست تسک‌های امروز
        """
        due_tasks = ReminderEngine.get_due_tasks(user_id)
        today = datetime.now().date()

        today_tasks = []
        for task in due_tasks:
            task_date = ReminderEngine._parse_date(task["due_date"])
            if task_date and task_date == today:
                today_tasks.append(task)

        return today_tasks

    @staticmethod
    def get_upcoming_tasks(user_id: int, days: int = 7) -> List[Dict[str, Any]]:
        """
        دریافت تسک‌های آینده

        Args:
            user_id: شناسه کاربر
            days: تعداد روزهای آینده

        Returns:
            List[Dict]: لیست تسک‌های آینده
        """
        try:
            tasks = TaskManager.get_all(user_id)
            today = datetime.now().date()
            upcoming_tasks = []

            if not tasks:
                return []

            for task in tasks:
                try:
                    if isinstance(task, dict):
                        if task.get("status") != "pending":
                            continue

                        due_date = task.get("due_date")
                        if not due_date:
                            continue

                        task_date = ReminderEngine._parse_date(due_date)
                        if not task_date:
                            continue

                        if today < task_date <= today + timedelta(days=days):
                            upcoming_tasks.append({
                                "id": task.get("id"),
                                "title": task.get("title", "بدون عنوان"),
                                "due_date": due_date,
                                "description": task.get("description", "")
                            })

                except Exception as e:
                    print(f"❌ خطا در پردازش تسک آینده: {e}")
                    continue

            return upcoming_tasks

        except Exception as e:
            print(f"❌ خطا در دریافت تسک‌های آینده: {e}")
            return []