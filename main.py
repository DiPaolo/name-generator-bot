#!/usr/bin/env python

import logging
import os
import random
import time

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext


# random.seed(time.time() / time.perf_counter() * time.process_time())
# random.seed(len(first_name) * time.time() / time.perf_counter() * time.process_time())


def gen_first_name():
    with open('first_names.txt', 'rt') as f:
        first_names = list()
        lines = f.readlines()
        for first_name in lines:
            if first_name[-1] == '\n':
                first_name = first_name[:-1]
            first_names.append(first_name)
        # print(lines)
        # print(first_names)
        return random.choice(first_names)


def gen_second_name():
    with open('second_names.txt', 'rt') as f:
        second_names = list()
        lines = f.readlines()
        for second_name in lines:
            if second_name[-1] == '\n':
                second_name = second_name[:-1]
            second_names.append(second_name)
        # print(lines)
        # print(second_names)
        return random.choice(second_names)


def gen_name():
    return f'{gen_first_name()} {gen_second_name()}'


# включаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


# это обработчики команд (handler-ы). Обычно приниают вот эти два параметра, которые содержат нужный
# контекст, то есть необъодимые для нас переменные (типа, имени пользователя, его ID и так далее), и
# созданный нами движок (об этом ниже)

# вот обработчик команды /start. Когда пользователь вводит /start, вызывается эта функция
# то же самое происходит, если пользователь выберет команду start из списка команд (это
# сделаем позже в BotFather)
def generate_name(engine: Update, context: CallbackContext) -> None:
    print('generate_name()')
    engine.message.reply_text(gen_name(), reply_to_message_id=None)


# другой обработчик - для команды /help. Когда пользователь вводит /help, вызывается этот код
def help_command(engine: Update, context: CallbackContext) -> None:
    # отправляем какой-то стандартный жестко заданный текст
    engine.message.reply_text('Помощь!')


def echo(engine: Update, context: CallbackContext) -> None:
    # вызываем команду отправки сообщения пользователю, используя
    # при это текст сообщения, полученный от пользователя
    engine.message.reply_text(engine.message.text)


def main() -> None:
    # создаем объект фреймворка (библиотеки) для создания телеграм-ботов, с помощью
    # которого мы сможем взаимодействовать с фреймворком, то есть тот связующий объект,
    # через который мы будем общаться со всеми внутренностями (которые делают основную
    # работу по отправке сообщений за нас) фреймворка. Причем, общаться будем в обе стороны:
    # принимать сообщения от него и задавать параметры для него
    #
    # я назвал его engine (движок), чтобы было понятнее. В самой либе (библиотеке, фреймворке)
    # он называется Updater, как видно, что немного запутывает
    engine = Updater(os.getenv('DP_TG_BOT_TOKEN'))

    # получаем объект "передатчика" или обработчика сообщений от нашего движка
    dispatcher = engine.dispatcher

    # тут "связываем" наши команды и соответствующие им обработчики (хендлеры);
    # иногда говорят "повесить коллбэк" (коллбэк это то же самое что и обработчики (они же хендлеры),
    # то есть та функция, которая вызывается в ответ на какое-то событие: callback, то есть
    # call back - дословно, что-то вроде вызвать обратно, то есть наша функция, которую мы передали,
    # вызовется позже в ответ на какое-то событие; в нашем случае они будут вызываться тогда, когда
    # пользователь будет выбирать соответствующие команды
    dispatcher.add_handler(CommandHandler("generate", generate_name))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # говорим обработчику сообений, чтобы он вызывал функцию echo каждый раз,
    # когда пользователь отправляем боту сообщение
    #
    # про параметр 'Filters.text & ~Filters.command' можно пока не заморачиваться;
    # он означает, что функция echo будет вызываться только тогда, когда пользователь
    # ввел именно текст, а не команду; в противном случае, если пользователь введет
    # команду /start или /help, эта функция будет вызвана, что нам не нужно
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    # dispatcher.add_handler(MessageHandler(Filters.user("@russian_name_generator_bot"), generate_name))

    # непосредственно старт бота
    engine.start_polling()

    # говорим боту работать, пока не нажмем Ctrl-C или что-то не сломается само :)
    engine.idle()


if __name__ == '__main__':
    main()
