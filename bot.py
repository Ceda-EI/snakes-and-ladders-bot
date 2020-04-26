"Bot Handler"
import os
from telegram.ext import Updater, CommandHandler
import config


def start(update, context):
    "/start"
    if update.effective_chat.id > 0:
        message = ("Single player is not supported at the moment. "
                   "Send /begin in a group to start the game.")
    else:
        message = "Send /begin to start the game."
    context.bot.send_message(update.effective_chat.id, message)


def main():
    "Main function"
    updater = Updater(token=config.API_KEY, use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler("start", start)
    dispatcher.add_handler(start_handler)
    updater.start_polling()

if __name__ == "__main__":
    main()
