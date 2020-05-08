import telebot
import config
import random
import datetime
import json


bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Добрый день, я главный санитар психиатрической лечебницы №4. "
                          "Вы можете общаться со мной вместо своих вымышленных друзей. Для подробной информации нажми /help@privatedurkabot.")


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.reply_to(message,
                 'У главного санитара есть несколько функций. Примите ваши таблетки и наслаждайтесь.\nДля начала каждому нужно стать на учет (в ряды пациентов '
                 'лечебницы) командой /register.\nПосле этого вы можете выбрать психопата дня /todayspsycho и пару дня /psychoshipper')


@bot.message_handler(commands=['request'])
def send_updates(message):
    bot.reply_to(message, f'username: {message.from_user.username}\nuser id: {message.from_user.id}')


def write_to_json_patients(username, user_id, chat_id):
    with open('patients.json', 'r') as jfr:
        jf_file = json.load(jfr)
    with open('patients.json', 'w') as jf:
        jf_target = jf_file[0]['patients']
        patients_info = {'username': username, 'user_id': user_id, 'chat_id': chat_id}
        jf_target.append(patients_info)
        json.dump(jf_file, jf, indent=4)


@bot.message_handler(commands=['register'])
def register(message):
    f = open('patients.json')
    data = json.load(f)
    for l in data:
        for d in l["patients"]:
            if d["user_id"] == message.from_user.id and d["chat_id"] == message.chat.id:
                bot.reply_to(message, f'Ты уже регистрировался, шизоид!')
                return
    write_to_json_patients(message.from_user.username, message.from_user.id, message.chat.id)
    bot.reply_to(message, 'Теперь ты тоже в списке пациентов!')

def write_to_json_todayspsycho(day, username, chat_id):
    with open('lastTimePlayed.json', 'r') as jfr:
        jf_file = json.load(jfr)
    with open('lastTimePlayed.json', 'w') as jf:
        jf_target = jf_file[0]['todayspsycho']
        todayspsycho_info = {'day': day, 'username': username, 'chat_id': chat_id}
        jf_target.append(todayspsycho_info)
        json.dump(jf_file, jf, indent=4)


@bot.message_handler(commands=['todayspsycho'])
def chooserandomuser(message):
    if message.chat.type == "private":
        bot.reply_to(message, "Эту функцию можно использовать только в групповых чатах!")
        return
    f = open('lastTimePlayed.json')
    data = json.load(f)
    now = datetime.date.today()
    for l in data:
        for d in l["todayspsycho"]:
            if d["day"] == now.strftime("%m/%d/%Y") and d["chat_id"] == message.chat.id:
                thischatpsycho = d["username"]
                bot.reply_to(message, f'Хватит на сегодня одного психопата!\nЭто, кстати, {thischatpsycho}')
                return
    f = open('patients.json')
    data = json.load(f)
    psycho = random.choice(data[0]["patients"])
    if psycho["chat_id"] != message.chat.id:
        chooserandomuser(message)
        return
    bot.reply_to(message, f'Господа душевнобольные! \nПсихопатом дня сегодня особенно проявил себя - @{psycho["username"]}')
    write_to_json_todayspsycho(now.strftime("%m/%d/%Y"), psycho, message.chat.id)

def write_to_json_psychoshipper(day, pair, chat_id):
    with open('lastTimeShipping.json', 'r') as jfr:
        jf_file = json.load(jfr)
    with open('lastTimeShipping.json', 'w') as jf:
        jf_target = jf_file[0]['psychoshipping']
        psychoshipping_info = {'day': day, 'pair': pair, 'chat_id': chat_id}
        jf_target.append(psychoshipping_info)
        json.dump(jf_file, jf, indent=4)

@bot.message_handler(commands=['psychoshipper'])
def randomshipper(message):
    if message.chat.type == "private":
        bot.reply_to(message, "Эту функцию можно использовать только в групповых чатах!")
        return
    f = open('lastTimeShipping.json')
    data = json.load(f)
    now = datetime.date.today()
    for l in data:
        for d in l["psychoshipping"]:
            if d["day"] == now.strftime("%m/%d/%Y") and d["chat_id"] == message.chat.id:
                thischatshipping = d["pair"]
                bot.reply_to(message, f'У нас уже есть пара!\nСовет да любовь!\nСегодня это {thischatshipping}')
                return
    f = open('patients.json')
    data = json.load(f)
    ship1 = random.choice(data[0]["patients"])
    ship2 = random.choice(data[0]["patients"])
    if ship1["chat_id"] != message.chat.id:
        randomshipper(message)
        return
    if ship2["chat_id"] != message.chat.id:
        randomshipper(message)
        return
    if ship1 == ship2:
        randomshipper(message)
        return
    todayspair = f'{ship1["username"]} + {ship2["username"]}'
    bot.reply_to(message,
                 f'Уважаемые пациенты! \nСегодня в нашей лечебнице образовалась новая пара удивительно психически неуравновешеных - '
                 f'@{ship1["username"]} + @{ship2["username"]}.\nВсем шампанского и транквилизаторов! ')

    write_to_json_psychoshipper(now.strftime("%m/%d/%Y"), todayspair, message.chat.id)


def write_to_json_diagnosis(username, day, chat_id, diagnosis):
    with open('diagnosis.json', 'r') as jfr:
        jf_file = json.load(jfr)
    with open('diagnosis.json', 'w') as jf:
        jf_target = jf_file[0]['diagnosis']
        diagnosis_info = {'username': username, 'day': day, 'chat_id': chat_id, 'diagnosis': diagnosis}
        jf_target.append(diagnosis_info)
        json.dump(jf_file, jf, indent=4)



@bot.message_handler(commands=['diagnosis'])
def diagnosis(message):
    f = open('diagnosis.json')
    data = json.load(f)
    for l in data:
        for d in l["diagnosis"]:
            now = datetime.date.today()
            if d["username"] == message.from_user.id and d["day"] == now.strftime("%m/%d/%Y") and d["chat_id"] == message.chat.id:
                yourtodaysdiagnosis = d["diagnosis"]
                bot.reply_to(message, f'Мы сегодня уже установили тебе диагноз...\nУ тебя явно {yourtodaysdiagnosis}')
                return

    diagnosislist = ["депрессивное расстройство", "деменция", "биполярное расстройство", "шизофрения", "деменция",
                     "аутизм", "алкогольное слабоумие", "аффективный психоз", "алкогольный бред ревности",
                     "алкогольный галлюциноз", "бессонница неорганического происхождения", "болезнь Альцгеймера",
                     "болезнь Брике", "болезнь Пика", "булимия", "галлюциноз",
                     "гиперкинез с задержкой развития", "головная боль напряжения", "дезинтегративный психоз",
                     "делирий", "синдром деперсонализации-дереализации",
                     "депрессия", "дислексия", "наркомания", "алкоголизм", "идиотия",
                     "изменение личности или познавательной способности на почве органического поражения головного мозга",
                     "имбецильность", "индуцированный психоз", "ипохондрия", "истерический психоз",
                     "катастрофический стресс", "мазохизм", "маниакально-депрессивный психоз",
                     "меланхолия", "нарушение сексуальной роли", "наркотический психоз", "неврастения",
                     "нервная анорексия", "обсессивно-компульсивное расстройство", "онейрофрения",
                     "острый бред", "отставание в арифметике специфическое", "отставание в чтении специфическое",
                     "паническое состояние", "параноидный психоз  психогенный",
                     "парафрения", "педофилия", "пограничное расстройство личности", "псевдошизофрения", "психоневроз",
                     "расстройство личности аффективное",
                     "расстройство личности ананкастическое", "расстройство личности астеническое",
                     "расстройство личности аффективное", "расстройство личности истерическое",
                     "расстройство личности шизоидное", "расстройство речевого развития", "садизм",
                     "сексуальные отклонения и расстройства", "сенситивный бред отношения",
                     "синдром Дауна", "синдром Ганзера", "состояние спутанности сознания", "тревожные состояния",
                     "шизофренический психоз", "эпилептическое слабоумие"]


    todaysdiagnosis = random.choice(diagnosislist)
    bot.reply_to(message, f'Проанализировав твои сообщения, нетрудно догадаться, что твой диагноз - {todaysdiagnosis}')
    now = datetime.date.today()
    write_to_json_diagnosis(message.from_user.id, now.strftime("%m/%d/%Y"), message.chat.id, todaysdiagnosis)

bot.polling()
