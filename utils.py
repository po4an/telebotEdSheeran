from telebot import types
from SQLighter import SQLighter
import config
from random import shuffle
from storage import storage


def count_rows():
    db = SQLighter(config.database_name)
    rowsnum = db.count_rows()
    storage['rows_count'] = rowsnum


def get_rows_count():
    rowsnum = storage['rows_count']
    return rowsnum


def set_user_game(chat_id, estimated_answer):
    storage[str(chat_id)] = estimated_answer


def finish_user_game(chat_id):
    del storage[str(chat_id)]


def get_answer_for_user(chat_id):
    try:
        answer = storage[str(chat_id)]
        return answer
    except KeyError:
        return None



def generate_markup(right_answer, wrong_answer):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard = True, resize_keyboard = True)
    all_answers = '{},{}'.format(right_answer, wrong_answer)
    list_items = []
    for item in all_answers.split(","):
        list_items.append(item)
    shuffle(list_items)
    for item in list_items:
        markup.add(item)
    return markup
