"Bot Handler"
from io import BytesIO
import logging
import random

from telegram.ext import Updater, CommandHandler
import config

from boards import BOARDS
from sal import Board


def start(update, context):
    "/start"
    if update.effective_chat.id > 0:
        message = ("Single player is not supported at the moment. "
                   "Send /newgame in a group to start the game.")
    else:
        message = "Send /newgame to start the game."
    context.bot.send_message(update.effective_chat.id, message)


def newgame(update, context):
    "/newgame"
    if update.effective_chat.id > 0:
        context.bot.send_message(update.effective_chat.id, "Run in a group!")
        return

    if "game" in context.chat_data:
        context.bot.send_message(update.effective_chat.id, "Game in progress!")
        return

    board = random.choice(BOARDS)
    game = context.chat_data["game"] = Board(board.data, board.image)
    caption = f"Starting new game with board {board.name}. Join via /join."
    context.bot.send_photo(update.effective_chat.id, BytesIO(game.draw()),
                           caption=caption)


def join(update, context):
    "/join"
    if "game" not in context.chat_data:
        context.bot.send_message(update.effective_chat.id,
                                 "No game in progress.")
        return

    game = context.chat_data["game"]
    first_name = update.effective_user.first_name
    game.add_player(update.effective_user.id, first_name)
    context.bot.send_message(update.effective_chat.id, f"{first_name} joined!")


def main():
    "Main function"
    logging.basicConfig(level=logging.INFO)
    updater = Updater(token=config.API_KEY, use_context=True)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler("start", start)
    newgame_handler = CommandHandler("newgame", newgame)
    join_handler = CommandHandler("join", join)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(newgame_handler)
    dispatcher.add_handler(join_handler)
    updater.start_polling()

if __name__ == "__main__":
    main()
