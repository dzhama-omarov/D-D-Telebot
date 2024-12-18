from datetime import datetime
from telebot import TeleBot
from loguru import logger
from bot.states import BotStates
from bot.keyboards import race_keyboard, class_keyboard
from database.models import Character, User


def register_callbacks(bot: TeleBot):
    @bot.callback_query_handler(func=lambda call:
                                call.data == 'create_character'
                                and bot.get_state(
                                    call.from_user.id,
                                    call.message.chat.id
                                    ) == BotStates.START.name)
    def create_character(call):
"'This function is called when the user chooses to create
        a character.
        It records this action in the logs, changes the state and
        sends a reply message to the user.
        with a request to choose a race.
        A corresponding keyboard is also created"'
        cur_user_id = call.from_user.id
cur_chat_id = call.message.chat.id
logger.info ('{time}: User {user}, chat {chat_id} sent a callback {command}'
                    .format(time=datetime.fromtimestamp(call.message.date),
                            user=cur_user_id,
                            chat_id=cur_chat_id,
                            command=call.data))
        character, created = Character.get_or_create(
            owner=cur_user_id,
            defaults={'name': '',
                      'char_class': '',
                      'race': '',
                      'balance': 0,
                      'level': 1,
                      'equipment': ''})
        if created:
            character.balance = 0
            character.level = 1
            character.equipment = ''
            character.save()
            logger.info ('{time}: User character {user_id}, chat {chat_id} added to the database'
.format(time=datetime.fromtimestamp(call.message.date),
                                user_id=cur_user_id,
                                chat_id=cur_chat_id
                                ))
else:
logger.info ('{time}: User character {user_id}, chat {chat_id} found in db'
.format(time=datetime.fromtimestamp(call.message.date),
                                user_id=cur_user_id,
                                chat_id=cur_chat_id
                                ))
bot.set_state(cur_user_id, BotStates.WAITING_FOR_RACE, cur_chat_id)
logger.info ('{time}: Set state: {state}'
                    .format(time=datetime.fromtimestamp(call.message.date),
                            state=bot.get_state(cur_user_id, cur_chat_id)
))
bot.send_message(call.message.chat.id , 'Choose a race',
                         reply_markup=race_keyboard())

    @bot.callback_query_handler(func=lambda call:
                                call.data.startswith('chosen_race:'))
def choose_class(call):
"'This function is called when the user selects a race.
        It records this action in the logs, changes the state and
        sends a reply message to the user.
        with a request to choose a class.
        A corresponding keyboard is also created"'
        cur_user_id = call.from_user.id
cur_chat_id = call.message.chat.id
logger.info ('{time}: User {user}, chat {chat_id} sent a callback {command}'
                    .format(time=datetime.fromtimestamp(call.message.date),
                            user=call.message.from_user.id,
                            chat_id=cur_chat_id,
                            command=call.data))
        character = Character.get(Character.owner ==cur_user_id)
character.race = call.data.split(':')[1]
character.save()
logger.info ('{time}: Race {race} added to the database'
.format(time=datetime.fromtimestamp(call.message.date),
                            race=call.data.split(':')[1]))
        bot.set_state(cur_user_id, BotStates.WAITING_FOR_CLASS, cur_chat_id)
logger.info ('{time}: Set state: {state}'
                    .format(time=datetime.fromtimestamp(call.message.date),
                            state=bot.get_state(cur_user_id, cur_chat_id)
))
bot.send_message(call.message.chat.id , 'Choose a class',
                         reply_markup=class_keyboard())

    @bot.callback_query_handler(func=lambda call:
                                call.data.startswith('chosen_class:'))
    def set_name(call):
        "'This function is called when the user selects a class.
        It records this action in the logs, changes the state and
        sends a reply message to the user.
        with a request to name the hero.
        A corresponding keyboard is also created"'
        cur_user_id = call.from_user.id
cur_chat_id = call.message.chat.id
logger.info ('{time}: User {user}, chat {chat_id} sent a callback {command}'
                    .format(time=datetime.fromtimestamp(call.message.date),
                            user=call.message.from_user.id,
                            chat_id=cur_chat_id,
                            command=call.data))
        character = Character.get(Character.owner ==cur_user_id)
character.char_class = call.data.split(':')[1]
character.save()
logger.info ('{time}: Added the {cclass} class to the database'
.format(time=datetime.fromtimestamp(call.message.date),
                            cclass=call.data.split(':')[1]))
bot.set_state(user_id=cur_user_id, state=BotStates.WAITING_FOR_NAME, chat_id=cur_chat_id)
logger.info ('{time}: Set state: {state}'
                    .format(time=datetime.fromtimestamp(call.message.date),
                            state=bot.get_state(cur_user_id, cur_chat_id)
))
bot.send_message(call.message.chat.id , 'What's the hero's name?')
