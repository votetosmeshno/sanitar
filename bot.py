import telebot
import config
import random
import datetime
import json
import sqlite3
import re


BOT_ID = 1117294158

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(message, "Добрый день, я главный санитар психиатрической лечебницы №4. "
                          "Вы можете общаться со мной вместо своих вымышленных друзей. Для подробной информации нажми /help@privatedurkabot.")


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.reply_to(message,
                 'У главного санитара есть несколько функций. Примите ваши таблетки и наслаждайтесь.\nДля начала каждому нужно стать на учет (в ряды пациентов '
                 'лечебницы) командой /register.\nПосле этого вы можете выбрать психопата дня /todayspsycho и пару дня /psychoshipper\nЕще я ставлю диагноз по команде /diagnosis, ты можешь вылечится приняв таблетку /takeapill, если повезет и примешь ту - можешь смело ставить себе новый диагноз! Здоровых у нас нет\nЯ могу сохранить себе в базу твою легендарную цитату. Для этого реплайни сообщение с тем, что хочешь сохранить командой /save. Бот выводит случайные цитаты пациентов по каманде /quote.')



@bot.message_handler(commands=['request'])
def send_updates(message):
    bot.reply_to(message, f'username: {message.from_user.username}\nuser id: {message.from_user.id}')

@bot.message_handler(commands=['contact'])
def send_contact(message):
    bot.reply_to(message, 'Бот создан @votetosmeshno. С идеями и вопросами - велкам!\nКстати, можете подписатся на ее канал @rarezhanna\ngithub.com/votetosmeshno/sanitar')


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
    write_to_json_todayspsycho(now.strftime("%m/%d/%Y"), psycho['username'], message.chat.id)

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
    if ship1 == None:
        randomshipper(message)
        return
    if ship2 == None:
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

def write_to_json_birthday(date, user_id, username, chat_id):
    with open('birthday.json', 'r') as jfr:
        jf_file = json.load(jfr)
    with open('birthday.json', 'w') as jf:
        jf_target = jf_file[0]['birthday']
        birthday_info = {'date': date, 'user_id': user_id, 'username': username, 'chat_id': chat_id}
        jf_target.append(birthday_info)
        json.dump(jf_file, jf, indent=4)

@bot.message_handler(commands=['birthdayinfo'])
def birthdayinfo(message):
    bot.send_message(message.chat.id, 'Если вы хотите создать список с датами рождения пациентов и получать уведомления-напоминания в чате я могу вам помочь!\n'
                              'Для этого, пожалуйста, напишите в чат сообщение с командой /birthday и датой вашего рождения в формате MM/DD/YY.\nМЕСЯЦ\nДЕНЬ\nГОД\nНапример: /birthday 01/02/03 для 2 января 2003 года\nПостарайтесь не ошибится хотя бы тут.')

@bot.message_handler(commands=['birthday'])
def birthday(message):
    f = open('birthday.json')
    data = json.load(f)
    for l in data:
        for d in l["birthday"]:
            if d["username"] == message.from_user.username and d["chat_id"] == message.chat.id and d["user_id"] == message.from_user.id:
                bot.reply_to(message, "Я и с первого раза запомнил дату твоего рождения!")
                return
    dateofbirth = re.findall("^/birthday (.+)", message.text)[0].strip()
    write_to_json_birthday(dateofbirth, message.from_user.id, message.from_user.username, message.chat.id)
    bot.reply_to(message, "Теперь я знаю твою дату рождения!")



@bot.message_handler(commands=['diagnosis'])
def diagnosis(message):
    f = open('pills.json')
    data = json.load(f)
    for l in data:
        for d in l["pills"]:
            if d["username"] == message.from_user.username and d["chat_id"] == message.chat.id and d["pills"] == "0":
                f = open('diagnosis.json')
                data = json.load(f)
                for l in data:
                    for d in l["diagnosis"]:
                        now = datetime.date.today()
                        if d["username"] == message.from_user.username and d["chat_id"] == message.chat.id:
                            yourtodaysdiagnosis = d["diagnosis"]
                            bot.reply_to(message, f'Ты еще не вылечился:(\n У тебя {yourtodaysdiagnosis}')
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
    bot.reply_to(message, f'Проанализировав твои сообщения, нетрудно догадаться, что твой диагноз - {todaysdiagnosis}.\nПопробуй вылечится приняв таблетку /takeapill')
    now = datetime.date.today()
    write_to_json_diagnosis(message.from_user.username, now.strftime("%m/%d/%Y"), message.chat.id, todaysdiagnosis)


def write_to_json_pills(day, username, user_id, chat_id, pills):
    with open('pills.json', 'r') as jfr:
        jf_file = json.load(jfr)
    with open('pills.json', 'w+') as jf:
        jf_target = jf_file[0]['pills']
        pills_info = {'day': day, 'username': username, 'user_id': user_id, 'chat_id': chat_id, 'pills': pills}
        jf_target.append(pills_info)
        json.dump(jf_file, jf)



@bot.message_handler(commands=['takeapill'])
def take_a_pill(message):
    f = open('pills.json')
    data = json.load(f)
    for l in data:
        for d in l["pills"]:
            now = datetime.date.today()
            if d["username"] == message.from_user.username and d["day"] == now.strftime("%m/%d/%Y") and d[
                "chat_id"] == message.chat.id:
                bot.reply_to(message, 'Ты сегодня уже принимал таблетку!\nПродолжим лечение завтра!')
                return


    amountofpills = random.randrange(1, 11)
    if amountofpills <= 8:
        bot.reply_to(message, 'Кажется ты принял не ту таблетку :(\nПопробуй завтра')
        now = datetime.date.today()
        write_to_json_pills(now.strftime("%m/%d/%Y"), message.from_user.username, message.from_user.id, message.chat.id,
                            '0')
        return
    else:
        bot.reply_to(message, 'Ура! Ты принял правильную таблетку!\nНо даже не думай, что ты вылечил все свои беды с башкой...')
        now = datetime.date.today()
        write_to_json_pills(now.strftime("%m/%d/%Y"), message.from_user.username, message.from_user.id, message.chat.id, '1')
        return


@bot.message_handler(commands=['stats'])
def get_stats(message):
    f = open('diagnosis.json')
    data = json.load(f)
    for l in data:
        for d in l["diagnosis"]:
            if d["username"] == message.from_user.username and d["chat_id"] == message.chat.id:
                cured = d["diagnosis"]
                bot.reply_to(message, f'За время прибывания в лечебнице ты успел вылечить: {cured}')
                return


@bot.message_handler(content_types=['new_chat_participant'])
def greetings(message):
    bot.reply_to(message, 'Добро пожаловать в нашу частную лечебницу!\n Тебе следует записать себя в список пациентов командой /register\nМожешь узнать обо мне больше по команде /help')




@bot.message_handler(commands=['quote'])
def send_quote(message):
    f = open('quotes.json')
    data = json.load(f)
    for l in data:
        for d in l["quotes"]:
            randomquote = random.choice(l['quotes'])
            bot.reply_to(message, f"{randomquote['username']} однажды сказал:\n\n{randomquote['message']}")
            return


def write_to_json_quotes(username, message):
    with open('quotes.json', 'r') as jfr:
        jf_file = json.load(jfr)
    with open('quotes.json', 'w') as jf:
        jf_target = jf_file[0]['quotes']
        quotes_info = {'username': username, 'message': message}
        jf_target.append(quotes_info)
        json.dump(jf_file, jf, indent=4)


@bot.message_handler(content_types=['text'])
def random_text(message):
    con = sqlite3.connect('mydatabase.db')
    cursorObj = con.cursor()

    cursorObj.execute("CREATE TABLE IF NOT EXISTS messages(chat_id integer, message text, user_id integer)")

    con.commit()

    def sql_insert(con, info):

        cursorObj = con.cursor()

        cursorObj.execute('''INSERT INTO messages(chat_id, message, user_id) VALUES(?, ?, ?)''', info)

        con.commit()

    info = (message.chat.id, message.text, message.from_user.id)

    sql_insert(con, info)

    con = sqlite3.connect('mydatabase.db')
    cursorObj = con.cursor()

    random_choice = cursorObj.execute(f"SELECT message FROM messages WHERE chat_id == {message.chat.id} ORDER BY random() LIMIT 1;")
    random_choice = cursorObj.fetchone()

    randomchoice = random.randrange(0, 100)
    if randomchoice < 2:
        bot.send_message(message.chat.id, random_choice)




    randomtextlist = ["кажется, ты глупый", "думаю, тебе вообще не стоит открывать рот", "ты точно не забыл принять свои таблетки сегодня?",
                      "я могу посоветовать тебе отличного психотерапевта", "в дурку его!", "с кем ты говоришь? тут никого нет", "с моим хомяком говорить интереснее чем с тобой",
                      "ты что опять придумал себе друзей?", "ты - мой любимый пациент", "и тебя вылечим", "ничего, говорят и с таким жить можно",
                      "вообще то в нашей лечебнице нельзя так выражаться!", "мне нравится как ты справляешься со своими бедами с башкой!", "ну вот, опять твои голоса в голове",
                      "не думаю что твоя мама была бы рада это услышать", "не сразил коронавирус - сразит твоя шиза", "вы мертвы", "это была ловушка санитара",
                      "я даже не знаю как на это реагировать", "ты как смирительную рубашку снял?", "меня не предупреждали, что ты такой буйный",
                      "опять ты в свои воображаемые игры играешь...", "ну тут только бог поможет", "а ты почему лабки не сделал?", "ну а что вы хотели? в дурке живем",
                      "мем получился очень семейный, а главное религиозный", "быдло", "в таких моментах не стоит ничего говорить, а только кинуть загадочный взгляд "
                      "в мексиканской шляпе", "ха-ха либераху порвало", "ты беспонтовый пирожок", "ясно, автору 0 лет", "осуждаю", "ищи себя в прошмандовках Азейбайджана",
                      "чем больше женщину мы любим тем больше меньше мы тем чем", "мораль думайте сами", "а пацанчик то реально умер", "а вот это я понимаю мем про каждого из нас!",
                       "постирония - это шутка, но не шутка. это такие пикчи с чувачками, которые якобы показывают искренность, но нет! братан, постирония - это шутка не шутка. подколы "
                       "типа автору 8 или 100 лет. рофл, сарказм - синонимы к этому слову. пойми, постирония это не твои картинки с говном.", "братан, я в своем "
                       "сознании сейчас так преисполнился...", "у тебя отличное чувство юмора", "а ты хорош", 'твои родители случайно не родители?', 'а ты мне нравишься!']
    if randomchoice == 4:
        bot.reply_to(message, random.choice(randomtextlist))
    f = open('lastTimePlayed.json')
    data = json.load(f)
    for l in data:
        for d in l["todayspsycho"]:
            now = datetime.date.today()
            if message.from_user.username == d["username"] and message.chat.id == d["chat_id"] and d["day"] == now.strftime("%m/%d/%Y"):
                randomchoice = random.randrange(0, 100)

                randomreplytopsycho = ["лови психопата!", "никто не забыл, что это психопат дня?", "психопатов тут не любят", "не зря ты тут психопат дня",
                                       "а ты свои таблетки принял?", "да, ты точно психопат", "попался! псих!", "ты зачем из палаты убежал?", "а ты сегодня буйный",
                                       "ты самый крутой психопат дня которого я видел", "думал все забыли что ты психопат дня?", "напоминаю! этот юзер - психопат дня",
                                       "ты смотри, как психопат дня разбушевался", "психопат дня сегодня не справляеься со своей шизой",
                                       "а твои голоса в голове сказали тебе, что ты будешь психопатом дня?", "ты мой любимый психопатик", 'я вижу у тебя сегодня удачный день!', 'ты хороший человек, как ты сюда попал?']
                if randomchoice < 2:
                    bot.reply_to(message, random.choice(randomreplytopsycho))
    if ("дурка" in message.text.lower() or "дурку" in message.text.lower() or "дурке" in message.text.lower()):
        bot.reply_to(message, 'А дурка тут!')
    if ("санитар" in message.text.lower() or "санитару" in message.text.lower() or "санитара" in message.text.lower()):
        bot.reply_to(message, 'Санитар на месте.')


    if message.text == "/save" and message.reply_to_message is not None:
        if message.reply_to_message.text == None:
            bot.reply_to(message, "Я не могу сохранить это сообщение.")
            return
        elif message.reply_to_message.text[0] == "/":
            bot.reply_to(message, "Мне незачем сохранять сообщение-команду")
            return
        elif message.reply_to_message.from_user.username == None:
            bot.reply_to(message, "Я не смогу правильно процитировать это чудесное сообщение, ведь у автора нет юзернейма")
            return
        else:
            write_to_json_quotes(message.reply_to_message.from_user.username, message.reply_to_message.text)
            bot.reply_to(message, "Я запомнил!")
            return

    angryuser = ['не кричи на меня так, я еще маленький', "я еще только учусь и обещаю быть лучше", "сквернословие - грех", "я обещаю тебе больше так не делать", "чем я тебя обидел?"]


    if ("отстань" in message.text.lower() or "пошел нахуй" in message.text.lower() or "иди нахуй" in message.text.lower() or "заебал" in message.text.lower() or "нахуй" in message.text.lower() or "сука" in message.text.lower()) and message.reply_to_message.from_user.id == BOT_ID:
        bot.reply_to(message, random.choice(angryuser))
        return











bot.polling()