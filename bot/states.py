from telebot.handler_backends import State, StatesGroup


class BotStates(StatesGroup):
    START = State()
    WAITING_FOR_RACE = State()
    WAITING_FOR_CLASS = State()
    WAITING_FOR_NAME = State()
