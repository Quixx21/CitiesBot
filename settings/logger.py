import asyncio
import logging
import sys

from aiogram import Bot

# just log to .log file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s() | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),  # logs to console
        logging.FileHandler("../bot.log", encoding="utf-8"),  # logs to file
    ],
)

logger = logging.getLogger("CitiesBot")


# log to send it for admin
class TelegramLogHandler(logging.Handler):
    def __init__(self, bot: Bot, chat_id: int, level=logging.ERROR):
        super().__init__(level)
        self.bot = bot
        self.chat_id = chat_id

    def emit(self, record: logging.LogRecord):
        msg = self.format(record)
        try:
            asyncio.create_task(
                self.bot.send_message(
                    self.chat_id, f" {record.levelname} in {record.name}:\n{msg}"
                )
            )
        except Exception as e:
            print("Failed to send log to Telegram:", e)
