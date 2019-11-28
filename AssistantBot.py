# -- coding: utf-8 --
from __future__ import unicode_literals
import telebot
from multiprocessing import Queue
from drivers.interrupt import Interrupt


# Debug_assistant_bot 898926225:AAEXGU2onSl0cGlDomzrpjvCWgqregmZC9I
bot = telebot.TeleBot('898926225:AAEXGU2onSl0cGlDomzrpjvCWgqregmZC9I')

user_validation = {'id': [681970459], 'name': ['Vova']}
admin_validation = {'id': [681970459], 'name': ['Vova']}


class CommonQueue:
    CQ = Queue()
    SysCQ = Queue()


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Привіт {}\nНатисни /help для довідки".format(message.chat.first_name))


@bot.message_handler(commands=["help"])
def help_box(message):
    bot.send_message(message.chat.id, "/start - початок використання\n/help - список команд\n\n")


@bot.message_handler()
def else_request(message):
    pass


def send():
    while not CommonQueue.CQ.empty():
        data = CommonQueue.CQ.get(block=False)
        bot.send_message(admin_validation['id'][0], data)


def on():
    interrupt = Interrupt(callback_handler=send, periodic=1)
    interrupt.go_go()

    bot.send_message(admin_validation['id'][0], 'FLAG REBOOT BOT')
    bot.polling()

