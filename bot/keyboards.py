from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from services.dnd_api import get_from_dnd_api


def main_menu_keyboard():
keyboard = InlineKeyboardMarkup()
keyboard.row(InlineKeyboardButton('Create a character',
                                      callback_data='create_character'),
                 InlineKeyboardButton('Help', callback_data='help'))
return keyboard


def race_keyboard():
    n_of_races, races_list = get_from_dnd_api('races')
    keyboard = InlineKeyboardMarkup()
    for race_data in races_list:
        index = race_data['index']
        name = race_data['name']
        url = race_data['url']
        keyboard.add(InlineKeyboardButton(name,
                                          callback_data='chosen_race:{race}'
                                          .format(race=name)))
    return keyboard


def class_keyboard():
    n_of_cclass, cclass_list = get_from_dnd_api('classes')
    keyboard = InlineKeyboardMarkup()
    for cclass_data in cclass_list:
        index = cclass_data['index']
        name = cclass_data['name']
        url = cclass_data['url']
        keyboard.add(InlineKeyboardButton(name,
                                          callback_data='chosen_class:{cclass}'
                                          .format(cclass=name)))
    return keyboard
