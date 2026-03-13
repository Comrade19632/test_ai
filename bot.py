import logging
import os
from datetime import datetime, timezone

import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def get_usd_to_rub_rate() -> tuple[float, str]:
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    usd = data["Valute"]["USD"]
    rate = float(usd["Value"])  # RUB for 1 USD
    date_raw = data.get("Date")
    rate_date = datetime.fromisoformat(date_raw.replace("Z", "+00:00")) if date_raw else datetime.now(timezone.utc)
    return rate, rate_date.strftime("%Y-%m-%d %H:%M UTC")


def build_rate_text() -> str:
    rate, rate_date = get_usd_to_rub_rate()
    return f"Курс: 1 USD = {rate:.4f} RUB\nИсточник: ЦБ РФ ({rate_date})"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Привет! Отправь любое сообщение, и я пришлю текущий курс рубля к доллару."
    )


async def reply_with_rate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        text = build_rate_text()
    except Exception as exc:  # noqa: BLE001
        logger.exception("Failed to get USD/RUB rate: %s", exc)
        text = "Не удалось получить курс прямо сейчас. Попробуй еще раз через минуту."

    await update.message.reply_text(text)


def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN environment variable is required")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_with_rate))

    logger.info("Bot started")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
