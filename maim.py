import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


TOKEN = "??????"

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_keyboard():
    kb = [
        [KeyboardButton(text="Привет")],
        [KeyboardButton(text="Пока")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    return keyboard

def get_InlineKeyboard():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
   [InlineKeyboardButton(text="Видео", url='https://vk.com/vkvideo')],
   [InlineKeyboardButton(text="Музыка", url='https://music.vk.com/')],
   [InlineKeyboardButton(text="Новости", url='https://dzen.ru/')]
])
    return ikb



@dp.message(CommandStart())
async def start(message: Message):
    await message.reply("Выберите действие:", reply_markup=get_keyboard())


@dp.message(F.text.in_(["Привет", "Пока"])) 
async def handle_text(message: types.Message):
    user_name = message.from_user.first_name
    
    if message.text == "Привет":
        await message.reply(f"Привет, {user_name}!")
    elif message.text == "Пока":
        await message.reply(f"До свидания, {user_name}!")

@dp.message(Command('links'))
async def links(message: Message):
    await message.answer('Вот ссылки, выбирай что больше нравится', reply_markup=get_InlineKeyboard())


def get_initial_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Показать больше", callback_data="show_options")]
    ])


def get_options_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Опция 1", callback_data="option_1")],
        [InlineKeyboardButton(text="Опция 2", callback_data="option_2")]
    ])


@dp.message(Command("dynamic"))
async def cmd_dynamic(message: types.Message):
    await message.answer("Нажмите на кнопку ниже:", reply_markup=get_initial_keyboard())


@dp.callback_query()
async def callback_handler(callback: CallbackQuery):
    if callback.data == "show_options":
       
        await callback.message.edit_reply_markup(reply_markup=get_options_keyboard())
    elif callback.data == "option_1":
        await callback.message.answer("Вы выбрали опцию 1")
        await callback.answer()
    elif callback.data == "option_2":
        await callback.message.answer("Вы выбрали опцию 2")
        await callback.answer()



async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())