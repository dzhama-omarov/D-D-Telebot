from telebot import TeleBot
from loguru import logger
from bot.states import BotStates
from datetime import datetime
from bot.keyboards import main_menu_keyboard, race_keyboard, class_keyboard
from database.models import Character, User


def register_handlers(bot: TeleBot):
    @bot.message_handler(commands=['start'])
def main_menu(message):
"'This function is called when the user sends /start.
        She records this action in the logs and sends a reply message
        a message with hints about further actions is sent to the user.
        A response keyboard is also created"'
        cur_user_id = message.from_user.id
cur_chat_id = message.chat.id
logger.info ('{time}: User {user_id}, chat {chat_id} sent the command {command}'
                    .format(time=datetime.fromtimestamp(message.date),
                            user_id=cur_user_id,
                            chat_id=cur_chat_id,
                            command=message.text))
bot.set_state(user_id=cur_user_id, state=BotStates.START, chat_id=cur_chat_id)
logger.info ('{time}: Set state: {state}'
                    .format(time=datetime.fromtimestamp(message.date),
                            state=bot.get_state(cur_user_id, cur_chat_id)
                            ))
        user, created = User.get_or_create(
            user_id=cur_user_id,
            defaults={'chat_id': cur_chat_id}
            )
        if created:
            logger.info ('{time}: User {user_id}, chat {chat_id} added to the database'
.format(time=datetime.fromtimestamp(message.date),
                                user_id=cur_user_id,
                                chat_id=cur_chat_id
                                ))
else:
logger.info ('{time}: User {user_id}, chat {chat_id} found in the database'
.format(time=datetime.fromtimestamp(message.date),
                                user_id=cur_user_id,
                                chat_id=cur_chat_id
                                ))
bot.send_message(message.chat.id , 'Greetings to you!\n'
'I'll help you create a hero. '
'If you're ready, click "Create a hero"'
                         'If you want to know what I can do, click "Help"',
                         reply_markup=main_menu_keyboard())

    @bot.message_handler(state=BotStates.WAITING_FOR_NAME)
def set_name(message):
"'This function is called when the user sends any
        text for entering the name of the hero.
        She records this action in the logs and sends a reply message
        a message to the user with information about the created hero"'
        cur_user_id = message.from_user.id
        logger.info ('{time}: User {user_id}, chat {chat_id} sent the name of the hero {hero}'
                    .format(time=datetime.fromtimestamp(message.date),
                            user_id=message.from_user.id,
                            chat_id=message.chat.id,
                            hero=message.text))
        character = Character.get(Character.owner == cur_user_id)
        character.name = message.text
        character.save()
bot.send_message(message.chat.id , 'A hero has been created!\n\n'
                         'Name: {name}\n'
                         'Race: {race}\n'
                         'Class: {cclass}\n'
                         'Number of coins: {balance}\n'
                         'Level: {level}'.format(name=character.name,
                                                   race=character.race,
                                                   cclass=character.char_class,
                                                   balance=character.balance,
                                                   level=character.level))

    @bot.message_handler(func=lambda message: True)
    def debug_handler(message):
        logger.info("Message received: {msg}".format(msg=message.text))
        logger.info("Current state: {state}".format(
            state=bot.get_state(message.from_user.id, message.chat.id)
        ))
