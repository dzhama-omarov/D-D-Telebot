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
        '''Данная функция вызываетсся, когда пользователь выбирает создание
        персонажа.
        Она записывает данное действие в логи, меняет состояние и
        отправляет ответное сообщение пользователю сообщение
        с просьбой выбрать рассу.
        Также создается соответсвующая клавиатура'''
        cur_user_id = call.from_user.id
        cur_chat_id = call.message.chat.id
        logger.info('{time}: Пользователь {user}, чат {chat_id} отправил callback {command}'
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
            logger.info('{time}: Персонаж пользователя {user_id}, чат {chat_id} добавлен в бд'
                        .format(time=datetime.fromtimestamp(call.message.date),
                                user_id=cur_user_id,
                                chat_id=cur_chat_id
                                ))
        else:
            logger.info('{time}: Персонаж пользователя {user_id}, чат {chat_id} найден в бд'
                        .format(time=datetime.fromtimestamp(call.message.date),
                                user_id=cur_user_id,
                                chat_id=cur_chat_id
                                ))
        bot.set_state(cur_user_id, BotStates.WAITING_FOR_RACE, cur_chat_id)
        logger.info('{time}: Установлено состояние: {state}'
                    .format(time=datetime.fromtimestamp(call.message.date),
                            state=bot.get_state(cur_user_id, cur_chat_id)
                            ))
        bot.send_message(call.message.chat.id, 'Выбери расу',
                         reply_markup=race_keyboard())

    @bot.callback_query_handler(func=lambda call:
                                call.data.startswith('chosen_race:'))
    def choose_class(call):
        '''Данная функция вызываетсся, когда пользователь выбирает расу.
        Она записывает данное действие в логи, меняет состояние и
        отправляет ответное сообщение пользователю сообщение
        с просьбой выбрать класс.
        Также создается соответсвующая клавиатура'''
        cur_user_id = call.from_user.id
        cur_chat_id = call.message.chat.id
        logger.info('{time}: Пользователь {user}, чат {chat_id} отправил callback {command}'
                    .format(time=datetime.fromtimestamp(call.message.date),
                            user=call.message.from_user.id,
                            chat_id=cur_chat_id,
                            command=call.data))
        character = Character.get(Character.owner == cur_user_id)
        character.race = call.data.split(':')[1]
        character.save()
        logger.info('{time}: Добавлена раса {race} в бд'
                    .format(time=datetime.fromtimestamp(call.message.date),
                            race=call.data.split(':')[1]))
        bot.set_state(cur_user_id, BotStates.WAITING_FOR_CLASS, cur_chat_id)
        logger.info('{time}: Установлено состояние: {state}'
                    .format(time=datetime.fromtimestamp(call.message.date),
                            state=bot.get_state(cur_user_id, cur_chat_id)
                            ))
        bot.send_message(call.message.chat.id, 'Выбери класс',
                         reply_markup=class_keyboard())

    @bot.callback_query_handler(func=lambda call:
                                call.data.startswith('chosen_class:'))
    def set_name(call):
        '''Данная функция вызываетсся, когда пользователь выбирает класс.
        Она записывает данное действие в логи, меняет состояние и
        отправляет ответное сообщение пользователю сообщение
        с просьбой назвать героя.
        Также создается соответсвующая клавиатура'''
        cur_user_id = call.from_user.id
        cur_chat_id = call.message.chat.id
        logger.info('{time}: Пользователь {user}, чат {chat_id} отправил callback {command}'
                    .format(time=datetime.fromtimestamp(call.message.date),
                            user=call.message.from_user.id,
                            chat_id=cur_chat_id,
                            command=call.data))
        character = Character.get(Character.owner == cur_user_id)
        character.char_class = call.data.split(':')[1]
        character.save()
        logger.info('{time}: Добавлен класс {cclass} в бд'
                    .format(time=datetime.fromtimestamp(call.message.date),
                            cclass=call.data.split(':')[1]))
        bot.set_state(user_id=cur_user_id, state=BotStates.WAITING_FOR_NAME, chat_id=cur_chat_id)
        logger.info('{time}: Установлено состояние: {state}'
                    .format(time=datetime.fromtimestamp(call.message.date),
                            state=bot.get_state(cur_user_id, cur_chat_id)
                            ))
        bot.send_message(call.message.chat.id, 'Как зовут героя?')
