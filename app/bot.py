import requests
from telebot import TeleBot, types

TOKEN = open("TOKEN.txt").read()

bot = TeleBot(TOKEN)


@bot.message_handler(commands=["помощь", "help", "command", "start"])
def all_commands(message):
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(types.InlineKeyboardButton("Подписка", callback_data="reg"),
                 types.InlineKeyboardButton("Мои подписки", callback_data="my_groups"))
    bot.send_message(message.chat.id,
                     "Есть вот такие команды:\n"
                     "Подписка - подписаться на рассылку расписания группы.\n"
                     "Мои подписки - вывести список групп, на рассылку расписания которых вы подсписаны, с возможнотью отписки.",
                     reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "reg":
        menu = types.InlineKeyboardMarkup()
        faculties = requests.get("http://localhost:8000/faculties/all").json()
        for faculty in faculties:
            menu.add(types.InlineKeyboardButton(faculty["name"], callback_data="fc" + str(faculty["id"])))
        menu.add(types.InlineKeyboardButton("Отмена", callback_data="Cancel"))
        bot.edit_message_text("Факультеты:", call.message.chat.id, call.message.message_id, reply_markup=menu)

    elif call.data.startswith("fc"):
        menu = types.InlineKeyboardMarkup()
        courses = requests.get("http://localhost:8000/courses/all").json()
        for course in courses:
            menu.add(types.InlineKeyboardButton(course["num"], callback_data="c" + str(course["id"]) + "_" + call.data))
        menu.row(types.InlineKeyboardButton("Назад", callback_data=call.data[call.data.find("_") + 1:]),
                 types.InlineKeyboardButton("Отмена", callback_data="Cancel"))
        bot.edit_message_text("Курсы:", call.message.chat.id, call.message.message_id, reply_markup=menu)

    elif call.data.startswith("c"):
        menu = types.InlineKeyboardMarkup()
        forms = requests.get("http://localhost:8000/forms/all").json()
        for form in forms:
            menu.add(types.InlineKeyboardButton(form["type"], callback_data="fr" + str(form["id"]) + "_" + call.data))
        menu.row(types.InlineKeyboardButton("Назад", callback_data=call.data[call.data.find("_") + 1:]),
                 types.InlineKeyboardButton("Отмена", callback_data="Cancel"))
        bot.edit_message_text('Формы:', call.message.chat.id, call.message.message_id, reply_markup=menu)

    elif call.data.startswith("fr"):
        menu = types.InlineKeyboardMarkup()
        data = call.data.split(sep="_")
        form_id = int(data[0][2:])
        course_id = int(data[1][1:])
        faculty_id = int(data[2][2:])
        groups = requests.get("http://localhost:8000/groups/sorted",
                              json={"faculty_id": faculty_id, "course_id": course_id, "form_id": form_id}).json()
        for group in groups:
            twink = False
            for user in group["users"]:
                if user["chat_id"] == call.message.chat.id:
                    twink = True
                    break
            if not twink:
                menu.add(types.InlineKeyboardButton(group["name"], callback_data="gr" + str(group["id"])))
        menu.row(types.InlineKeyboardButton("Назад", callback_data=call.data[call.data.find("_") + 1:]),
                 types.InlineKeyboardButton("Отмена", callback_data="Cancel"))
        bot.edit_message_text('Группы с такими данными', call.message.chat.id, call.message.message_id,
                              reply_markup=menu)

    elif call.data.startswith("gr"):
        requests.post("http://localhost:8000/users", json={"chat_id": call.message.chat.id, "group_id": call.data[2:]})
        bot.edit_message_text("Подписка выполнена успешно!", call.message.chat.id, call.message.message_id)

    elif call.data == "Cancel":
        bot.edit_message_text(
            "Регистрация отменена. Если вы не нашли свою группу, значит либо её пока нет, либо вы уже подписаны на неё,"
            " либо вы ввели некорректные данные.", call.message.chat.id,
            call.message.message_id)

    elif call.data == "my_groups":
        menu = types.InlineKeyboardMarkup()
        users = requests.get(f"http://localhost:8000/users/by_tele/{call.message.chat.id}").json()
        if users:
            for user in users:
                menu.add(
                    types.InlineKeyboardButton(user["group"]["name"], callback_data="del" + str(user["group"]["id"])))
            bot.edit_message_text("Список групп, нажмите для удаления:", call.message.chat.id, call.message.message_id,
                                  reply_markup=menu)
        else:
            bot.edit_message_text("У вас нет подписок.", call.message.chat.id, call.message.message_id)

    elif call.data.startswith("del"):
        group_id = call.data[3:]
        requests.delete("http://localhost:8000/users/sorted",
                        json={"chat_id": call.message.chat.id, "group_id": group_id})
        bot.edit_message_text("Вы отписались от группы.", call.message.chat.id, call.message.message_id)


bot.polling(none_stop=True)
