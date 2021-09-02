import datetime
from PIL import Image
import schedule
from telebot import TeleBot, types
import scraper
from settings import BOT_TOKEN, SCHEDULE_TIME, COMICS_TIME, IMG_FORMAT
from models.student_group import GroupStatus
from models.user import UserRole
from servise import user_servises, faculty_servises, course_servises, form_servises, group_servises, static_servises

time_to_send_comics = datetime.time.fromisoformat(COMICS_TIME)
time_to_send_schedule = datetime.time.fromisoformat(SCHEDULE_TIME)
TOKEN = BOT_TOKEN

bot = TeleBot(TOKEN, parse_mode="HTML")


@bot.message_handler(commands=["reg"])
def start(message):
    user = user_servises.get_user(chat_id=message.chat.id)
    if not user:
        user_servises.post_user(chat_id=message.chat.id)
        bot.send_message(message.chat.id, "Я тебя запомнил. Используй /start для взаимодействия со мной.")
    else:
        bot.send_message(message.chat.id,
                         "Не нужно, я тебя уже знаю. Используй /start для взаимодействия со мной.")


@bot.message_handler(commands=["помощь", "help", "command", "start"])
def all_commands(message):
    user = user_servises.get_user(chat_id=message.chat.id)
    if user:
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.add(
            types.InlineKeyboardButton("Подписка", callback_data="reg"),
            types.InlineKeyboardButton("Мои подписки", callback_data="my_groups" + str(user.id))
        )
        if user.get_comics:
            keyboard.add(types.InlineKeyboardButton("Отписаться от получения комиксов", callback_data="rem_comics"))
        else:
            keyboard.add(types.InlineKeyboardButton("Подписаться на получение комиксов", callback_data="get_comics"))
        keyboard.add(
            types.InlineKeyboardButton("Выслать комикс", callback_data="send_comics_to_me"),
            types.InlineKeyboardButton("Выслать расписание", callback_data="send_schedule_to_me" + str(user.id))
        )
        if user.role_code == UserRole.admin.value:
            keyboard.add(
                types.InlineKeyboardButton("Разослать комиксы", callback_data="send_comics_to_all"),
                types.InlineKeyboardButton("Разослать расписание", callback_data="send_schedule_to_all")
            )
            keyboard.add(
                types.InlineKeyboardButton("Обновить и разослать расписание", callback_data="scrap_and_send_schedule"),
                types.InlineKeyboardButton("Обновить комикс", callback_data="scrap_comics")
            )
        bot.send_message(message.chat.id,
                         "Есть вот такие команды:\nПодписка - подписаться на рассылку расписания группы.\n"
                         "Мои подписки - вывести список групп, на рассылку расписания которых ты подсписан"
                         "(с возможнотью отписки).\n"
                         "Комиксы - получать комиксы каждый день.",
                         reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Используйте /reg для создания пользователя.")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "reg":
        menu = types.InlineKeyboardMarkup()
        faculties = faculty_servises.get_all_faculties("name")
        for faculty in faculties:
            menu.add(types.InlineKeyboardButton(faculty.name, callback_data="fc" + str(faculty.id)))
        menu.add(types.InlineKeyboardButton("Отмена", callback_data="Cancel"))
        bot.edit_message_text("Факультеты:", call.message.chat.id, call.message.message_id, reply_markup=menu)

    elif call.data == "send_comics_to_all":
        mail_comics_to_all("Внеплановая рассылка комиксов")
        bot.edit_message_text("Комиксы отправлены.", call.message.chat.id, call.message.message_id)

    elif call.data == "get_comics":
        user_servises.put_user(call.message.chat.id, get_comics=True)
        bot.edit_message_text("Ты подписался на рассылку комиксов", call.message.chat.id, call.message.message_id)

    elif call.data == "rem_comics":
        user_servises.put_user(call.message.chat.id, get_comics=False)
        bot.edit_message_text("Ты отписался от рассылки комиксов", call.message.chat.id, call.message.message_id)

    elif call.data.startswith("fc"):
        menu = types.InlineKeyboardMarkup()
        courses = course_servises.get_courses()
        for course in courses:
            menu.add(types.InlineKeyboardButton(course.num, callback_data="c" + str(course.id) + "_" + call.data))
        menu.row(types.InlineKeyboardButton("Назад", callback_data="reg"),
                 types.InlineKeyboardButton("Отмена", callback_data="Cancel"))
        bot.edit_message_text("Курсы:", call.message.chat.id, call.message.message_id, reply_markup=menu)

    elif call.data.startswith("c"):
        menu = types.InlineKeyboardMarkup()
        forms = form_servises.get_all_forms()
        for form in forms:
            menu.add(types.InlineKeyboardButton(form.type, callback_data="fr" + str(form.id) + "_" + call.data))
        menu.row(types.InlineKeyboardButton("Назад", callback_data=call.data[call.data.find("_") + 1:]),
                 types.InlineKeyboardButton("Отмена", callback_data="Cancel"))
        bot.edit_message_text('Формы:', call.message.chat.id, call.message.message_id, reply_markup=menu)

    elif call.data.startswith("fr"):
        menu = types.InlineKeyboardMarkup()
        data = call.data.split(sep="_")
        form_id = int(data[0][2:])
        course_id = int(data[1][1:])
        faculty_id = int(data[2][2:])
        groups = group_servises.get_groups(faculty_id=faculty_id, course_id=course_id, form_id=form_id)
        for group in groups:
            twink = False
            group_users = group_servises.get_all_link(group.id)
            for group_user in group_users:
                if group_user.user.chat_id == call.message.chat.id:
                    twink = True
                break
            if not twink:
                if group.status == GroupStatus.completed.value:
                    menu.add(types.InlineKeyboardButton(group.name, callback_data="gr" + str(group.id)))
        menu.row(types.InlineKeyboardButton("Назад", callback_data=call.data[call.data.find("_") + 1:]),
                 types.InlineKeyboardButton("Отмена", callback_data="Cancel"),
                 types.InlineKeyboardButton("Создать новую",
                                            callback_data=f"new-group_fc{faculty_id}_c{course_id}_fr{form_id}"))
        bot.edit_message_text('Группы с такими данными', call.message.chat.id, call.message.message_id,
                              reply_markup=menu)

    elif call.data.startswith("gr"):
        user = user_servises.get_user(chat_id=call.message.chat.id)
        group_servises.post_group_user(user.id, int(call.data[2:]))
        bot.edit_message_text("Подписка успешно выполнена!", call.message.chat.id, call.message.message_id)

    elif call.data.startswith("Cancel"):
        bot.edit_message_text(
            "Регистрация отменена. Если ты не нашёл свою группу, значит либо её пока нет, либо ты уже подписан на неё,"
            " либо ты ввел некорректные данные.", call.message.chat.id,
            call.message.message_id)

    elif call.data.startswith("my_groups"):
        menu = types.InlineKeyboardMarkup()
        user_id = call.data[9:]
        group_users = group_servises.get_all_link(user_id=user_id)
        if group_users:
            for group_user in group_users:
                if group_user.group.status_code == GroupStatus.completed.value:
                    menu.add(types.InlineKeyboardButton(group_user.group.name,
                                                        callback_data="del" + str(group_user.group.id)))
                elif group_user.group.status_code == GroupStatus.muted.value:
                    menu.add(
                        types.InlineKeyboardButton(group_user.group.name + "(выкл)",
                                                   callback_data="del" + str(group_user.group.id)))
                elif group_user.group.status_code == GroupStatus.waiting.value:
                    menu.add(
                        types.InlineKeyboardButton(group_user.group.name + "(обр.)",
                                                   callback_data="del" + str(group_user.group.id)))
            bot.edit_message_text("Список групп, нажми для удаления:", call.message.chat.id, call.message.message_id,
                                  reply_markup=menu)
        else:
            bot.edit_message_text("У тебя нет подписок.", call.message.chat.id, call.message.message_id)

    elif call.data.startswith("del"):
        group_id = call.data[3:]
        user = user_servises.get_user(chat_id=call.message.chat.id)
        group_servises.delete_group_user(user.id, group_id)
        bot.edit_message_text("Ты отписался от группы.", call.message.chat.id, call.message.message_id)

    elif call.data.startswith("new-group"):
        data = call.data.split("_")
        message = bot.edit_message_text(
            "Введи название группы:", call.message.chat.id,
            call.message.message_id
        )
        bot.register_next_step_handler(message, finish_new_group, data[1][2:], data[2][1:], data[3][2:])

    elif call.data == "send_comics_to_me":
        bot.edit_message_text("Загрузка...", call.message.chat.id, call.message.message_id)
        mail_comics_ind(call.message.chat.id)
        bot.edit_message_text("Ну раз просишь, то держи:", call.message.chat.id, call.message.message_id)

    elif call.data.startswith("send_schedule_to_me"):
        user = user_servises.get_user(chat_id=call.message.chat.id)
        users_groups = group_servises.get_all_link(user_id=user.id)
        if GroupStatus.completed.value in [item.group.status_code for item in users_groups]:
            bot.edit_message_text("Загрузка...", call.message.chat.id, call.message.message_id)
            mail_schedule_ind(call.data[19:], call.message.chat.id)
            bot.edit_message_text("Всегда пожалуйста:", call.message.chat.id, call.message.message_id)
        else:
            bot.edit_message_text("У тебя нет подписок.", call.message.chat.id, call.message.message_id)

    elif call.data == "send_schedule_to_all":
        mail_schedule_to_all()
        bot.edit_message_text("Расписание отправлено.", call.message.chat.id, call.message.message_id)

    elif call.data == "scrap_comics":
        scraper.get_comic_img()
        bot.edit_message_text("Комикс обновлён.", call.message.chat.id, call.message.message_id)

    elif call.data == "scrap_and_send_schedule":
        scrap_and_send_schedule()
        bot.edit_message_text("Расписание получено и отправлено", call.message.chat.id, call.message.message_id)


def finish_new_group(message, faculty_id, course_id, form_id):
    name = message.text
    group_servises.post_group(name, int(faculty_id), int(course_id), int(form_id), GroupStatus.waiting.value)
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    menu.add(types.KeyboardButton("Да"), types.KeyboardButton("Нет"))
    message = bot.send_message(message.chat.id, "Хочешь сразу подписаться на эту группу?", reply_markup=menu)
    bot.register_next_step_handler(message, subscribe_new_group, name)


def subscribe_new_group(message, name):
    hide_keyboard = types.ReplyKeyboardRemove()
    menu = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    menu.add(types.KeyboardButton("Да"), types.KeyboardButton("Нет"))
    user = user_servises.get_user(chat_id=message.chat.id)
    if message.text == "Да":
        group = group_servises.get_groups(mark="name")[0]
        group_servises.post_group_user(user.id, group.id)
        bot.send_message(message.chat.id, "Готово!", reply_markup=hide_keyboard)
    elif message.text == "Нет":
        bot.send_message(message.chat.id, "Ладно.", reply_markup=hide_keyboard)
    else:
        message = bot.send_message(message.chat.id,
                                   "Кнопки: \"Ну да, ну да...\"\nЕщё раз. Хочешь сразу подписаться на эту группу?",
                                   reply_markup=menu)
        bot.register_next_step_handler(message, subscribe_new_group, name)


def mail_comics_ind(chat_id):
    bot.send_photo(chat_id, open(f"comics.{IMG_FORMAT}", 'rb'))


def mail_schedule_ind(user_id, chat_id):
    group_users = group_servises.get_all_link(user_id=user_id)
    for group_user in group_users:
        img = Image.open(f"schedule_imgs/{group_user.group.name}.{IMG_FORMAT}")
        bot.send_photo(chat_id, img,
                       f"{group_user.group.faculty.name}, {group_user.group.form.type} форма обучения, "
                       f"{group_user.group.course.num} курс, группа {group_user.group.name}")


def mail_schedule_to_all():
    for group in group_servises.get_groups():
        img = Image.open(f"schedule_imgs/{group.name}.{IMG_FORMAT}")
        for group_user in group_servises.get_all_link(group.id):
            bot.send_photo(group_user.user.chat_id, img,
                           f"{group.faculty.name}, {group.form.type} форма обучения, "
                           f"{group.course.num} курс, группа {group.name}")


def mail_comics_to_all(message_text: str = "Держи очередной комикс"):
    users = user_servises.get_users(True)
    for user in users:
        bot.send_photo(user.chat_id, open(f"comics.{IMG_FORMAT}", 'rb'), caption=message_text)


def scrap_and_send_schedule(planned: bool = False):
    for group in group_servises.get_groups(status_code=GroupStatus.completed.value):
        if group.current_schedule != group.last_schedule or planned:
            img = Image.open(f"schedule_imgs/{group.name}.{IMG_FORMAT}")
            for user_group in group_servises.get_all_link(group.id):
                bot.send_photo(user_group.user.chat_id, img, f"{group.faculty.name}, {group.form.type} форма обучения, "
                                                             f"{group.course.num} курс, группа {group.name}")


def scrap_and_send_comics():
    global comics_job
    if static_servises.check_last_date().comics_date < datetime.date.today():
        result = scraper.get_comic_img()
        print(f"[LOG/scraper]: {result}", end="")
        if result:
            print()
            mail_comics_to_all()
            schedule.cancel_job(comics_job)
            comics_job = schedule.every().day.at(time_to_send_comics.isoformat()).do(scrap_and_send_comics())
        else:
            print(", trying again in 5 minutes...")
            schedule.cancel_job(comics_job)
            comics_job = schedule.every().day.at(time_to_send_comics.isoformat()).do(scrap_and_send_comics())


schedule_job = schedule.every(1).hour.do(scrap_and_send_schedule)
comics_job = schedule.every().day.at(time_to_send_comics.isoformat()).do(scrap_and_send_comics)
if __name__ == "__main__":
    if datetime.datetime.now().time() > time_to_send_comics:
        scrap_and_send_comics()
    if datetime.datetime.now().time() > time_to_send_schedule:
        scrap_and_send_schedule(True)
    bot.polling()
