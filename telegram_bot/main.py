

from telebot import TeleBot
from config import token
import SQLtool


def telegram_bot(token):
    bot = TeleBot(token)
    sql = SQLtool.SQL()
    error = "error"

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(message.chat.id, "Привет, это "\
                                          "студенческий проект для игры пиксель арт"\
                                          "нажмите /help для получения информации")

    @bot.message_handler(content_types=["text"])
    def send_text(message):

        if message.text.lower() == "/help":  # COMMAND HELP
            try:
                help = "команды:\n\n" \
                        "/help - данная команда\n\n" \
                        "/reg - начать регистрацию аккаунта для игры\n\n" \
                        "/del - удалить аккаунт для игры\n\n" \
                        "/my - показат мои аккаунты"
                bot.send_message(message.chat.id, help)
            except Exception as ex:
                bot.send_message(message.chat.id, error)

        elif message.text.lower() == "/my":
            try:
                buf = sql.my_accounts(message.chat.id)
                if buf == error:
                    bot.send_message(message.chat.id, "Error with Database.")
                bot.send_message(message.chat.id, "your accounts:")
                bot.send_message(message.chat.id, buf)

            except Exception as ex:
                bot.send_message(message.chat.id, error)

        elif message.text.lower() == "/reg":  # COMMAND REG
            try:
                next_step = bot.send_message(message.chat.id, "Регистрация аккаунта. Введите логин.\nнажмите /exit для закрытия регистрации")
                bot.register_next_step_handler(next_step, set_login)
            except Exception as ex:
                bot.send_message(message.chat.id, error)

        elif message.text.lower() == "/del":
            try:
                next_step = bot.send_message(message.chat.id, "Введите логин от аккаунта.")
                bot.register_next_step_handler(next_step, delete_account)
            except Exception as ex:
                bot.send_message(message.chat.id, error)

        else:
            bot.send_message(message.chat.id, "Данная команда не поддержимается")

    def delete_account(message):
        if sql.is_my_login(message.text, message.chat.id):
            bot.send_message(message.chat.id, "удаление аккаунта.")

            if not sql.delete_account_by_login(message.text):
                bot.send_message(message.chat.id, "Ошибка с БД.")
                bot.clear_step_handler_by_chat_id(message.chat.id)
                return
        else:
            bot.send_message(message.chat.id, "Данный аккаунт не принадлжеит Вам.")

        bot.clear_step_handler_by_chat_id(message.chat.id)

    def set_login(message):  # COMMAND REG №2
        try:
            # print("login:", message.text)

            if message.text.lower() == "/exit":
                bot.clear_step_handler_by_chat_id(message.chat.id)
                return

            if sql.is_special_login(message.text):
                next_step = bot.send_message(message.chat.id, "Хорошо, введите пароль.")
                bot.register_next_step_handler(next_step, set_password, message.text)
            else:
                next_step = bot.send_message(message.chat.id, "Данный логин уже используется.\nВведите логин.")
                bot.register_next_step_handler(next_step, set_login)

        except Exception as ex:
            bot.send_message(message.chat.id, error + "1")

    def set_password(message, login_):  # COMMAND REG №3
        try:
            # print("password:", message.text)

            if not sql.add_account(login_, message.text, message.chat.id):
                bot.send_message(message.chat.id, "Ошибка с БД.")
                bot.clear_step_handler_by_chat_id(message.chat.id)
                return

            bot.send_message(message.chat.id, "Хорошо.")
            bot.clear_step_handler_by_chat_id(message.chat.id)
        except Exception as ex:
            # print(ex)
            bot.send_message(message.chat.id, error + "2")

    bot.polling()


if __name__ == '__main__':
    telegram_bot(token)
