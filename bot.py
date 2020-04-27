"Bot Handler"
import logging
import random

from telegram.ext import Updater, CommandHandler, MessageHandler, filters, \
        PicklePersistence
import config

from boards import BOARDS
from sal import Board, NotTurnError


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
    context.bot.send_photo(update.effective_chat.id, game.draw(),
                           caption=caption)


def join(update, context):
    "/join"
    if "game" not in context.chat_data:
        context.bot.send_message(update.effective_chat.id,
                                 "No game in progress.")
        return

    game = context.chat_data["game"]
    first_name = update.effective_user.first_name
    color = game.add_player(update.effective_user.id, first_name)
    message = f"{first_name} joined with {color}!"
    context.bot.send_message(update.effective_chat.id, message)


def begin(update, context):
    "/begin"
    if "game" not in context.chat_data:
        context.bot.send_message(update.effective_chat.id,
                                 "No game in progress.")
        return

    game = context.chat_data["game"]
    context.chat_data["begin"] = True
    player_name = game.turn["name"]
    message = f"Game has begun! Current turn: {player_name}"
    context.bot.send_message(update.effective_chat.id, message)


def status(update, context):
    "/status"
    if "game" not in context.chat_data:
        context.bot.send_message(update.effective_chat.id,
                                 "No game in progress.")
        return

    game = context.chat_data["game"]
    message = "List of players: \n\n"
    for player in game.players:
        if game.turn == player:
            message += "* "
        else:
            message += "   "
        message += (f"{player['position']}: {player['name']} "
                    f"({player['color'].name} {player['shape'].name})\n")
    context.bot.send_message(update.effective_chat.id, message)


def dice(update, context):
    "Handles dice being thrown"
    if "game" not in context.chat_data:
        return

    if update.message.forward_date is not None:
        return

    if not context.chat_data.get("begin", False):
        context.bot.send_message(update.effective_chat.id,
                                 "Game has not started yet.")
        return

    game = context.chat_data["game"]
    pid = update.effective_user.id

    if pid != game.turn["pid"]:
        return

    steps = update.message.dice.value
    try:
        player = game.turn
        final_position, direction = game.move(pid, steps, check_turn=True)
    except NotTurnError:
        return
    img = game.draw()
    if final_position == 100:
        message = f"{player['name']} ({player['color'].name}) won! Game ended."
        del context.chat_data["game"]
        context.chat_data["begin"] = False
    elif direction == 1:
        message = (f"{player['name']} grabbed a ladder and reached "
                   f"{final_position}.")
    elif direction == 0:
        message = f"{player['name']} reached {final_position}."
    elif direction == -1:
        message = (f"{player['name']} was dragged down by a snake and reached "
                   f"{final_position}.")

    if final_position != 100:
        next_player = game.turn
        message += f" Current turn: {next_player['name']}"
    context.bot.send_photo(update.effective_chat.id, img, caption=message)


def main():
    "Main function"
    logging.basicConfig(level=logging.INFO)
    if config.PERSIST:
        persist = PicklePersistence(config.PERSIST_FILENAME)
    else:
        persist = None
    updater = Updater(token=config.API_KEY, use_context=True, persistence=persist)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler("start", start)
    newgame_handler = CommandHandler("newgame", newgame)
    join_handler = CommandHandler("join", join)
    begin_handler = CommandHandler("begin", begin)
    status_handler = CommandHandler("status", status)
    dice_handler = MessageHandler(filters.Filters.dice, dice)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(newgame_handler)
    dispatcher.add_handler(join_handler)
    dispatcher.add_handler(begin_handler)
    dispatcher.add_handler(status_handler)
    dispatcher.add_handler(dice_handler)
    updater.start_polling()

if __name__ == "__main__":
    main()
