import openai
import pkg_resources
import re
import json
import sqlite3
import string
import random
from time import strftime, localtime

from telegram import Bot
from telegram.utils.request import Request
from telegram.ext import MessageHandler, Filters, Updater

YELLOW = "\033[93m"
RED = "\033[91m"
END = "\033[0m"


class Engine(object):

    def __init__(self, telegram_token: str = None, openai_key: str = None, bot_name: str = "Bot-GPT"):
        # internal variables
        self.name = bot_name
        self.ver = pkg_resources.get_distribution("telegram-bot-gpt").version
        self.db = "bot_gpt.db"

        db, cr = self.get_data("chats", col="id", param="ORDER BY id DESC LIMIT 1")
        num = cr.fetchone()
        self.num_chats = 0 if num is None else num[0]

        db, cr = self.get_data("users", "uid, daily_allowed, adm")
        users = [c for c in cr.fetchall()]
        self.admin = [user[0] for user in users if user[2] > 0]

        self.setting = DEFAULT_SETTING.copy()
        db, cr = self.get_data("setting", "var, val")
        setting = {c[0]: c[1] for c in cr.fetchall()}
        for key in setting:
            self.setting[key] = int(setting[key]) if setting[key].isnumeric() else setting[key]
        self.set(self.setting.keys(), self.setting.values())

        # OpenAI
        self.openai_key = openai_key

        # Telegram bot setting
        self.telegram_token = telegram_token
        self.bot = None
        if self.telegram_token is not None:
            try:
                self.set_bot(self.telegram_token, bot_name)
            except:
                print(f"{RED}[ERROR] Telegram token cannot be used, bot initialization failed.{END}")
                exit()

        db.close()

    def set_bot(self, telegram_token: str, bot_name: str = None):
        self.bot = Bot(telegram_token, request=Request(con_pool_size=8))
        if bot_name is not None:
            self.name = bot_name
        return True

    def set_botname(self, bot_name: str = "Bot-GPT"):
        self.name = bot_name
        return bot_name

    def reset_botname(self):
        return self.set_botname()

    def set_openai_key(self, openai_key: str):
        self.openai_key = openai_key
        openai.api_key = self.openai_key
        return True

    def del_openai_key(self):
        self.openai_key = None
        openai.api_key = None
        return True

    def set_ai_temperature(self, temp=75):
        if 0 < temp < 1:
            temp *= 100
        temp = int(temp)
        self.set("ai_temperature", temp)
        return temp

    def reset_ai_temperature(self):
        return self.set_ai_temperature()

    def set_memory_length(self, length: int = 3):
        length = min(max(length, 1), 10)
        self.set("memory_length", length)
        return length

    def reset_memory_length(self):
        return self.set_memory_length()

    def set_max_token(self, val: int = 200):
        self.set("max_token", val)
        return val

    def reset_max_token(self):
        return self.set_max_token()

    def set_daily_limit(self, limit: int = None):
        if limit is None:
            limit = 50
        self.set("daily_limit", limit)
        return limit

    def reset_daily_limit(self):
        self.setting["daily_limit"] = 50
        return self.setting["daily_limit"]

    def set_admin_limit(self, limit: int = None):
        if limit is None:
            limit = 50
        self.set("admin_limit", limit)
        return limit

    def reset_admin_limit(self):
        return self.set_admin_limit()

    def add_empty_response(self, resp: str):
        if "; " + resp + ";" not in "; " + self.setting["empty_response"] + ";":
            resp = self.setting["empty_response"] + "; " + resp
            self.set("empty_response", resp)
        return resp

    def reset_empty_response(self):
        resp = DEFAULT_SETTING["empty_response"]
        self.set("empty_response", resp)
        return resp

    def reset_settings(self):
        self.set(DEFAULT_SETTING.keys(), DEFAULT_SETTING.values())
        return True

    def activate_bot(self, status=1):
        status = 0 if status in [0, False] else 1
        self.set("bot_active", status)
        return status == 1

    def deactivate_bot(self):
        return self.activate_bot(status=0)

    def is_bot_active(self):
        return self.setting["bot_active"] == 1

    def new_password(self, char=8):
        password = ''.join(random.choices(string.ascii_lowercase + string.digits, k=char))
        self.set("password", password)
        return password

    def get_password(self):
        return self.get("password")

    def get(self, var: str):
        var = var.lower()
        if var == "password" and len(self.setting["password"]) == 0:
            self.new_password()

        if var in self.setting.keys():
            return self.setting[var]

        return None

    def set(self, variables, values):
        if isinstance(variables, str) and (isinstance(values, str) or isinstance(values, int)):
            variables = [variables]
            values = [values]

        db = sqlite3.connect(self.db, check_same_thread=False)
        cr = db.cursor()
        cr.execute("CREATE TABLE IF NOT EXISTS setting (var TEXT primary key, val TEXT)")

        for var, val in zip(variables, values):
            var = var.replace("'", "''")
            if isinstance(val, str):
                val = val.replace("'", "''")
            self.setting[var] = val
            cr.execute(f"INSERT INTO setting (var, val) VALUES('{var}', '{val}') "
                       f"ON CONFLICT(var) DO UPDATE SET val = '{val}';")

        db.commit()
        db.close()
        return True

    def get_data(self, table: str, col: str = "id", where: str = "", param: str = ""):
        db = sqlite3.connect(self.db, check_same_thread=False)
        cr = db.cursor()

        if len(col) > 0:
            try:
                if len(where) > 0:
                    where = ' WHERE ' + where
                cr.execute(f"SELECT {col} FROM {table}{where} {param}")
            except:
                cr.execute("CREATE TABLE IF NOT EXISTS users "
                           "(id INTEGER, reg TEXT, uid TEXT primary key, unick TEXT,"
                           " daily_allowed TINYINT, adm TINYINT, tokens INT)")
                cr.execute("CREATE TABLE IF NOT EXISTS chats "
                           "(id INTEGER, reg TEXT, uid TEXT, inp TEXT, res TEXT, tokens INT)")
                cr.execute("CREATE TABLE IF NOT EXISTS setting (var TEXT primary key, val TEXT)")

        return db, cr

    def start(self, uid, unick: str = None):
        if unick is None:
            unick = "---"
        server_time = strftime("%d.%m.%Y %H:%M:%S", localtime())

        i_am_admin = self.admin.count(uid)

        db, cr = self.get_data("users", "id, uid")
        rows = [c for c in cr.fetchall()]
        uids = []
        for r in rows:
            uids.append(r[1])
        last_id = rows[-1][0] if len(rows) > 0 else 0

        if str(uid) not in uids:
            limit = 0
            if len(uids) == 0:
                i_am_admin = 1

            if i_am_admin == 1:
                self.admin.append(uid)
                limit = self.setting["admin_limit"]
                self.activate_bot()

            query = f"INSERT INTO users(id, reg, uid, unick, daily_allowed, adm, tokens) " \
                    f"VALUES({last_id + 1}, '{server_time}', '{uid}', '{unick}', {limit}, {i_am_admin}, 0)"
            cr.execute(query)
            db.commit()

        db.close()

        if i_am_admin == 1:
            password = self.setting["password"]
            if len(password) == 0:
                password = self.new_password()

            text = f"You are *admin* of {self.name}.\n\n" \
                   f"All users will require a password before using this bot, " \
                   f"to modify send /new\_password, while /get\_password displays it.\n\n" \
                   f"The current password is:"

            self.bot.send_message(uid, text=text, parse_mode="Markdown")
            self.bot.send_message(uid, text=f"`{password}`", parse_mode="Markdown")

        else:
            self.bot.send_message(uid, text=f"`To use this bot, please enter the *password* set by admin.`",
                                  parse_mode="Markdown")

        return "ok"

    def command(self, message):
        uid = str(message.chat.id)
        inp = message.text.lower()[1:]
        text = None

        if inp == "start":
            unick = message.chat.username
            return self.start(uid, unick)

        if inp == "help":
            text = read_file("help_admin.txt" if uid in self.admin else "help_user.txt")
            text = text.replace("{self.name}", f"{self.name}")
            text = text.replace("{self.ver}", f"{self.ver}")

        elif inp == "disclaimer":
            text = read_file("disclaimer.txt")

        elif inp == "is_bot_active":
            text = "✅ `Yes, bot is active.`" if self.is_bot_active() else "❌ `No, bot is *not* active.`"

        if uid in self.admin:
            if inp == "usage":
                # time = strftime("%d.%m.%Y %H:%M:%S", localtime())
                db, cr = self.get_data("chats", col="reg", param="ORDER BY id DESC LIMIT 1")
                time = cr.fetchone()
                if time is None:
                    self.bot.send_message(uid, text="`No record found in database.`", parse_mode="Markdown")
                    return "ok"

                db, cr = self.get_data("chats", col="uid, tokens", where=f"reg LIKE '{time[0][:10]}%'")
                rows = [c for c in cr.fetchall()]
                db.close()

                if len(rows) == 0:
                    text = "`[Empty]`"
                else:
                    uids = []
                    chats = {}
                    tokens = {}
                    for r in rows:
                        if r[0] not in tokens:
                            uids.append(r[0])
                            chats[r[0]] = 0
                            tokens[r[0]] = 0

                        chats[r[0]] += 1
                        tokens[r[0]] += r[1]

                    text = "\n".join(f"`{u}: {chats[u]} chats, {tokens[u]} tokens`" for u in uids)

            elif inp.endswith("password"):
                if re.match(r"^(get_)?password$", inp):
                    self.bot.send_message(uid, text=f"`{self.get_password()}`", parse_mode="Markdown")
                    text = "To create a new one, send /new\_password to the bot.\n\n" \
                           "Use /reset\_password to change it, forcing all existing users re-entering the new one."

                elif re.match(r"^(new|reset)_password$", inp):
                    if inp.startswith("reset"):
                        db, cr = self.get_data("users", col="")
                        cr.execute(f"UPDATE users set daily_allowed=-1 WHERE adm=0")
                        db.commit()
                        db.close()
                        self.bot.send_message(uid, parse_mode="Markdown",
                                              text="Password is reset, now all users should re-enter the new one:")

                    else:
                        self.bot.send_message(uid, text="Password is renewed:", parse_mode="Markdown")

                    text = f"`{self.new_password()}`"

            elif re.match("^(de)?activate(_bot)?$", inp):
                status = 0 if inp.startswith("de") else 1
                self.activate_bot(status=status)
                text = f"`Bot successfully {inp.split('_')[0]}d.`"

            if text is None:
                text = f"`Unknown bot command:\n/{inp}`"

        else:  # not admin, no matching command
            text = f"`Unknown bot command:\n/{inp}`"

        if text is None:
            unick = message.chat.username
            self.start(uid, unick)
            return self.command(message)

        self.bot.send_message(uid, text=text, parse_mode="Markdown")

        return "ok"

    def respond(self, message):
        uid = str(message.chat.id)
        inp = message.text

        if uid not in self.admin:
            db, cr = self.get_data("users", "uid, daily_allowed", f"uid='{uid}'")
            found = [c for c in cr.fetchall()]
            db.close()

            if len(found) == 0:
                unick = message.chat.username
                return self.start(uid, unick)

            is_allowed = found[-1][1]
            if is_allowed < 1:
                db, cr = self.get_data("users", col="")
                ret = "not ok"
                if inp == self.setting["password"]:
                    daily_allowed = self.setting["daily_limit"]
                    cr.execute(f"UPDATE users set daily_allowed={daily_allowed} WHERE uid='{uid}'")
                    db.commit()
                    text = f"🙂\n_Welcome to {self.name}_,\nIt is recommended to read /help before starting a chat!"
                    ret = "ok"

                elif is_allowed < 0:
                    cr.execute(f"UPDATE users set daily_allowed=0 WHERE uid='{uid}'")
                    db.commit()
                    text = "`Bot is reset by admin.\nTo continue using it, please enter the *new password*.`"

                self.bot.send_message(uid, text=text, parse_mode="Markdown")
                db.close()
                return ret

        if self.openai_key is None:
            self.send_error_report(uid, "No API key provided")
            return "not ok"

        # date = message.date

        if inp is None or len(inp) == 0:
            return "not ok"

        time = strftime("%d.%m.%Y %H:%M:%S", localtime())

        db, cr = self.get_data("chats", col="inp, res", where=f"uid='{uid}' AND reg LIKE '{time[:10]}%'")
        rows = [c for c in cr.fetchall()]
        if uid not in self.admin:
            check = len(rows)
            if check > self.setting["daily_limit"]:
                daily_limit = self.setting["daily_limit"]
                self.bot.send_message(uid, f"`Daily limit of {daily_limit} chats reached. Come back tomorrow.`",
                                      parse_mode="Markdown")
                return "ok"

        prompt = re.sub("  +", " ", inp.strip())
        words_num = len(re.findall("[A-Za-z0-9-']+", prompt))
        mem = self.setting["memory_length"] if words_num <= 3 else 1 if words_num <= 9 else 0
        messages = []
        if words_num < 4:
            for r in rows[-mem:]:
                messages.extend([{"role": "user", "content": r[0]}, {"role": "assistant", "content": r[1]}])
        messages.append({"role": "user", "content": prompt})

        self.bot.send_chat_action(uid, "typing")

        # print(prompt)
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=self.setting["max_token"],
                stop=None,
                temperature=self.setting["ai_temperature"] / 100,
            )
            response = resp.choices[0].message["content"]
            tokens = resp["usage"]["total_tokens"]
            # print(answer)

        except Exception as e:
            self.send_error_report(uid, str(e))
            return "not ok"

        self.bot.send_message(uid, response, parse_mode="Markdown")

        esc_inp = inp.replace("'", "''")
        esc_res = response.replace("'", "''")
        self.num_chats += 1
        query = f"INSERT INTO chats (id, reg, uid, inp, res, tokens) " \
                f"VALUES({self.num_chats}, '{time}', '{uid}', '{esc_inp}', '{esc_res}', {tokens})"
        cr.execute(query)

        cr.execute(f"SELECT tokens FROM users where uid = '{uid}'")
        prev_tokens = cr.fetchone()[0]
        cr.execute(f"UPDATE users SET tokens = {prev_tokens + tokens}")
        db.commit()

        try:
            db.close()
        except:
            pass

        return "ok"

    def send_error_report(self, uid, report, send=True):
        text = None
        status = "admin" if uid in self.admin else "user"

        for key in ERRORS:
            if report.startswith(key):
                text = ERRORS[key][status]
                break

        if text is None:
            text = ERRORS["Unknown error"][status]

        if send:
            self.bot.send_message(uid, text=f"`{text}`", parse_mode="Markdown")

        return text

    @staticmethod
    def help():
        help_dev()

    def run(self):
        try:
            updater = Updater(bot=self.bot)
        except:
            print(f"{RED}[ERROR] You have not provided a required Telegram bot token.{END}\n")
            help_dev("all")
            exit()

        dispatcher = updater.dispatcher

        def process(data, _):
            message = data.message
            self.respond(message)
            return "ok"

        def command(data, _):
            message = data.message
            self.command(message)
            return "ok"

        dispatcher.add_handler(MessageHandler(Filters.command, command, run_async=True))
        dispatcher.add_handler(MessageHandler(Filters.text, process, run_async=True))
        dispatcher.add_handler(MessageHandler(Filters.sticker, process, run_async=True))

        print(f"{self.name} ready.\n")

        if self.openai_key is None:
            print(f"{YELLOW}[WARNING] You have not provided a required OpenAI key.{END}\n")
            help_dev("OpenAI")

        updater.start_polling()
        updater.idle()
        pass


def read_file(filename: str):
    with open(pkg_resources.resource_filename(__name__, filename), "r", encoding="utf-8") as file:
        return file.read()


def help_dev(what="full"):
    text = read_file("help_dev.txt")
    if what == "Telegram":
        text = text.split("\n\n")[-3]
    elif what == "OpenAI":
        text = text.split("\n\n")[-2]
    elif what == "all":
        text = "\n\n".join(text.split("\n\n")[-3:-1])

    print(text)


DEFAULT_SETTING = json.loads(read_file("setting.json"))
ERRORS = json.loads(read_file("alerts.json"))["errors"]

if __name__ == '__main__':
    help_dev()
