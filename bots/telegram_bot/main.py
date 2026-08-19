import asyncio

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters
)

from services.tasks.worker import TaskWorker

from services.ai.config import TELEGRAM_TOKEN

from database.db import init_db

from handlers.start import start
from handlers.help import help_command
from handlers.plan import plan_command
from handlers.tech import tech_command
from handlers.message import handle_message

from handlers.admin_panel import admin_panel
from handlers.callbacks import callback_dispatcher

from handlers.profile import profile
from handlers.clear import clear_memory
from handlers.about import about

from handlers.user_callbacks import (
    buy_command,
    referral_command
)

from handlers.tasks import tasks_command
from handlers.task_actions import (
    done_task,
    delete_task
)
from core.logger import logger

def main():

    async def post_init(application):

        worker = TaskWorker(
            application.bot
        )


        # ذخیره استاندارد در telegram Application
        application.bot_data["task_worker"] = worker


        asyncio.create_task(
            worker.start()
        )


    init_db()
    


    logger.info(
    "Starting PF-AI Telegram Bot..."
    )
    


    app = (
        Application
        .builder()
        .token(
            TELEGRAM_TOKEN
        )
        .post_init(
            post_init
        )
        .build()
    )


    # ==================
    # Commands
    # ==================

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )


    app.add_handler(
        CommandHandler(
            "help",
            help_command
        )
    )


    app.add_handler(
        CommandHandler(
            "admin",
            admin_panel
        )
    )


    app.add_handler(
        CommandHandler(
            "plan",
            plan_command
        )
    )


    app.add_handler(
        CommandHandler(
            "tech",
            tech_command
        )
    )


    app.add_handler(
        CommandHandler(
            "profile",
            profile
        )
    )


    app.add_handler(
        CommandHandler(
            "clear",
            clear_memory
        )
    )


    app.add_handler(
        CommandHandler(
            "buy",
            buy_command
        )
    )


    app.add_handler(
        CommandHandler(
            "referral",
            referral_command
        )
    )


    app.add_handler(
        CommandHandler(
            "about",
            about
        )
    )


    # ==================
    # Tasks
    # ==================

    app.add_handler(
        CommandHandler(
            "tasks",
            tasks_command
        )
    )


    app.add_handler(
        CommandHandler(
            "done",
            done_task
        )
    )


    app.add_handler(
        CommandHandler(
            "delete",
            delete_task
        )
    )


    # ==================
    # Callbacks
    # ==================

    app.add_handler(
        CallbackQueryHandler(
            callback_dispatcher
        )
    )


    # ==================
    # Messages
    # ==================

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    logger.info(
    "PF-AI started successfully"
    )
    


    app.run_polling()



if __name__ == "__main__":
    main()