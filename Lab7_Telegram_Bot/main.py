# ТЗ по боту:
#  1) Формат имени (готово)
#  2) Манера общения = "На вы" (готово)
#  3) Использование бд PostgreSQL (готово)
#  4) Использование данной апи (готово)
#  5) Использование psycopg2 (готово)
#  6) Формат вывода расписания на каждый день недели:
#     < День недели>
#     < Предмет > < Кабинет > < Время > < Преподаватель >
#     ...
#  7) Во время работы бота должны быть отображены следующие графические кнопки: (готово)
#     Понедельник
#     Вторник
#     Среда
#     Четверг
#     Пятница 
#     Расписание на текущую неделю
#     Расписание на следующую неделю
#  8) При нажатии на кнопку с днём недели бот должен выводить информацию из бд
#  с расписанием на выбранный день текущий недели
#  9) При нажатии на кнопку "Расписание на текущую неделю" бот должен выводить
#  информацию из бд с расписанием на всю текущую неделю
#  10) При нажатии на кнопку "Расписание на следующую неделю" бот должен выводить
#  информацию из бд с расписанием на всю следующую неделю
#  11) Команда /week - вывод недели на данный момент - верхняя/нижняя (готово)
#  12) Команда /mtuci - ссылка на mtuci.ru (готово)
#  13) Команда /help - вывод краткой информации о себе, краткой документации и
#  список команд (готово готово)
#  (ГОТОВО) 14) При вводе неизвестной команды или неизвестного боту сообщения, бот должен
#  отправлять сообщение - "Извините, я Вас не понял" 
#  (ГОТОВО) 15) Структура бд должна соответствовать схеме в методичке
import telebot, psycopg2, datetime
from telebot import types


token = "5822901262:AAGaQ65BSEimFLHxnSZcjLqzvike8PD2aM0"
bot = telebot.TeleBot(token)

conn = psycopg2.connect(database="telebot",
                        user="postgres",
                        password="A048kp46",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()

nums = int(datetime.datetime.utcnow().isocalendar()[1])

def even_week(nums):
    if nums % 2 == 0:
        return 'чётная'
    else:
        return 'нечётная'

def day_schedule(day, week):
    cursor.execute("select subject, room_numb, start_time from timetable where day=%s and week=%s order by id",
                   [str(day), str(week)])
    records = cursor.fetchall()
    string = ''

    if records:
        for i in records:
            subject, room_numb, start_time = i[0], i[1], i[2]
            cursor.execute("select full_name from teacher where subject=%s", [str(subject)])
            full_name = cursor.fetchall()
            string += str(subject) + '  Кабинет №' + str(room_numb) + '  Начало: ' + str(start_time) + ' Преподаватель: ' \
            + str(full_name[0][0]) + '\n'
    else:
        string = 'Занятий нет' + '\n'

    return string

def week_schedule(week):
    days = ['Понедельник','Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
    days_db = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб']
    string = ''
    for i in range(len(days)):
        string += str(days[i]) + " :\n" + day_schedule(str(days_db[i]), even_week(week)) + '\n'

    return string


@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup() #Класс создаёт кастом клавиаутуру с текстовыми кнопками вместо обычной клавы 
    # Заполняет кастом клаву кнопками
    keyboard.row("Расписание на текущую неделю")
    keyboard.row("Расписание на следующую неделю") 
    keyboard.row("Понедельник", "Вторник")
    keyboard.row("Среда", "Четверг")
    keyboard.row("Пятница", "Суббота")
    bot.send_message(message.chat.id, 'Здравствуйте! Хотите узнать свежую информацию о МТУСИ?', reply_markup=keyboard)
    # отправляет пользователю сообщение

@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Основная моя функция - отображать расписание, но мои создатели наделили меня \
ещё возможностью вывода текущей недели. Для этого введите /week \nА ещё я могу подсказать место где вы всегда \
сможете узнать свежую информацию о МТУСИ! \nКоманда /mtuci поможет вам в этом')

@bot.message_handler(commands=['week'])
def week(message):
    if nums % 2 == 0:
        bot.send_message(message.chat.id, "Чётная неделя")
    else:
        bot.send_message(message.chat.id, "Нечётная неделя")

@bot.message_handler(commands=['mtuci'])
def mtuci(message):
    bot.send_message(message.chat.id, 'https://mtuci.ru')    

@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() == "хочу":
        bot.send_message(message.chat.id, "Тогда Вам сюда - https://mtuci.ru")
    elif message.text.lower() == 'понедельник':
        bot.send_message(message.chat.id, day_schedule('Пн', even_week(nums)))
    elif message.text.lower() == 'вторник':
        bot.send_message(message.chat.id, day_schedule('Вт', even_week(nums)))
    elif message.text.lower() == 'среда':
        bot.send_message(message.chat.id, day_schedule('Ср', even_week(nums)))
    elif message.text.lower() == 'четверг':
        bot.send_message(message.chat.id, day_schedule('Чт', even_week(nums)))
    elif message.text.lower() == 'пятница':
        bot.send_message(message.chat.id, day_schedule('Пт', even_week(nums)))
    elif message.text.lower() == 'суббота':
        bot.send_message(message.chat.id, day_schedule('Сб', even_week(nums)))
    elif message.text.lower() == 'расписание на текущую неделю':
        bot.send_message(message.chat.id, week_schedule(nums))
    elif message.text.lower() == 'расписание на следующую неделю':
        bot.send_message(message.chat.id, week_schedule(nums + 1))
    else:
        bot.send_message(message.chat.id, "Простите, я не знаю такой команды")

bot.polling(none_stop=True, interval=0)
