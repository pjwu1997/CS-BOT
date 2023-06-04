# %%
import os
import json
import telebot
import openai
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand, MenuButtonCommands
import random
import schedule
from threading import Thread
from time import sleep
import datetime

from utils import update, plot
# %%
def datetime_converter():
    ct = datetime.datetime.now()
    ct = ct - datetime.timedelta(minutes=ct.minute % 15,
                             seconds=ct.second,
                             microseconds=ct.microsecond)
    return ct

# # timestamp is number of seconds since 1970-01-01 

# print(ct)

# # convert the timestamp to a datetime object in the local timezone
# dt_object = datetime.datetime.fromtimestamp(ct)

# # print the datetime object and its type
# print("dt_object =", dt_object)
# print("type(dt_object) =", type(dt_object))
# %%
config = json.load(open('config.json'))
openai_key = config['openai_key']
tg_bot_token = config['tg_bot_token']
tg_chat_id = config['tg_chat_id']
response_id = config['response_id']
openai.api_key = openai_key
BOT_TOKEN=tg_bot_token
chat_id=tg_chat_id
coin_list = ['BTCUSDT', 'ETHUSDT', 'LTCUSDT']


bot = telebot.TeleBot(BOT_TOKEN)

bot.set_my_commands(commands = [
    BotCommand('mostshorted','查詢資費最低之幣種'),
    BotCommand('mostlonged','查詢資費最高之幣種'),
    BotCommand('getid', '得到聊天id'),
    BotCommand('getuserid', '得到用戶id')
    ])
bot.set_chat_menu_button(bot.get_me().id, MenuButtonCommands(type = 'commands'))

def check_valid(message):
    if message.from_user.id in response_id:
        return True
    else:
        return False

def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(0.5)
        # print('Check!')

def function_to_run():
    print('Running: ' + str(datetime.datetime.now()))
    send_photo(coin_list)
    return 1

def send_photo(coin_list):
    name = plot(coin_list)
    bot.send_photo(response_id[0], open(name, 'rb'))

@bot.message_handler(commands=['getid'])
def get_id(message):
    # print(message)
    chat_id = message.chat.id
    bot.send_message(chat_id, str(chat_id))

@bot.message_handler(commands=['getuserid'])
def getuserid(message):
    # print(message)
    user_id = message.from_user.id
    bot.send_message(message.chat.id, str(user_id))

@bot.message_handler(commands=['getuserid'])
def getuserid(message):
    # print(message)
    user_id = message.from_user.id
    bot.send_message(message.chat.id, str(user_id))




if __name__ == "__main__":
    # Create the job in schedule.
    schedule.every().hour.at(":02").do(function_to_run)

    # Spin up a thread to run the schedule check so it doesn't block your bot.
    # This will take the function schedule_checker which will check every second
    # to see if the scheduled job needs to be ran.
    Thread(target=schedule_checker).start() 

    # And then of course, start your server.
    bot.infinity_polling()
    # server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))


# %%
