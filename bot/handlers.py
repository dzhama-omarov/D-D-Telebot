from telebot import TeleBot
from loguru import logger
from bot.states import BotStates
from datetime import datetime
from bot.keyboards import main_menu_keyboard, race_keyboard, class_keyboard
from database.models import Character, User


def register_handlers(bot: TeleBot):
    @bot.message_handler(commands=['start'])
    def main_menu(message):
        '''Данная функция вызываетсся, когда пользователь отправляет /start.
        Она записывает данное действие в логи и отправляет ответное сообщение
        пользователю сообщение с подсказками о дальнейших дейстивиях.
        Также создается клавиатура ответа'''
        cur_user_id = message.from_user.id
        cur_chat_id = message.chat.id
        logger.info('{time}: Пользователь {user_id}, чат {chat_id} отправил команду {command}'
                    .format(time=datetime.fromtimestamp(message.date),
                            user_id=cur_user_id,
                            chat_id=cur_chat_id,
                            command=message.text))
        bot.set_state(user_id=cur_user_id, state=BotStates.START, chat_id=cur_chat_id)
        logger.info('{time}: Установлено состояние: {state}'
                    .format(time=datetime.fromtimestamp(message.date),
                            state=bot.get_state(cur_user_id, cur_chat_id)
                            ))
        user, created = User.get_or_create(
            user_id=cur_user_id,
            defaults={'chat_id': cur_chat_id}
            )
        if created:
            logger.info('{time}: Пользователь {user_id}, чат {chat_id} добавлен в бд'
                        .format(time=datetime.fromtimestamp(message.date),
                                user_id=cur_user_id,
                                chat_id=cur_chat_id
                                ))
        else:
            logger.info('{time}: Пользователь {user_id}, чат {chat_id} найден в бд'
                        .format(time=datetime.fromtimestamp(message.date),
                                user_id=cur_user_id,
                                chat_id=cur_chat_id
                                ))
        bot.send_message(message.chat.id, 'Приветствую тебя!\n'
                         'Я помогу тебе создать героя. '
                         'Если готов нажимай "Создать героя"'
                         'Если же хочешь узнать, что я умею, нажми "Помощь"',
                         reply_markup=main_menu_keyboard())

    @bot.message_handler(state=BotStates.WAITING_FOR_NAME)
    def set_name(message):
        '''Данная функция вызываетсся, когда пользователь отправляет любой
        текст для ввода имени героя.
        Она записывает данное действие в логи и отправляет ответное сообщение
        пользователю сообщение с ингформацией о созданом герое'''
        cur_user_id = message.from_user.id
        logger.info('{time}: Пользователь {user_id}, чат {chat_id} отправил имя героя {hero}'
                    .format(time=datetime.fromtimestamp(message.date),
                            user_id=message.from_user.id,
                            chat_id=message.chat.id,
                            hero=message.text))
        character = Character.get(Character.owner == cur_user_id)
        character.name = message.text
        character.save()
        bot.send_message(message.chat.id, 'Герой создан!\n\n'
                         'Имя: {name}\n'
                         'Раса: {race}\n'
                         'Класс: {cclass}\n'
                         'Кол-во монет: {balance}\n'
                         'Уровень: {level}'.format(name=character.name,
                                                   race=character.race,
                                                   cclass=character.char_class,
                                                   balance=character.balance,
                                                   level=character.level))

    @bot.message_handler(func=lambda message: True)
    def debug_handler(message):
        logger.info("Получено сообщение: {msg}".format(msg=message.text))
        logger.info("Текущее состояние: {state}".format(
            state=bot.get_state(message.from_user.id, message.chat.id)
        ))
