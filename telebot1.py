# -*- coding: utf-8 -*-
import config
import telebot
from SQLighter import SQLighter
import random
import utils
from telebot import types
import os



bot = telebot.TeleBot(config.TOKEN)



"""@bot.message_handler(commands = ["test"])
def tete(message):
    for i in os.listdir("musmp3/"):
        if i.split(".")[-1] == "ogg":
            f = open('musmp3/' + i, 'rb')
            ty = bot.send_voice(message.chat.id, f)
            bot.send_message(message.chat.id, ty.voice.file_id, reply_to_message_id = ty.message_id)"""


@bot.message_handler(commands = ["game"])
def game(message):
    db_worker = SQLighter(config.database_name)
    row = db_worker.select_single(random.randint(1, utils.get_rows_count()))
    markup = utils.generate_markup(row[0][2], row[0][3])
    bot.send_voice(message.chat.id, row[0][1], reply_markup = markup)
    utils.set_user_game(message.chat.id, row[0][2])
    db_worker.close()

@bot.message_handler(commands = ["start"])
def hello(message):
    sti = open("stic/hello.webp", "rb")
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id, "Доброе время суток, товарищ {}.\n"
                                      "Я большой фанат Ed Sheeran.\n"
                                      "Давай проверим насколько хорошо ты знаешь этого певца!\n"
                                      "Набери команду /game , чтобы начать игру.".format(message.from_user.first_name))


@bot.message_handler(func = lambda message: True, content_types = ["text"])
def check_answer(message):
    answer = utils.get_answer_for_user(message.chat.id)
    if not answer:
        bot.send_message(message.chat.id, 'Чтобы начать игру, выберите команду /game')
    else:
        keyboard_hider = types.ReplyKeyboardRemove()
        if message.text == answer:
            bot.send_message(message.chat.id, "Верно!\nДавай еще раз)", reply_markup = keyboard_hider)
        else:
            bot.send_message(message.chat.id, "Эх, я был о тебе лучшего мнения. Ладно, дам еще попытку", reply_markup = keyboard_hider)
        utils.finish_user_game(message.chat.id)



if __name__ == "__main__":
    utils.count_rows()
    random.seed()
    bot.polling(none_stop = True)