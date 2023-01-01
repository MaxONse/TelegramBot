import telebot
import os
from telebot import types
import time

path = os.path.join('', 'register.txt')
path1 = os.path.join('', 'Mike_Tyson.txt')
path2 = os.path.join('', 'Mohammad_Ali.txt')

config = {
    "name": "py_sport_bot",
    "token": "5852813491:AAGRatVTQ4c9kaSE6QlsfWZ_ZtpGunlOK6M"
}

keyboard1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn_autorisation = types.KeyboardButton("Autorisation")
btn_registration = types.KeyboardButton("Registration")
keyboard1.add(btn_autorisation, btn_registration)
key2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
b1 = types.KeyboardButton("Order trainer")
b2 = types.KeyboardButton("Buy exercise with a trainer")
b3 = types.KeyboardButton("Show numbers available exercise with a trainer")
b4 = types.KeyboardButton("Check account")
b5 = types.KeyboardButton("Recharge your account")
b6 = types.KeyboardButton("Numbers of remaining visits")
b7 = types.KeyboardButton("Buy a visits")
b8 = types.KeyboardButton("Show available trainers")
key2.add(b1, b2, b3, b4, b5, b6, b7, b8)
key1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
t1 = types.KeyboardButton("Mike Tyson")
t2 = types.KeyboardButton("Mohammad Ali")
key1.add(t1, t2)
bot = telebot.TeleBot(config["token"])
trainer = ""  # глобальная переменная для проверки последнего выбранного тренера
exercise = 500
visits = 100  # глобальная переменная для покупки посещений
auth = False  # глобальная переменная для прохождения аутентификации
data = []  # глобальная переменная для записи всех данных пользователя и их изменения, записи в файл!


@bot.message_handler(content_types=["text"])
def get_text(message):
    global trainer
    global data
    global auth
    if message.text == "/start":
        bot.send_message(message.chat.id, f"Please Choose:", reply_markup=keyboard1)
    if message.text == "Registration":
        question = bot.send_message(message.chat.id,
                                    "Enter a login, card number, name and surname separated by a space!")
        bot.register_next_step_handler(question, registration)
    if message.text == "Autorisation":
        question = bot.send_message(message.chat.id, "Enter a login and card number separated by a space!")
        bot.register_next_step_handler(question, autorisation)
    if auth:
        if message.text == "Order trainer":
            bot.send_message(message.chat.id, f"Please Choose a trainer to see available time:", reply_markup=key1)
        if message.text == "Mike Tyson":
            trainer += 'Mike Tyson'
            file = open(path1, "r")
            read = file.readlines()
            file.close()
            inlines = telebot.types.InlineKeyboardMarkup()
            for i in read:
                j = i.split("-")
                inlines.add(telebot.types.InlineKeyboardButton(text=f"{j[0]}", callback_data=f"{j[0]}"))
            bot.send_message(message.chat.id, f"Choose:", reply_markup=inlines)
        if message.text == "Mohammad Ali":
            trainer += 'Mohammad Ali'
            file = open(path2, "r")
            read = file.readlines()
            file.close()
            inlines = telebot.types.InlineKeyboardMarkup()
            for i in read:
                j = i.split("-")
                inlines.add(telebot.types.InlineKeyboardButton(text=f"{j[0]}", callback_data=f"{j[0]}"))
            bot.send_message(message.chat.id, f"Choose", reply_markup=inlines)
        if message.text == "Buy exercise with a trainer":
            question = bot.send_message(message.chat.id, f"How many exercises you will take?")
            bot.register_next_step_handler(question, buy_ex)
        if message.text == "Show numbers available exercise with a trainer":
            bot.send_message(message.chat.id, f"You have a {data[6]} classes", reply_markup=key2)
        if message.text == "Check account":
            bot.send_message(message.chat.id, f"You have {data[4]}$ on account ", reply_markup=key2)
        if message.text == "Recharge your account":
            question = bot.send_message(message.chat.id, f"How much do you want to top up your account?")
            bot.register_next_step_handler(question, funds)
        if message.text == "Numbers of remaining visits":
            bot.send_message(message.chat.id, f"You have {data[5]} visits on account ", reply_markup=key2)
        if message.text == "Buy a visits":
            question = bot.send_message(message.chat.id, f"How many visits do you want to buy?")
            bot.register_next_step_handler(question, vis)
        if message.text == "Show available trainers":
            bot.send_message(message.chat.id, f"We have two trainers: Mike Tyson and Mohammad Ali")


def vis(message):  # функция для покупки посещений, за одно проверки на количество денег на счету!
    global visits
    global data
    if int(data[4]) < visits:
        bot.send_message(message.chat.id, f"Insufficient funds, please, top up an account", reply_markup=key2)
    elif int(message.text) >= 1:
        if int(message.text) * visits <= int(data[4]):
            data[4] = f"{int(data[4]) - (int(message.text) * visits)}"
            data[5] = f"{int(data[5]) + int(message.text)}"
            file = open(path, "r")
            read = file.readlines()
            file.close()
            lt = []
            for i in read:
                j = i.split()
                if data[0] != j[0]:
                    lt.append(i)
            lt.append(" ".join(data))
            file = open(path, "w")
            file.write("\n".join(lt) + "\n")
            file.close()
        else:
            bot.send_message(message.chat.id, f"Insufficient funds, please, top up an account", reply_markup=key2)
    else:
        bot.send_message(message.chat.id, f"Wrong type input", reply_markup=key2)
    bot.send_message(message.chat.id, "Done", reply_markup=key2)


def funds(message):  # Функция для пополнения счета
    global data
    data[4] = f'{(int(message.text) + (int(data[4])))}'
    file = open(path, "r")
    read = file.readlines()
    file.close()
    lt = []
    for i in read:
        j = i.split()
        if data[0] != j[0]:
            lt.append(i)
    lt.append(" ".join(data))
    file = open(path, "w")
    file.write("\n".join(lt) + "\n")
    file.close()
    bot.send_message(message.chat.id, "Done", reply_markup=key2)


def buy_ex(message):  # функция для покупки занятий с тренером, проверяет счет!
    global exercise
    global data
    if int(data[4]) < exercise:
        bot.send_message(message.chat.id, f"Insufficient funds, please, top up an account", reply_markup=key2)
    elif (int(message.text)) >= 1:
        if ((int(message.text)) * exercise) <= (int(data[4])):
            data[4] = f"{(int(data[4]) - (int(message.text) * exercise))}"
            data[6] = f"{(int(data[6]) + int(message.text))}"
            file = open(path, "r")
            read = file.readlines()
            file.close()
            lt = []
            for i in read:
                j = i.split()
                if data[0] != j[0]:
                    lt.append(i)
            lt.append(" ".join(data))
            file = open(path, "w")
            file.write("\n".join(lt) + "\n")
            file.close()
    else:
        bot.send_message(message.chat.id, f"Wrong input or insufficient funds, please, top up an account",
                         reply_markup=key2)
    bot.send_message(message.chat.id, "Done", reply_markup=key2)


def autorisation(message):  # проверка авторизации и времени с прошедшей авторизации
    global auth
    global data
    if len(message.text.split()) == 2:
        file = open(path, "r")
        read = file.readlines()
        st = message.text.split()
        file.close()
        tm = (int(time.time()) - 86400)
        for i in read:
            j = i.split()
            if j[0] == st[0] and j[1] == st[1] and int(j[7]) >= tm:
                data.append(j)
                data = [item for sublist in data for item in sublist]
                auth = True
                bot.send_message(message.chat.id, f"Hello user, choose what do you want?", reply_markup=key2)

            elif j[0] == st[0] and j[1] == st[1] and int(j[7]) < tm:
                data.append(j)
                data = [item for sublist in data for item in sublist]
                data[7] = str(int(time.time()))
                lt = []
                for i in read:
                    if message.text not in i:
                        lt.append(i)
                data1 = " ".join(data)
                lt.append(data1)
                file = open(path, "w")
                file.write("\n".join(lt) + "\n")
                file.close()
                auth = True
                bot.send_message(message.chat.id, f"Hello user, choose what do you want?", reply_markup=key2)
            else:
                bot.send_message(message.chat.id, f"Who are you?? You shell not pass!!!")
                bot.send_message(message.chat.id, f"Please Choose:", reply_markup=keyboard1)
    else:
        bot.send_message(message.chat.id, f"Wrong type input", reply_markup=keyboard1)


def registration(message):  # дозапись в файл нового пользователя
    if len(message.text.split()) == 4:
        file = open(path, "a")
        money = 0
        visits = 30
        trainers = 0
        reg = message.text.split()
        file.write(f"{reg[0]} {reg[1]} {reg[2]} {reg[3]} {money} {visits} {trainers} {int(time.time())}\n")
        file.close()
        bot.register_next_step_handler(bot.send_message(message.chat.id, f"Use you're login and password to enter!"),
                                       autorisation)
    else:
        bot.send_message(message.chat.id, f"Wrong input", reply_markup=keyboard1)


@bot.callback_query_handler(func=lambda call: True)
def callback_data(call):  # вывод расписания тренеров по имени, дням и часам
    global trainer
    global data
    if int(data[6]) > 0:
        if trainer == 'Mike Tyson':
            file = open(path1, 'r')
            read1 = file.readlines()
            file.close()
            for i in read1:
                j = i.split("-")
                if j[0] == call.data:
                    k = j[1].split()
                    inlines = telebot.types.InlineKeyboardMarkup()
                    for l in k:
                        inlines.add(telebot.types.InlineKeyboardButton(text=f"{l}", callback_data=f"{l}"))
                    bot.send_message(call.message.chat.id, f"{call.data}", reply_markup=inlines)
                    if call.data:
                        data[6] = f'{((int(data[6])) - 1)}'
                        file = open(path, "r")
                        read = file.readlines()
                        file.close()
                        lt = []
                        for i in read:
                            j1 = i.split()
                            if data[0] != j1[0]:
                                lt.append(i)
                        lt.append(" ".join(data))
                        file = open(path, "w")
                        file.write("\n".join(lt) + "\n")
                        file.close()
                        trainer = ""
        elif trainer == 'Mohammad Ali':
            file = open(path2, 'r')
            read1 = file.readlines()
            file.close()
            for i in read1:
                j = i.split("-")
                if j[0] == call.data:
                    k = j[1].split()
                    inlines = telebot.types.InlineKeyboardMarkup()
                    for l in k:
                        inlines.add(telebot.types.InlineKeyboardButton(text=f"{l}", callback_data=f"{l}"))
                    bot.send_message(call.message.chat.id, f"{call.data}", reply_markup=inlines)
                    if call.data:
                        data[6] = f'{((int(data[6])) - 1)}'
                        file = open(path, "r")
                        read = file.readlines()
                        file.close()
                        lt = []
                        for i in read:
                            j1 = i.split()
                            if data[0] != j1[0]:
                                lt.append(i)
                        lt.append(" ".join(data))
                        file = open(path, "w")
                        file.write("\n".join(lt) + "\n")
                        file.close()
                        trainer = ""
    else:
        bot.send_message(call.message.chat.id, f"You don't have trainer classes please buy them from the menu!",
                         reply_markup=key2)
    bot.send_message(call.message.chat.id, "Done", reply_markup=key2)


bot.polling(none_stop=True, interval=0)
