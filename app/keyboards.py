from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import  InlineKeyboardBuilder


from config import TOKEN
from aiogram import Bot
import app.db as db
bot = Bot(token=TOKEN)

admin = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📈 Статистика' , callback_data='stats'),
     InlineKeyboardButton(text='🎬 Фильмы' , callback_data='movies')],
    [InlineKeyboardButton(text='📺 Панель каналов', callback_data='channel_panel')]
])

channels = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Добавить канал' , callback_data='add_channel'),
     InlineKeyboardButton(text='❌ Удалить канал' , callback_data='delete_channel')]
])

movies = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🎬 Список фильмов', callback_data='movies_list')],
    [InlineKeyboardButton(text='✅ Добавить фильм' , callback_data='add_movie'),
     InlineKeyboardButton(text='❌ Удалить фильм' , callback_data='delete_movie')]


])

async def showChannels():
    keyboard = InlineKeyboardBuilder()
    channelss = await db.get_channels()
    for channel in channelss:

        keyboard.add(InlineKeyboardButton(text=channel[1], url=channel[2]))
    keyboard.add(InlineKeyboardButton(text='Я подписался', callback_data="subchanneldone"))
    return keyboard.adjust(1).as_markup()



