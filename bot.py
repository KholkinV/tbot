import telebot
from telebot import types
from database import db
from config import states
import data
#from handlers import start_handler
import category_handler

bot_token = ''

bot = telebot.TeleBot(token=bot_token)
con = db.connect()

@bot.message_handler(commands=['user'])
def user(message):
  db.add_user(con, message.chat.id, message.from_user.first_name, message.from_user.last_name)
  bot.send_message(message.chat.id, text=f'Привет {message.from_user.first_name}')

# /start Вывод всех категорий
@bot.message_handler(commands=['start'])
def start(message):
  categories = db.select_categories(con)
  inline_keyboard=types.InlineKeyboardMarkup()
  for category in categories:
    inline_keyboard.add(types.InlineKeyboardButton(text=category.name, callback_data=category.id))

  bot.send_message(message.chat.id, text=f'Привет {message.from_user.first_name}', reply_markup=inline_keyboard)

# /admin Вывод доступных команд для админов
@bot.message_handler(commands=['admin'])
def admin(message):
  db.set_state(con, states.STATE_ADMIN, message.chat.id)
  inline_keyboard=types.InlineKeyboardMarkup()
  inline_keyboard.add(types.InlineKeyboardButton(text='Добавить категорию', callback_data='addCategory'))
  inline_keyboard.add(types.InlineKeyboardButton(text='Удалить категорию', callback_data='deleteCategory'))

  bot.send_message(message.chat.id, text='Администрирование', reply_markup=inline_keyboard)

# обработчик
@bot.callback_query_handler(func=lambda call: db.get_current_state(con, call.message.chat.id) == states.STATE_ADMIN)
def handler(call):
  if call.data == 'addCategory':
    add_category(call)
  elif call.data == 'deleteCategory':
    category_handler.delete_category(bot, con, call)
  # else:
  #   start_handler.startHandler(bot, call)

# @bot.callback_query_handler(func=lambda call: True)
# def start_h(call):
#   startHandler(bot, call)

# Добавить категорию
def add_category(call):
  db.set_state(con, states.STATE_ENTER_CATEGORY_NAME, call.message.chat.id)
  bot.send_message(call.message.chat.id, text='Введи название категории')
  #db.addCategory(con, "Общая информация о компании, сотрудниках", None, None)

@bot.message_handler(func=lambda message: db.get_current_state(con, message.chat.id) == states.STATE_ENTER_CATEGORY_NAME)
def user_entering_name(message):
  bot.send_message(message.chat.id, "Введи описание категории")
  db.set_state(con, states.STATE_ENTER_CATEGORY_INFO, message.chat.id)

@bot.message_handler(func=lambda message: db.get_current_state(con, message.chat.id) == states.STATE_ENTER_CATEGORY_INFO)
def user_entering_info(message):
  db.set_state(con, states.STATE_ENTER_PARENT_CATEGORY, message.chat.id)
  categories = db.select_all_categories(con)
  inline_keyboard=types.InlineKeyboardMarkup()
  inline_keyboard.add(types.InlineKeyboardButton(text="Нет родительской категории", callback_data="no_category"))
  for category in categories:
    inline_keyboard.add(types.InlineKeyboardButton(text=category.name, callback_data=category.id))

  bot.send_message(message.chat.id, "Выбери родительскую категорию", reply_markup=inline_keyboard)

@bot.callback_query_handler(func=lambda call: db.get_current_state(con, call.message.chat.id) == states.STATE_ENTER_PARENT_CATEGORY)
def user_entering_parent_category(call):
  bot.send_message(call.message.chat.id, f"Готово!, {call.data}")
  db.set_state(con, states.DEFAULT, call.message.chat.id)

def startHandler(bot, call):
  category = next(c for c in data.categories if c.id == int(call.data))
  subCategories = list(filter(lambda c: c.parentId == int(call.data), data.categories))

  if len(subCategories) > 0:
    inline_keyboard=types.InlineKeyboardMarkup()

    for subCategory in subCategories:
      inline_keyboard.add(types.InlineKeyboardButton(text=subCategory.name, callback_data=subCategory.id))
    bot.send_message(call.message.chat.id, text=category.name, reply_markup=inline_keyboard)
  else:
    if not category.info == '':
      bot.send_message(call.message.chat.id, text=category.info)
    else:
      bot.send_message(call.message.chat.id, text=category.name)

bot.polling()
# while True:
#   try:
#     bot.polling()
#   except Exception:
#     time.sleep(15)