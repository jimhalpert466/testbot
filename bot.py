import aiogram.utils.markdown as md
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types, executor
import settings
from db import User, db
import time
import random

# bot init
bot = Bot(token=settings.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


class Goods(StatesGroup):
    code = State()
    data = State()


class Review(StatesGroup):
    data = State()
    good_id = State()
    review_text = State()
    rating = State()


# KEYBOARD
get_key = types.KeyboardButton('🎁 Get link to key (232/300)')
history = types.KeyboardButton('📋 Issue history (last 5)')
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(get_key)
keyboard.add(history)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    """START HANDLING"""
    await bot.send_message(message.chat.id, 'Hello! 👋\nNow there is a month of free distribution of STEAM keys!\nRather take your! 🔑', reply_markup=keyboard)
    # save user data to base
    try:
        db.session.add(User(id=message.chat.id, login=message.chat.username,
                       fname=message.chat.first_name, lname=message.chat.last_name, status=0))
        db.session.commit()
    except Exception as e:
        print(e)


@dp.message_handler()
async def message_text_controller(message: types.Message):
    """TEXT Controller"""

    link = 'http://usheethe.com/fS38'

    user = User.query.filter_by(id=str(message.chat.id)).first()

    # key btn
    if message.text == '🎁 Get link to key (232/300)':
        

        if user.status == 0:
            await bot.send_message(message.chat.id, 'Randomization process... Please wait 🐱', reply_markup=keyboard)
            time.sleep(random.randint(3, 6))
            await bot.send_message(message.chat.id, f"Your link to the key🔑\nLink: {link}\nYour key is inside the txt file 📄 \n\nPlease don`t hate ads\nThis helps us provide you with our product for FREE.\nThank you for being with us 😊", reply_markup=keyboard)
            
            await bot.send_message(message.chat.id, 'You can ask for a new key after 24 hours ⏳', reply_markup=keyboard)

        
            user.status = 1
            db.session.commit()
        else:
            await bot.send_message(message.chat.id, 'Wait 24 hours ⏳', reply_markup=keyboard)

    # history btn
    if message.text == '📋 Issue history (last 5)':
        await bot.send_message(message.chat.id, 'Last 5 distributions', reply_markup=keyboard)

        games = [{'id': '541*******', 'game': 'Risk of Rain 2 Steam Key EUROPE'},
                 {'id': '133******', 'game': 'Viking Brothers 3 Steam Key GLOBAL'},
                 {'id': '165*****', 'game': 'Calico (PC) Steam Key EUROPE'},
                 {'id': '224******', 'game': 'Hotline Miami 2: Wrong Number Steam Key EUROPE'},
                 {'id': '559*******', 'game': 'Muddledash Steam Key GLOBAL'}]
        
        if user.status == 0:
            for i in games:
                await bot.send_message(message.chat.id, i['id'] + ': ' + i['game'], reply_markup=keyboard)
        else:
            await bot.send_message(message.chat.id, f"{str(message.chat.id)[0:3]}********: Alien: Isolation (Nostromo Edition) Steam Key EUROPE", reply_markup=keyboard)
            for i in games[1:5]:
                await bot.send_message(message.chat.id, i['id'] + ': ' + i['game'], reply_markup=keyboard)



def start():
    executor.start_polling(dp, skip_updates=True)


start()
