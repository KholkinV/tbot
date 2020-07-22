from telebot import types

# /start обработка
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
