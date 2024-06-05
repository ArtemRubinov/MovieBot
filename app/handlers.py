from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram import F, Router

import config
from config import admin
import sqlite3
import app.keyboards as kb
import asyncio
from config import TOKEN
from aiogram import Bot
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import app.db as db

bot = Bot(token=TOKEN)

router = Router()


class Sender(StatesGroup):
    textmsg = State()

class Movie (StatesGroup):
    deletemovieid = State()
    addmoviename = State()
    addmoviedescription = State()

class Channel (StatesGroup):
    addchannelid = State()
    addchannelname = State()
    addchannellink = State()
    deletechannelid = State()

async def check_sub_channels(channels, user_id):
    for channel in channels:
        chat_member = await  bot.get_chat_member(chat_id=channel[0], user_id=user_id)
        if chat_member.status == 'left':
            return False
    return True


@router.message(CommandStart())
async def cmd_start(message: Message):
    if message.from_user.id == admin:
        await  message.answer(text=f'Вот твоя админ панелька', reply_markup=kb.admin)

    if await check_sub_channels(await db.get_channels(), message.from_user.id) or message.from_user.id == admin:
        await  message.answer(text=f'Приветствую, <b>{message.from_user.first_name}</b>, ты находишься в боте для '
                               f'поиска фильмов по коду, для поиска воспользуйся /search код_фильма',parse_mode='HTML')
    else:
        await bot.send_message(message.from_user.id, "Для доступа к боту необходимо подписаться на партнеров!",
                                   reply_markup=await kb.showChannels())
    await db.create_db()
    await db.add_user(message.from_user.id)



@router.message(Command("search"))
async def search(message:Message, command: CommandObject):
    if await check_sub_channels(await db.get_channels(), message.from_user.id) or message.from_user.id == admin:
        await message.answer(f"{await db.get_movie_data_as_string(command.args)}", parse_mode='HTML')
    else:
        await bot.send_message(message.from_user.id, "Для доступа к боту необходимо подписаться на партнеров!",
                               reply_markup=await kb.showChannels())

@router.message(Command('send'))
async def settext(message: Message, state: FSMContext):
    if await check_sub_channels(await db.get_channels(), message.from_user.id):
        await state.set_state(Sender.textmsg)
        await message.answer('Введите текст рассылки')
    else:
        await bot.send_message(message.from_user.id, "Для доступа к боту необходимо подписаться на партнеров!", reply_markup=await kb.showChannels())

@router.callback_query(F.data == "subchanneldone")
async def subchanneldone(callback: CallbackQuery):
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    if await check_sub_channels(await db.get_channels(), callback.from_user.id):
        await bot.send_message(callback.from_user.id, "Успех! Для поиска воспользуйся /search код_фильма")
    else:
        await bot.send_message(callback.from_user.id, "Для доступа к боту необходимо подписаться на партнеров!", reply_markup=await kb.showChannels())

@router.callback_query(F.data == "stats")
async def stats(callback: CallbackQuery):
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    totaluser = await db.get_total_user_count()
    todayuser = await db.get_users_joined_today_count()
    await bot.send_message(callback.from_user.id, f"📊 Статистика\n Пользователей за сегодня: {todayuser} \n "
                                                  f"Пользователей за все время: {totaluser}", reply_markup=kb.admin)

@router.callback_query(F.data == "channel_panel")
async def channel_panel(callback: CallbackQuery):
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, f"{await db.get_channels_data_as_string()} ",
                           reply_markup=kb.channels, parse_mode='HTML')

@router.callback_query(F.data == "movies")
async def movies(callback: CallbackQuery):
    await bot.delete_message(callback.from_user.id, callback.message.message_id)
    await bot.send_message(callback.from_user.id, f"Меню фильмов 🎬", reply_markup=kb.movies)

@router.callback_query(F.data == "movies_list")
async def movies_list(message: Message):
    await bot.send_message(message.from_user.id, f"{await db.get_movies_data_as_string()} ",
                           reply_markup=kb.movies, parse_mode='HTML')

@router.callback_query(F.data == "delete_movie")
async def delete_movie(message: Message, state: FSMContext):
    await state.set_state(Movie.deletemovieid)
    await message.message.answer('Введите id фильма, который необходимо удалить')

@router.message(Movie.deletemovieid)
async def del_movie(message: Message, state: FSMContext):
    await state.update_data(deletemovieid=message.text)
    data = await state.get_data()
    try:
        await db.delete_movie(data)
        await message.answer('Канал успешно удален')
    except Exception as e:
        await message.answer('Возникла ошибка при удалении канала')


@router.callback_query(F.data == "delete_channel")
async def delete_channel(message: Message, state: FSMContext):
    await state.set_state(Channel.deletechannelid)
    await message.message.answer('Введите id канала, который необходимо удалить')

@router.message(Channel.deletechannelid)
async def del_channel(message: Message, state: FSMContext):
    await state.update_data(deletechannelid=message.text)
    data = await state.get_data()
    try:
        await db.delete_channel(data)
        await message.answer('Канал успешно удален')
    except Exception as e:
        await message.answer('Возникла ошибка при удалении канала')

@router.callback_query(F.data == "add_channel")
async def add_channel(message: Message, state: FSMContext):
    await state.set_state(Channel.addchannelid)
    await message.message.answer('Введите id канала, который необходимо удалить, убедитесь, '
                                 'что бот является администратором в канале!')

@router.message(Channel.addchannelid)
async def add_channel_id(message: Message, state: FSMContext):
    await state.update_data(addchannelid=message.text)
    await state.set_state(Channel.addchannelname)
    await message.answer('Введите название канала, которое будет отображаться у пользователей')

@router.message(Channel.addchannelname)
async def add_channel_name(message: Message, state: FSMContext):
    await state.update_data(addchannelname=message.text)
    await state.set_state(Channel.addchannellink)
    await message.answer('Введите ссылку на канал в формате https://t.me/example')

@router.message(Channel.addchannellink)
async def add_channel_link(message: Message, state: FSMContext):
    await state.update_data(addchannellink=message.text)
    data = await state.get_data()
    await state.clear()
    try:
        await db.add_channel(data)
        await message.answer('Канал успешно добавлен')
    except Exception as e:
        await message.answer('Возникла ошибка при добавлении канала')

@router.callback_query(F.data == "add_movie")
async def add_movie(message: Message, state: FSMContext):
    await state.set_state(Movie.addmoviename)
    await message.message.answer('Введите название фильма')

@router.message(Movie.addmoviename)
async def add_movie_name(message: Message, state: FSMContext):
    await state.update_data(addmoviename=message.text)
    await state.set_state(Movie.addmoviedescription)
    await message.answer('Введите описание к фильму')

@router.message(Movie.addmoviedescription)
async def add_movie_description(message: Message, state: FSMContext):
    await state.update_data(addmoviedescription=message.text)
    data = await state.get_data()
    await state.clear()
    try:
        await db.add_movie(data)
        await message.answer('Фильм успешно добавлен')
    except Exception as e:
        await message.answer(f'Возникла ошибка при добавлении фильма {e}')








