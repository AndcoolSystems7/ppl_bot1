"""
Pepeland bandage bot
Проект защищён авторским правом
created by AndcoolSystems, 2023©
"""
tech_raboty = False
import logging
logging.basicConfig(level=logging.INFO)
try: 
	import replit
	on_server = True
except: on_server = False

server_text = "replit" if on_server else "local"
logging.info(f"Running on {server_text} server")
#print(f"INFO:Running on {server_text} server")

if on_server: from scripts.background import keep_alive
import aiogram
import scripts.client as client
import os
from PIL import Image
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime  #Модуль времени
import pytz
import time as time1
from aiogram.utils.markdown import link
from io import BytesIO
import numpy as np
import random
import scripts.da as da
import aioschedule as schedule
import asyncio
from aiogram.utils.exceptions import (MessageCantBeDeleted,
                                      MessageToDeleteNotFound)
from contextlib import suppress
import scripts.clientCommands as clientCommands
import math
import scripts.emoji as emoji
import importlib

if on_server: API_TOKEN = '6121533259:AAHe4O1XP63PtF6RfYf_hJ5QFyMp6J387SU'
else: API_TOKEN = '5850445478:AAFx4SZdD1IkSWc4h_0qU9IoXyT8VAElbTE'

logger = logging.getLogger('schedule')
logger.setLevel(logging.WARNING)


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
da.init(bot, dp)
async def sessionPizda(msg): await msg.answer("Упс. Ваша сессия была завершена\nПожалуйста, отправьте /start для начала работы")
async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()
def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))

if not tech_raboty:
	listOfClients = []
	welcome_msg = Image.open(f"res/presets/start.png")

	clientCommands.init(bot, dp, on_server)
	andcool_id = -1001980044675


	#---------------------------------------------------------------------------------------------------

	@dp.message_handler(commands=['badgesReload'])
	async def send_welcome(message: types.Message):
		andcool_id = -1001980044675
		if andcool_id == message.chat.id:
			try:
				importlib.reload(emoji)
				await message.reply(text="Badges reloaded")
			except Exception as e: await message.reply(text=f"Badges reloader:{e}")
	#---------------------------------------------------------------------------------------------------


	@dp.message_handler(commands=['reviews'])
	async def send_welcome(message: types.Message):
		global andcool_id
		if os.path.isfile("data/reviews.npy"):
			reviewsListNp = np.load("data/reviews.npy")
			reviewsList = reviewsListNp.tolist()
			if reviewsList == []: 
				await message.answer(text="Отзывов пока не было(")
				return
			global listOfClients
			if listOfClients == []: listOfClients.append(client.Client(message.chat.id))
			else:
				finded = False
				for add in range(len(listOfClients)):
					if listOfClients[add].chat_id == message.chat.id:
						finded == True
						listOfClients[add] = client.Client(message.chat.id)
						break
				if not finded: listOfClients.append(client.Client(message.chat.id))

			id1 = message.chat.id
			id = client.find_client(listOfClients, message.chat.id)
			messages_on_page = 4
			
			if len(reviewsList) <= messages_on_page:
				reviewTxt = []

				for x in range(len(reviewsList)):
					member = await bot.get_chat_member(int(reviewsList[x][1]), int(reviewsList[x][1]))
					
					first = str(member.user.first_name) if member.user.first_name != None else ""
					kast_a = " " if first != "" else ""
					last = (kast_a + str(member.user.last_name)) if member.user.last_name != None else ""
					msg_id = f"({len(reviewsList) - x}) ({reviewsList[x][1]})" if andcool_id == message.chat.id else ""
					emoji1 = emoji.badges.get(int(reviewsList[x][1]), "")
					reviewTxt.append(f"*{first}{last}{emoji1} {reviewsList[x][0]} {msg_id}\n\n")

				rew = "".join(reviewTxt)
				await message.answer(text=f"Отзывы:\n{rew}*Страница 1-1*\nОставить отзыв можно отправив команду /review", parse_mode="Markdown")
			else:
				keyboard1: InlineKeyboardMarkup = InlineKeyboardMarkup()
				big_button_4: InlineKeyboardButton = InlineKeyboardButton(
					text='←', callback_data='leftRev')
				big_button_5: InlineKeyboardButton = InlineKeyboardButton(
					text='→', callback_data='rightRev')
				
				pages_count = math.ceil(len(reviewsList) / messages_on_page) - 1
				listOfClients[id].ReviewsPage = constrain(listOfClients[id].ReviewsPage, 0, pages_count)
				if listOfClients[id].ReviewsPage > 0: 
					if listOfClients[id].ReviewsPage < pages_count:
						keyboard1.row(big_button_4, big_button_5)
					elif listOfClients[id].ReviewsPage == pages_count: 
						keyboard1.row(big_button_4)
				elif listOfClients[id].ReviewsPage == 0: 
					keyboard1.row(big_button_5)
				
				reviewTxt = []
				for x in range(messages_on_page):
					try:
						member = await bot.get_chat_member(int(reviewsList[x + (messages_on_page * listOfClients[id].ReviewsPage)][1]), int(reviewsList[x + (messages_on_page * listOfClients[id].ReviewsPage)][1]))
						msg_id = f"({len(reviewsList) - (x + (messages_on_page * listOfClients[id].ReviewsPage))}) ({reviewsList[x + (messages_on_page * listOfClients[id].ReviewsPage)][1]})" if andcool_id == message.chat.id else ""
						first = str(member.user.first_name) if member.user.first_name != None else ""
						kast_a = " " if first != "" else ""
						last = (kast_a + str(member.user.last_name)) if member.user.last_name != None else ""
						emoji1 = emoji.badges.get(int(reviewsList[x + (messages_on_page * listOfClients[id].ReviewsPage)][1]), "")
						reviewTxt.append(f"*{first}{last}{emoji1} {reviewsList[x + (messages_on_page * listOfClients[id].ReviewsPage)][0]} {msg_id}\n\n")
					except: pass
				rew = "".join(reviewTxt)
				try:
					listOfClients[id].ReviewsMsg = await message.answer(text=f"Отзывы:\n{rew}*Страница {listOfClients[id].ReviewsPage + 1}-{pages_count + 1}*\nОставить отзыв можно отправив команду /review", parse_mode="Markdown", reply_markup=keyboard1)
				except: pass
				

		else: await message.answer(text="Отзывов пока не было(")


	#---------------------------------------------------------------------------------------------------
	@dp.callback_query_handler(text=["rightRev", "leftRev"])
	async def from_f(message: CallbackQuery):
		global listOfClients
		reviewsListNp = np.load("data/reviews.npy")
		reviewsList = reviewsListNp.tolist()
		id = client.find_client(listOfClients, message.message.chat.id)
		if id == -1: 
			await sessionPizda(message.message)
			return
		messages_on_page = 4
		pages_count = math.ceil(len(reviewsList) / messages_on_page) - 1
		if message.data == "rightRev":
			if listOfClients[id].ReviewsPage < pages_count: listOfClients[id].ReviewsPage += 1
		else:
			if listOfClients[id].ReviewsPage > 0: listOfClients[id].ReviewsPage -= 1
		keyboard1: InlineKeyboardMarkup = InlineKeyboardMarkup()
		big_button_4: InlineKeyboardButton = InlineKeyboardButton(
			text='←', callback_data='leftRev')
		big_button_5: InlineKeyboardButton = InlineKeyboardButton(
			text='→', callback_data='rightRev')
		

		listOfClients[id].ReviewsPage = constrain(listOfClients[id].ReviewsPage, 0, pages_count)
		if listOfClients[id].ReviewsPage > 0: 
			if listOfClients[id].ReviewsPage < pages_count:
				keyboard1.row(big_button_4, big_button_5)
			elif listOfClients[id].ReviewsPage == pages_count: 
				keyboard1.row(big_button_4)
		elif listOfClients[id].ReviewsPage == 0: 
			keyboard1.row(big_button_5)
		reviewTxt = []
		for x in range(messages_on_page):
			try:
				member = await bot.get_chat_member(int(reviewsList[x + (messages_on_page * listOfClients[id].ReviewsPage)][1]), int(reviewsList[x + (messages_on_page * listOfClients[id].ReviewsPage)][1]))
						
				first = str(member.user.first_name) if member.user.first_name != None else ""
				kast_a = " " if first != "" else ""
				last = (kast_a + str(member.user.last_name)) if member.user.last_name != None else ""
				msg_id = f"({len(reviewsList) - (x + (messages_on_page * listOfClients[id].ReviewsPage))}) ({reviewsList[x + (messages_on_page * listOfClients[id].ReviewsPage)][1]})" if andcool_id == message.message.chat.id else ""
				emoji1 = emoji.badges.get(int(reviewsList[x + (messages_on_page * listOfClients[id].ReviewsPage)][1]), "")
				reviewTxt.append(f"*{first}{last}{emoji1} {reviewsList[x + (messages_on_page * listOfClients[id].ReviewsPage)][0]} {msg_id}\n\n")
			except: pass
		rew = "".join(reviewTxt)
		try:
			await listOfClients[id].ReviewsMsg.edit_text(text=f"Отзывы:\n{rew}*Страница {listOfClients[id].ReviewsPage + 1}-{pages_count + 1}*\nОставить отзыв можно отправив команду /review", reply_markup=keyboard1, parse_mode="Markdown")
		except: pass
	#---------------------------------------------------------------------------------------------------
	
	@dp.message_handler(commands=['review'])
	async def send_welcome(message: types.Message):
		global listOfClients
		if listOfClients == []: listOfClients.append(client.Client(message.chat.id))
		else:
			finded = False
			for add in range(len(listOfClients)):
				if listOfClients[add].chat_id == message.chat.id:
					finded == True
					listOfClients[add] = client.Client(message.chat.id)
					break
			if not finded: listOfClients.append(client.Client(message.chat.id))

		id1 = message.chat.id
		banned = False
		if os.path.isfile("data/banned.npy"):
			reviewsListNp = np.load("data/banned.npy")
			reviewsList = reviewsListNp.tolist()
			if reviewsList == []: pass
			else: 
				if message.from_user.id in reviewsList: banned = True
		if not banned:
			id = client.find_client(listOfClients, message.chat.id)
			keyboard1: InlineKeyboardMarkup = InlineKeyboardMarkup()
			big_button_4: InlineKeyboardButton = InlineKeyboardButton(
				text='Отмена', callback_data='reviewDeny')


			keyboard1.row(big_button_4)
			listOfClients[id].waitToReview = True
			await message.answer(text="Окей, теперь отправьте *одно* сообщение - ваш отзыв.\n*Пожалуйста*, будьте вежливыми и не употребляйте грубые слова и выражения!", parse_mode="Markdown", reply_markup=keyboard1)
		else: await message.answer(text="Вы забанены в отзывах, напишите в /support и модераторы рассмотрят ваш запрос")

	#---------------------------------------------------------------------------------------------------
	@dp.callback_query_handler(text="reviewDeny")
	async def from_f(message: CallbackQuery):
		id1 = message.message.chat.id
		global listOfClients
		id = client.find_client(listOfClients, message.message.chat.id)
		if id == -1: 
			await sessionPizda(message.message)
			return
		listOfClients[id].waitToReview = False
		await message.message.delete()
	#---------------------------------------------------------------------------------------------------

	@dp.message_handler(commands=['support'])
	async def send_welcome(message: types.Message):
		global listOfClients
		if listOfClients == []: listOfClients.append(client.Client(message.chat.id))
		else:
			finded = False
			for add in range(len(listOfClients)):
				if listOfClients[add].chat_id == message.chat.id:
					finded == True
					listOfClients[add] = client.Client(message.chat.id)
					break
			if not finded: listOfClients.append(client.Client(message.chat.id))

		id1 = message.chat.id

		id = client.find_client(listOfClients, message.chat.id)

		listOfClients[id].wait_to_support = True
		await message.answer(text="Окей, теперь отправь *одно* сообщение (можно фото с подписью), где описываете вашу проблему или вопрос.", parse_mode="Markdown")

	

	#---------------------------------------------------------------------------------------------------
	async def render_and_edit(message, id, id1):
		global listOfClients
		bio = BytesIO()
		skin_rer = await listOfClients[id].rerender()

		bio.name = f'{id1}.png'
		skin_rer.save(bio, 'PNG')
		bio.seek(0)
		photo1 = types.input_media.InputMediaPhoto(media=bio, caption="Вот предварительный просмотр")

		try: listOfClients[id].prewiew_id = await bot.edit_message_media(photo1,
									chat_id=listOfClients[id].prewiew_id.chat.id,
									message_id=listOfClients[id].prewiew_id.message_id)
		except:pass
	#---------------------------------------------------------------------------------------------------
	@dp.message_handler(commands=['start'])
	async def send_welcome(message: types.Message):

		now_time_log = datetime.now(pytz.timezone('Etc/GMT-3'))

		now_time_format = "{}.{}.{}-{}:{}".format(now_time_log.day,
												now_time_log.month,
												now_time_log.year,
												now_time_log.hour,
												now_time_log.minute)

		big_button_1: InlineKeyboardButton = InlineKeyboardButton(
			text='Из файла', callback_data='file')

		big_button_2: InlineKeyboardButton = InlineKeyboardButton(
			text='По нику', callback_data='nick')

		# Создаем объект инлайн-клавиатуры
		keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup()
		keyboard.row(big_button_2, big_button_1)
		global welcome_msg
		bio = BytesIO()
		bio.name = f'{message.from_user.id}.png'
		welcome_msg.save(bio, 'PNG')
		bio.seek(0)
		await message.answer_photo(photo=bio, caption="Привет👋! Давай начнём.\nОткуда брать скин?",
												reply_markup=keyboard)
		global listOfClients
		if listOfClients == []: listOfClients.append(client.Client(message.chat.id))
		else:
			finded = False
			for add in range(len(listOfClients)):
				if listOfClients[add].chat_id == message.chat.id:
					finded == True
					listOfClients[add] = client.Client(message.chat.id)
					break
			if not finded: listOfClients.append(client.Client(message.chat.id))
		f_usr_list = []

		if os.path.isfile("data/usr.txt"):
			userListFile = open("data/usr.txt", 'r', encoding='utf-8')
			f_usr_list = userListFile.read().split("\n")
			userListFile.close()
			userListFile = open("data/usr.txt", 'a', encoding='utf-8')

		else:
			userListFile = open("data/usr.txt", 'w', encoding='utf-8')
			userListFile.close()
			userListFile = open("data/usr.txt", 'a', encoding='utf-8')

		if os.path.isfile("data/usr_use.txt"):
			userListFile1 = open("data/usr_use.txt", 'a', encoding='utf-8')

		else:
			userListFile1 = open("data/usr_use.txt", 'w', encoding='utf-8')
			userListFile1.close()
			userListFile1 = open("data/usr_use.txt", 'a', encoding='utf-8')
		if f_usr_list != []:
			if not str(f"{message.from_user.username} - {message.from_user.id}") in f_usr_list:
				userListFile.write(f"{message.from_user.username} - {message.from_user.id}\n")

		userListFile1.write(f"{message.from_user.username} - {now_time_format} - {message.from_user.id}\n")
		userListFile.close()
		userListFile1.close()

		
		
	#---------------------------------------------------------------------------------------------------
	@dp.callback_query_handler(text="file")
	async def from_f(message: CallbackQuery):
		global listOfClients
		id = client.find_client(listOfClients, message.message.chat.id)
		if id == -1: 
			await sessionPizda(message.message)
			return
		msg = await message.message.answer(
			'Хорошо, теперь отправь мне свой скин.\nОбязательно при отправке убери галочку "Сжать изображение"'
		)
		await message.message.delete()
		listOfClients[id].wait_to_file = 1
		listOfClients[id].import_msg = msg

	#---------------------------------------------------------------------------------------------------
	@dp.callback_query_handler(text="nick")
	async def from_f(message: CallbackQuery):
		global listOfClients
		id = client.find_client(listOfClients, message.message.chat.id)
		if id == -1: 
			await sessionPizda(message.message)
			return
		msg = await message.message.answer("Хорошо, теперь отправь мне свой никнейм.")
		await message.message.delete()
		
		listOfClients[id].wait_to_file = 2
		listOfClients[id].import_msg = msg

	#---------------------------------------------------------------------------------------------------
	@dp.message_handler(content_types=['photo'])
	async def handle_docs_photo(message: types.Message):
		global listOfClients
		
		if message.from_user.id == 1197005557:
			if message.caption != None:
				mess = message.caption.split(" ")
				if mess[0] == "/sendToId":
					await message.photo[-1].download(destination_file=f'file.png')
					photo = open(f'file.png', 'rb')
					await bot.send_photo(chat_id=int(mess[1]), caption=f"Ответ администратора:\n{mess[2]}", photo=photo)
		
		id = client.find_client(listOfClients, message.chat.id)
		if id == -1: 
			await sessionPizda(message)
			return
			
		if listOfClients[id].wait_to_support:
			await message.photo[-1].download(destination_file=f'file.png')
			photo = open(f'file.png', 'rb')
			await bot.send_photo(chat_id=-1001980044675, caption=f"{message.caption}\n\nОтправил: {message.from_user.username}\nЕго id: {message.from_user.id}", photo=photo)
			photo.close()
			os.remove('file.png')
			listOfClients[id].wait_to_support = False

		elif listOfClients[id].wait_to_file == 1:
			await message.reply('Пожалуйста, отправьте мне развёртку скина как файл или при отпраке снимите галочку "Сжать изображение"')



	#---------------------------------------------------------------------------------------------------
	@dp.message_handler(content_types=['document'])
	async def handle_docs_photo(message: types.Message):
		global listOfClients
		id = client.find_client(listOfClients, message.chat.id)
		id1 = message.chat.id
		if id == -1: 
			await sessionPizda(message)
			return

		if listOfClients[id].wait_to_file == 1:
			if document := message.document:
				try:
					await document.download(destination_file=f'{id1}.png')
				except aiogram.utils.exceptions.FileIsTooBig:
					text1 = 'Ты серёзно пытался загрузить файл объёмом более *20 Мегабайт*?🤨\nЗачем? Обычный скин имеет объём примерно *4 Килобайт*.\nЧто ты хотел этим доказать?\n'
					text2 = "Ты ждал много времени, пока загрузиться файл, ради чего? Ради минутной забавы?\nТы пытался показать боту, кто тут главный, но сам проиграл.\n"
					await message.reply(text1 + text2, parse_mode="Markdown")
					return

			usr_img = Image.open(f'{id1}.png').convert("RGBA")
			os.remove(f'{id1}.png')
			w, h = usr_img.size
			done = True
			for y_ch in range(3):
				for x_ch in range(3):
					r, g, b, t = usr_img.getpixel((x_ch, y_ch))
					if t != 0:
						done = False
						break

			if not done:
				msg_del = await message.answer("У вашего скина непрозрачный фон!\nПредпросмотр будет некорректным!")
				asyncio.create_task(delete_message(msg_del, 10))
		
			if w == 64 and h == 64:
				await listOfClients[id].init_mc_f(usr_img)
				listOfClients[id].wait_to_file = 0
				await listOfClients[id].prerender()
				await listOfClients[id].import_msg.delete()
				await message.delete()

				if not bool(usr_img.getpixel((46, 52))[3]) and not bool(usr_img.getpixel((45, 52))[3]): 
					keyboard1: InlineKeyboardMarkup = InlineKeyboardMarkup()
					big_button_4: InlineKeyboardButton = InlineKeyboardButton(
						text='Стив', callback_data='man_steve')

					big_button_5: InlineKeyboardButton = InlineKeyboardButton(
						text='Алекс', callback_data='man_alex')

					keyboard1.row(big_button_4, big_button_5)

					msg = await message.answer("Извините, боту не удалось корректно определить тип вашего скина.\nПожалуйста, выберете правильный:", reply_markup=keyboard1)
					listOfClients[id].info_id = msg
					return
				skin_rer = await listOfClients[id].rerender()
				bio = BytesIO()
				bio.name = f'{id1}.png'
				skin_rer.save(bio, 'PNG')
				bio.seek(0)

				msg = await message.answer_photo(bio, "Вот предварительный просмотр")
				listOfClients[id].prewiew_id = msg
				

				msg = await colorDialog(message, id)
				listOfClients[id].info_id = msg
			else:
				await message.reply("Пожалуйста, отправьте развёртку скина в формате png с разрешением 64х64 пикселей")
				usr_img.close()
				os.remove(f'{id1}.png')

		if listOfClients[id].wait_to_file == 4:
			listOfClients[id].wait_to_file = 0
			if document := message.document:
				await document.download(destination_file=f'paramImported{id1}.json')
			await message.delete()
			try:
				listOfClients[id].importJSON(id1)
			except: 
				msg = await message.answer("Не удалось корректно прочитать файл настроек")
				asyncio.create_task(delete_message(msg, 5))
			await render_and_edit(message, id, id1)
			os.remove(f'paramImported{id1}.json')
			await start_set(message)

	#---------------------------------------------------------------------------------------------------
	colour_txt = ["blue", "yellow", "green", "red", "pink", "violet", "orange", "black", "white"]
	@dp.callback_query_handler(text=colour_txt)
	async def from_f(message: CallbackQuery):

		id1 = message.message.chat.id
		global listOfClients
		global colour_txt
		id = client.find_client(listOfClients, message.message.chat.id)
		if id == -1: 
			await sessionPizda(message.message)
			return

		colours = [(61, 58, 201), (250, 213, 30), (85, 163, 64), (176, 30, 30), (252, 15, 192), (105, 0, 198), (255, 102, 0), (0, 0, 0), (255, 255, 255)]
		listOfClients[id].colour = colours[colour_txt.index(message.data)]

		await render_and_edit(message.message, id, id1)
		await acceptChoose(message.message)


	colour_txt_cu = ["golden", "pwOld"]
	@dp.callback_query_handler(text=colour_txt_cu)
	async def from_f(message: CallbackQuery):

		id1 = message.message.chat.id
		global listOfClients
		global colour_txt
		id = client.find_client(listOfClients, message.message.chat.id)
		if id == -1: 
			await sessionPizda(message.message)
			return

		colours = [0, 1]
		listOfClients[id].pepeImage = colours[colour_txt_cu.index(message.data)]
		listOfClients[id].colour = (0, 0, 0)

		await render_and_edit(message.message, id, id1)
		await acceptChoose(message.message)


	#---------------------------------------------------------------------------------------------------
	@dp.callback_query_handler(text="done_c")
	async def from_f(message: CallbackQuery):
		id1 = message.message.chat.id
		global listOfClients
		id = client.find_client(listOfClients, id1)
		if id == -1: 
			await sessionPizda(message.message)
			return
		await start_set(message.message)

	#---------------------------------------------------------------------------------------------------
	@dp.callback_query_handler(text="custom")
	async def from_f(message: CallbackQuery):

		id1 = message.message.chat.id
		global listOfClients
		id = client.find_client(listOfClients, id1)
		if id == -1: 
			await sessionPizda(message.message)
			return
		await listOfClients[id].info_id.delete()
		listOfClients[id].colour = 5
		listOfClients[id].wait_to_file = 3

		big_button_5: InlineKeyboardButton = InlineKeyboardButton(
		text='Отмена', callback_data='customDeny')

					# Создаем объект инлайн-клавиатуры
		keyboard1: InlineKeyboardMarkup = InlineKeyboardMarkup(
				inline_keyboard=[[big_button_5]])
		link4 = link('этом сайте', 'https://colorscheme.ru/color-converter.html')
		msg = await message.message.answer(
			f"Теперь отправьте свой цвет в формате *HEX* или *RGB*\nЦвет можно получить на {link4}\nБот принимает цвета в форматах:\n#ffffff\nffffff\n255,255,255\n255, 255, 255 и т.п.", parse_mode= 'Markdown', reply_markup=keyboard1
		)
		listOfClients[id].info_id = msg
	#---------------------------------------------------------------------------------------------------
	@dp.callback_query_handler(text="customDeny")
	async def from_f(message: CallbackQuery):
		id1 = message.message.chat.id
		global listOfClients
		id = client.find_client(listOfClients, id1)
		if id == -1: 
			await sessionPizda(message.message)
			return
		await colorDialog(message.message, id)
	#---------------------------------------------------------------------------------------------------
	async def acceptChoose(message):
		global listOfClients
		id = client.find_client(listOfClients, message.chat.id)
		if id == -1: 
			await sessionPizda(message)
			return
		big_button_4: InlineKeyboardButton = InlineKeyboardButton(
				text='Подтвердить выбор цвета', callback_data='done_d')

		big_button_5: InlineKeyboardButton = InlineKeyboardButton(
			text='Изменить цвет', callback_data='colD')

		keyboard1: InlineKeyboardMarkup = InlineKeyboardMarkup(
			inline_keyboard=[[big_button_4], [big_button_5]])
		await listOfClients[id].info_id.edit_text("Готово?", reply_markup=keyboard1)


	#---------------------------------------------------------------------------------------------------
	async def reset_accept(message):
		global listOfClients
		id = client.find_client(listOfClients, message.chat.id)
		if id == -1: 
			await sessionPizda(message)
			return
		big_button_4: InlineKeyboardButton = InlineKeyboardButton(
				text='Да ✓', callback_data='resetAccept')

		big_button_5: InlineKeyboardButton = InlineKeyboardButton(
			text='Нет ✗', callback_data='resetDeny')

		keyboard1: InlineKeyboardMarkup = InlineKeyboardMarkup(
			inline_keyboard=[[big_button_4], [big_button_5]])
		await listOfClients[id].info_id.edit_text("Сбросить?\nТочно?", reply_markup=keyboard1)

	#---------------------------------------------------------------------------------------------------
	@dp.callback_query_handler(text="resetDeny")
	async def from_f(message: CallbackQuery):
		global listOfClients
		id = client.find_client(listOfClients, message.message.chat.id)
		if id == -1: 
			await sessionPizda(message.message)
			return
		await start_set(message.message)


	#---------------------------------------------------------------------------------------------------
	@dp.callback_query_handler(text="resetAccept")
	async def from_f(message: CallbackQuery):
		global listOfClients
		id = client.find_client(listOfClients, message.message.chat.id)
		id1 = message.message.chat.id
		if id == -1: 
			await sessionPizda(message.message)
			return

		listOfClients[id].pos = 4
		listOfClients[id].overlay = True
		listOfClients[id].bw = False
		listOfClients[id].negative = False
		listOfClients[id].pose = 0
		listOfClients[id].absolute_pos = 0
		listOfClients[id].pepe_type = 0
		listOfClients[id].first_layer = 1

		await render_and_edit(message.message, id, id1)
		await start_set(message.message)


	#---------------------------------------------------------------------------------------------------
	@dp.callback_query_handler(text="colD")
	async def from_f(message: CallbackQuery):
		global listOfClients
		id = client.find_client(listOfClients, message.message.chat.id)
		if id == -1: 
			await sessionPizda(message.message)
			return
		msg = await colorDialog(message.message, id)
		
		
	#---------------------------------------------------------------------------------------------------
	@dp.callback_query_handler(text="done_d")
	async def from_f(message: CallbackQuery):
		global listOfClients
		id = client.find_client(listOfClients, message.message.chat.id)
		if id == -1: 
			await sessionPizda(message.message)
			return
		await start_set(message.message)
	#---------------------------------------------------------------------------------------------------

	async def done_accept(message):
		global listOfClients
		id = client.find_client(listOfClients, message.chat.id)
		if id == -1: 
			await sessionPizda(message)
			return
		big_button_4: InlineKeyboardButton = InlineKeyboardButton(
				text='Да ✓', callback_data='donetAccept')

		big_button_5: InlineKeyboardButton = InlineKeyboardButton(
			text='Нет ✗', callback_data='doneDeny')

		big_button_6: InlineKeyboardButton = InlineKeyboardButton(
			text='Готово, добавить ещё повязку', callback_data='doneadd')

		keyboard1: InlineKeyboardMarkup = InlineKeyboardMarkup(
			inline_keyboard=[[big_button_4], [big_button_5], [big_button_6]])
		await listOfClients[id].info_id.edit_text("Готово? После завершения отредактировать скин будет невозможно!", reply_markup=keyboard1)


	#---------------------------------------------------------------------------------------------------
	@dp.callback_query_handler(text="donetAccept")
	async def from_f(message: CallbackQuery):
		global listOfClients
		id1 = message.message.chat.id
		id = client.find_client(listOfClients, message.message.chat.id)
		if id == -1: 
			await sessionPizda(message.message)
			return
		bio = BytesIO()
		bio.name = f'{hex(int(id1))[2:].upper()}.png'
		listOfClients[id].skin_raw.save(bio, 'PNG')
		bio.seek(0)
		await message.message.answer_document(bio)
		await listOfClients[id].info_id.delete()
		listOfClients.pop(id)
		await message.message.answer("Вы можете оставить отзыв, отправив команду /review\nВсе просто общаются в отзывах")

	@dp.callback_query_handler(text="doneDeny")
	async def from_f(message: CallbackQuery):
		global listOfClients
		id1 = message.message.chat.id
		id = client.find_client(listOfClients, message.message.chat.id)
		if id == -1: 
			await sessionPizda(message.message)
			return
		await start_set(message.message)


	@dp.callback_query_handler(text="doneadd")
	async def from_f(message: CallbackQuery):
		global listOfClients
		id1 = message.message.chat.id
		id = client.find_client(listOfClients, message.message.chat.id)
		if id == -1: 
			await sessionPizda(message.message)
			return

		listOfClients[id].first_skin1 = listOfClients[id].skin_raw
		listOfClients[id].reset()
		msg = await colorDialog(message, id)
		listOfClients[id].info_id = msg

	#---------------------------------------------------------------------------------------------------
	async def colorDialog(message, id):
		global listOfClients
		
		big_button_1: InlineKeyboardButton = InlineKeyboardButton(
			text='Синий', callback_data='blue')
		goldenBtn: InlineKeyboardButton = InlineKeyboardButton(
			text='Повязка Пугода', callback_data='golden')
		
		pwOld: InlineKeyboardButton = InlineKeyboardButton(
			text='Старая повязка Пугода', callback_data='pwOld')

		big_button_2: InlineKeyboardButton = InlineKeyboardButton(
			text='Красный', callback_data='red')
		big_button_3: InlineKeyboardButton = InlineKeyboardButton(
			text='Зелёный', callback_data='green')
		big_button_4: InlineKeyboardButton = InlineKeyboardButton(
			text='Жёлтый', callback_data='yellow')
		
		pink_btn: InlineKeyboardButton = InlineKeyboardButton(
			text='Розовый', callback_data='pink')
		
		violet_btn: InlineKeyboardButton = InlineKeyboardButton(
			text='Фиолетовый', callback_data='violet')
		
		orange_btn: InlineKeyboardButton = InlineKeyboardButton(
			text='Оранжевый', callback_data='orange')
		
		white_btn: InlineKeyboardButton = InlineKeyboardButton(
			text='Белый', callback_data='white')
		
		black_btn: InlineKeyboardButton = InlineKeyboardButton(
			text='Чёрный', callback_data='black')

		custom_btn: InlineKeyboardButton = InlineKeyboardButton(
			text='Кастомный', callback_data='custom')

				# Создаем объект инлайн-клавиатуры
		keyboard1: InlineKeyboardMarkup = InlineKeyboardMarkup()

		keyboard1.row(goldenBtn)
		keyboard1.row(pwOld)
		keyboard1.row(big_button_1, big_button_2, big_button_3)
		keyboard1.row(big_button_4, pink_btn, violet_btn)
		keyboard1.row(orange_btn, white_btn, black_btn)

		keyboard1.row(custom_btn)
		
		if listOfClients[id].info_id == 0:
			msg = await message.answer("Теперь выбери цвет повязки",
																reply_markup=keyboard1)
		else:
			msg = await listOfClients[id].info_id.edit_text("Теперь выбери цвет повязки",
																reply_markup=keyboard1)
		return msg
	#---------------------------------------------------------------------------------------------------
	@dp.callback_query_handler(text="done")
	async def from_f(message: CallbackQuery):
		global listOfClients
		id1 = message.message.chat.id
		id = client.find_client(listOfClients, message.message.chat.id)
		if id == -1: 
			await sessionPizda(message.message)
			return
		await done_accept(message.message)

	#---------------------------------------------------------------------------------------------------
	@dp.callback_query_handler(text="bandage_dwnd")
	async def from_f(message: CallbackQuery):
		global listOfClients
		id1 = message.message.chat.id
		id = client.find_client(listOfClients, message.message.chat.id)
		if id == -1: 
			await sessionPizda(message.message)
			return
		
		bio = BytesIO()
		bio.name = f'{id1}.png'
		listOfClients[id].bandage.save(bio, 'PNG')
		bio.seek(0)
		await message.message.answer_document(bio)


	#---------------------------------------------------------------------------------------------------
	async def start_set(message):
		global listOfClients
		id = client.find_client(listOfClients, message.chat.id)
		if id == -1: 
			await sessionPizda(message)
			return

		up_btn: InlineKeyboardButton = InlineKeyboardButton(text='↑',																			
											callback_data='up')

		info_btn: InlineKeyboardButton = InlineKeyboardButton(
			text=f'{listOfClients[id].pos}/8', callback_data='no')
		
		down_btn: InlineKeyboardButton = InlineKeyboardButton(
			text='↓', callback_data='down')
		
		first_layer_btn: InlineKeyboardButton = InlineKeyboardButton(
			text='Первый слой', callback_data='first')

		bw_btn: InlineKeyboardButton = InlineKeyboardButton(text='В ч/б',
													callback_data='bw')

		negative_btn: InlineKeyboardButton = InlineKeyboardButton(
			text='Инвертировать', callback_data='negative')

		pose_btn: InlineKeyboardButton = InlineKeyboardButton(
			text='Поза', callback_data='pose')

		overlay_btn: InlineKeyboardButton = InlineKeyboardButton(
			text='Оверлей', callback_data='over')
		
		bodyPart_btn: InlineKeyboardButton = InlineKeyboardButton(
			text='Часть тела', callback_data='body_part')
		
		pepetype_btn: InlineKeyboardButton = InlineKeyboardButton(
			text='Тип пепе', callback_data='pepe')
		
		bndg_downl: InlineKeyboardButton = InlineKeyboardButton(
			text='Скачать повязку', callback_data='bandage_dwnd')

		donw_btn: InlineKeyboardButton = InlineKeyboardButton(
			text='Готово ✓', callback_data='done')
		
		reset_btn: InlineKeyboardButton = InlineKeyboardButton(
			text='Сбросить', callback_data='reset')
		
		delete_btn: InlineKeyboardButton = InlineKeyboardButton(
			text='Удаление пикселей над повязкой', callback_data='delete_sw')
		
		pass_btn: InlineKeyboardButton = InlineKeyboardButton(
			text='-', callback_data='passs')
		
		export: InlineKeyboardButton = InlineKeyboardButton(
			text='Экспортировать настройки', callback_data='exp')
		importpar: InlineKeyboardButton = InlineKeyboardButton(
			text='Импортировать настройки', callback_data='imp')

		# Создаем объект инлайн-клавиатуры
		keyboard3: InlineKeyboardMarkup = InlineKeyboardMarkup()
		keyboard3.row(up_btn,   first_layer_btn, bodyPart_btn, export)
		keyboard3.row(info_btn, overlay_btn,     pepetype_btn, importpar)
		keyboard3.row(down_btn, pose_btn,        negative_btn, reset_btn)
		keyboard3.row(pass_btn, delete_btn,        bw_btn,       bndg_downl)
		keyboard3.row(pass_btn, pass_btn,        pass_btn,       donw_btn)
		

		
		listOfClients[id].change_e = not listOfClients[id].change_e
		listOfClients[id].delete_mess = True
		txt11 = "Алекс" if listOfClients[id].slim else "Стив"
		txt1 = f"*Версия скина:* {txt11}\n"
		txt12 = "Вкл" if listOfClients[id].overlay else "Выкл"

		txt13 = "Выкл"
		if listOfClients[id].first_layer == 0: txt13 = "Выкл"
		elif listOfClients[id].first_layer == 1: txt13 = "Подкладка"
		elif listOfClients[id].first_layer == 2: txt13 = "Дублирование повязки"

		body = ["Левая рука", "Левая нога", "Правая рука", "Правая нога"]
		txt7 = f"*Часть тела:* {body[listOfClients[id].absolute_pos]}\n"

		txt14 = "Вкл" if listOfClients[id].bw else "Выкл"
		txt15 = "Вкл" if listOfClients[id].negative else "Выкл"
		txt16 = "Вкл" if listOfClients[id].delete_pix else "Выкл"
		e = "e" if listOfClients[id].change_e else "е"
		txt3 = f"*Оверлей:* {txt12}\n"
		txt4 = f"*Первый слой:* {txt13}\n"
		txt5 = f"*Чёрно-б{e}лый:* {txt14}\n"
		txt6 = f"*Негатив:* {txt15}\n"
		txt8 = f"*Удаление пикселей над повязкой:* {txt16}\n"
		
		try:
				
			msg = await listOfClients[id].info_id.edit_text(
				f"*Параметры:*\n{txt1}{txt3}{txt4}{txt5}{txt6}{txt7}{txt8}",
				reply_markup=keyboard3, parse_mode='Markdown')

		except:pass



	#---------------------------------------------------------------------------------------------------
	@dp.callback_query_handler(text="exp")
	async def from_f(message: CallbackQuery):
		id1 = message.message.chat.id
		global listOfClients
		id = client.find_client(listOfClients, message.message.chat.id)
		if id == -1: 
			await sessionPizda(message.message)
			return
		listOfClients[id].exportJSON(id1)
		await message.message.answer_document(open(f"params{id1}.json", 'rb'))
		os.remove(f'params{id1}.json')

	@dp.callback_query_handler(text="imp")
	async def from_f(message: CallbackQuery):
		id1 = message.message.chat.id
		global listOfClients
		id = client.find_client(listOfClients, message.message.chat.id)
		if id == -1: 
			await sessionPizda(message.message)
			return
		listOfClients[id].wait_to_file = 4
		deny_import: InlineKeyboardButton = InlineKeyboardButton(
			text='Отмена', callback_data='denyImp')

				# Создаем объект инлайн-клавиатуры
		keyboard1: InlineKeyboardMarkup = InlineKeyboardMarkup(
						inline_keyboard=[[deny_import]])
		await listOfClients[id].info_id.edit_text("Окей, теперь отправьте файл настроек в формате JSON", reply_markup=keyboard1)

	#---------------------------------------------------------------------------------------------------
	@dp.callback_query_handler(text="denyImp")
	async def from_f(message: CallbackQuery):
		id1 = message.message.chat.id
		global listOfClients
		id = client.find_client(listOfClients, message.message.chat.id)
		if id == -1: 
			await sessionPizda(message.message)
			return
		listOfClients[id].wait_to_file = 0
		await start_set(message.message)
	#---------------------------------------------------------------------------------------------------

	@dp.callback_query_handler(text="reset")
	async def from_f(message: CallbackQuery):

		id1 = message.message.chat.id
		global listOfClients
		id = client.find_client(listOfClients, message.message.chat.id)
		if id == -1: 
			await sessionPizda(message.message)
			return

		await reset_accept(message.message)

	#---------------------------------------------------------------------------------------------------
	@dp.callback_query_handler(text="up")
	async def from_f(message: CallbackQuery):

		id1 = message.message.chat.id
		global listOfClients
		id = client.find_client(listOfClients, message.message.chat.id)
		if id == -1: 
			await sessionPizda(message.message)
			return
		if listOfClients[id].pos > 0:
			listOfClients[id].pos -= 1

		await render_and_edit(message.message, id, id1)
		await start_set(message.message)

	#---------------------------------------------------------------------------------------------------
	@dp.callback_query_handler(text="delete_sw")
	async def from_f(message: CallbackQuery):

		id1 = message.message.chat.id
		global listOfClients
		id = client.find_client(listOfClients, message.message.chat.id)
		if id == -1: 
			await sessionPizda(message.message)
			return
		listOfClients[id].delete_pix = not listOfClients[id].delete_pix


		await render_and_edit(message.message, id, id1)
		await start_set(message.message)



	#---------------------------------------------------------------------------------------------------
	@dp.callback_query_handler(text="pose")
	async def from_f(message: CallbackQuery):

		id1 = message.message.chat.id
		global listOfClients
		id = client.find_client(listOfClients, message.message.chat.id)
		if id == -1: 
			await sessionPizda(message.message)
			return
		listOfClients[id].pose += 1

		if listOfClients[id].pose > len(listOfClients[id].poses[0]) - 1: listOfClients[id].pose = 0

		await render_and_edit(message.message, id, id1)
		await start_set(message.message)

	#---------------------------------------------------------------------------------------------------
	@dp.callback_query_handler(text="bw")
	async def from_f(message: CallbackQuery):

		id1 = message.message.chat.id
		global listOfClients
		id = client.find_client(listOfClients, message.message.chat.id)
		if id == -1: 
			await sessionPizda(message.message)
			return
		listOfClients[id].bw = not listOfClients[id].bw

		await render_and_edit(message.message, id, id1)

		await start_set(message.message)

	#---------------------------------------------------------------------------------------------------
	@dp.callback_query_handler(text="negative")
	async def from_f(message: CallbackQuery):

		id1 = message.message.chat.id
		global listOfClients
		id = client.find_client(listOfClients, message.message.chat.id)
		if id == -1: 
			await sessionPizda(message.message)
			return
		listOfClients[id].negative = not listOfClients[id].negative

		await render_and_edit(message.message, id, id1)


		await start_set(message.message)

	#---------------------------------------------------------------------------------------------------
	@dp.callback_query_handler(text="down")
	async def from_f(message: CallbackQuery):
		id1 = message.message.chat.id
		global listOfClients
		id = client.find_client(listOfClients, message.message.chat.id)
		if id == -1: 
			await sessionPizda(message.message)
			return
		if listOfClients[id].pos < 8:
			listOfClients[id].pos += 1

		await render_and_edit(message.message, id, id1)
		await start_set(message.message)

	#---------------------------------------------------------------------------------------------------
	@dp.callback_query_handler(text="first")
	async def from_f(message: CallbackQuery):
		id1 = message.message.chat.id
		global listOfClients
		id = client.find_client(listOfClients, message.message.chat.id)
		if id == -1: 
			await sessionPizda(message.message)
			return
		listOfClients[id].first_layer += 1

		if listOfClients[id].first_layer > 2: listOfClients[id].first_layer = 0

		await render_and_edit(message.message, id, id1)
		await start_set(message.message)

	#---------------------------------------------------------------------------------------------------
	@dp.callback_query_handler(text="over")
	async def from_f(message: CallbackQuery):
		id1 = message.message.chat.id
		global listOfClients
		id = client.find_client(listOfClients, message.message.chat.id)
		if id == -1: 
			await sessionPizda(message.message)
			return
		listOfClients[id].overlay = not listOfClients[id].overlay

		await render_and_edit(message.message, id, id1)
		await start_set(message.message)


	#---------------------------------------------------------------------------------------------------
	@dp.callback_query_handler(text="body_part")
	async def from_f(message: CallbackQuery):
		id1 = message.message.chat.id
		global listOfClients
		id = client.find_client(listOfClients, message.message.chat.id)
		if id == -1: 
			await sessionPizda(message.message)
			return
		listOfClients[id].absolute_pos += 1

		if listOfClients[id].absolute_pos > 3: listOfClients[id].absolute_pos = 0

		await render_and_edit(message.message, id, id1)
		await start_set(message.message)
	#---------------------------------------------------------------------------------------------------
	@dp.callback_query_handler(text="pepe")
	async def from_f(message: CallbackQuery):
		id1 = message.message.chat.id
		global listOfClients
		id = client.find_client(listOfClients, message.message.chat.id)
		if id == -1: 
			await sessionPizda(message.message)
			return
		listOfClients[id].pepe_type += 1

		if listOfClients[id].pepe_type > len(listOfClients[id].pepes) - 1: listOfClients[id].pepe_type = 0

		await render_and_edit(message.message, id, id1)
		await start_set(message.message)
	#---------------------------------------------------------------------------------------------------

	@dp.callback_query_handler(text="man_steve")
	async def from_f(message: CallbackQuery):
		id1 = message.message.chat.id
		global listOfClients
		id = client.find_client(listOfClients, message.message.chat.id)
		if id == -1: 
			await sessionPizda(message.message)
			return
		listOfClients[id].slim_cust = 1
		await listOfClients[id].info_id.delete()
		listOfClients[id].info_id = 0

		await listOfClients[id].prerender()
		listOfClients[id].slim = False
		skin_rer = await listOfClients[id].rerender()
		bio = BytesIO()
		bio.name = f'{id1}.png'
		skin_rer.save(bio, 'PNG')
		bio.seek(0)

		msg = await message.message.answer_photo(bio, "Вот предварительный просмотр")
		listOfClients[id].prewiew_id = msg


		msg = await colorDialog(message.message, id)
		listOfClients[id].info_id = msg

	#---------------------------------------------------------------------------------------------------

	@dp.callback_query_handler(text="man_alex")
	async def from_f(message: CallbackQuery):
		id1 = message.message.chat.id
		global listOfClients
		id = client.find_client(listOfClients, message.message.chat.id)
		if id == -1: 
			await sessionPizda(message.message)
			return
		listOfClients[id].slim_cust = 2

		await listOfClients[id].info_id.delete()
		listOfClients[id].info_id = 0
		await listOfClients[id].prerender()
		listOfClients[id].slim = True
		skin_rer = await listOfClients[id].rerender()
		bio = BytesIO()
		bio.name = f'{id1}.png'
		skin_rer.save(bio, 'PNG')
		bio.seek(0)

		msg = await message.message.answer_photo(bio, "Вот предварительный просмотр")
		listOfClients[id].prewiew_id = msg


		msg = await colorDialog(message.message, id)
		listOfClients[id].info_id = msg
	#---------------------------------------------------------------------------------------------------
	@dp.message_handler(content_types=['text'])
	async def echo(message: types.Message):

		global listOfClients
		id = client.find_client(listOfClients, message.chat.id)
		if id == -1: 
			if message.chat.id != -1001980044675: await sessionPizda(message)
			return
		id1 = message.chat.id

		

		if listOfClients[id].waitToReview:
			await bot.send_message(chat_id=-1001980044675, text=f"*{message.from_user.username}* оставил отзыв:\n{message.text}\nЕго id: {message.from_user.id}", parse_mode="Markdown")
			listOfClients[id].waitToReview = False
			await message.answer("Спасибо за отзыв!\nПосмотреть список всех отзывов можно отправив /reviews")
			now_time_log = datetime.now(pytz.timezone('Etc/GMT-3'))

			now_time_format = "{}.{}.{}-{}:{}".format(now_time_log.day,
												now_time_log.month,
												now_time_log.year,
												now_time_log.hour,
												now_time_log.minute)
			if not os.path.isfile("data/reviews.npy"):
				np.save(arr=np.array([]), file="data/reviews.npy")
				reviewsList = []
			else: 
				reviewsListNp = np.load("data/reviews.npy")
				reviewsList = reviewsListNp.tolist()

			reviewsList.insert(0, [f"{now_time_format}:*\n{message.text}", message.from_user.id])

			np.save(arr=np.array(reviewsList), file="data/reviews.npy")
		elif listOfClients[id].wait_to_support:
			await bot.send_message(chat_id=-1001980044675, text=f"{message.text}\n\nОтправил: {message.from_user.username}\nЕго id: {message.from_user.id}")
			listOfClients[id].wait_to_support = False
		elif message.from_user.is_bot == False:
			
			#if listOfClients[id].delete_mess: await message.delete()
		

			if listOfClients[id].wait_to_file == 2:
				done = await listOfClients[id].init_mc_n(message.text)
				if done == 1 or done == 3:
					if done == 3: 
						msg_del = await message.answer("У вашего скина непрозрачный фон!\nПредпросмотр будет некорректным!")
						asyncio.create_task(delete_message(msg_del, 10))
					listOfClients[id].wait_to_file = 0
					await listOfClients[id].import_msg.delete()
					await message.delete()

					await listOfClients[id].prerender()

					skin_rer = await listOfClients[id].rerender()
					bio = BytesIO()
					bio.name = f'{id1}.png'
					skin_rer.save(bio, 'PNG')
					bio.seek(0)

					msg = await message.answer_photo(bio, "Вот предварительный просмотр")
					listOfClients[id].prewiew_id = msg


					msg = await colorDialog(message, id)
					listOfClients[id].info_id = msg

				elif done == 4: 
					await listOfClients[id].import_msg.delete()
					await message.delete()
					keyboard1: InlineKeyboardMarkup = InlineKeyboardMarkup()
					big_button_4: InlineKeyboardButton = InlineKeyboardButton(
						text='Стив', callback_data='man_steve')

					big_button_5: InlineKeyboardButton = InlineKeyboardButton(
						text='Алекс', callback_data='man_alex')

					keyboard1.row(big_button_4, big_button_5)
					msg = await message.answer("Извините, боту не удалось корректно определить тип вашего скина.\nПожалуйста, выберете правильный:", reply_markup=keyboard1)
					listOfClients[id].info_id = msg
				

				else:
					await message.answer("Аккаунт с таким именем не найден(")
			if listOfClients[id].wait_to_file == 3:
				try:
					try: await listOfClients[id].error_msg.delete()
					except: pass
					await message.delete()
					msg_c = message.text.lstrip('#')

					input1 = msg_c.split(", ")
					input2 = msg_c.split(",")

					if len(input1) == 1 and len(input2) == 1:
						colour = tuple(int(msg_c[i:i + 2], 16) for i in (0, 2, 4))
					else:
						if len(input1) == 1:
							colour = (int(input2[0]), int(input2[1]), int(input2[2]))
						else:
							colour = (int(input1[0]), int(input1[1]), int(input1[2]))

					r, g, b = colour
					if r > 255 or g > 255 or b > 255 or r < 0 or g < 0 and b < 0: 
						raise ZeroDivisionError
					listOfClients[id].colour = colour

					
					listOfClients[id].wait_to_file = 0
					await render_and_edit(message, id, id1)

					big_button_4: InlineKeyboardButton = InlineKeyboardButton(
						text='Подтвердить выбор цвета', callback_data='done_c')

					big_button_5: InlineKeyboardButton = InlineKeyboardButton(
						text='Изменить цвет', callback_data='colD')

					# Создаем объект инлайн-клавиатуры
					keyboard1: InlineKeyboardMarkup = InlineKeyboardMarkup(
						inline_keyboard=[[big_button_4], [big_button_5]])
					msg = await listOfClients[id].info_id.edit_text("Готово?", reply_markup=keyboard1)
					listOfClients[id].info_id = msg

				except Exception as e:
					print(e)
					text1 = "Бот принимает цвета HEX и RGB, в форматах:\n#ffffff\nffffff\n255,255,255\n255, 255, 255 и т.п."
					msg = await message.answer("Не удалось получить цвет(\n" + text1 + "\nПопробуйте ещё раз")
					listOfClients[id].error_msg = msg

else:
	@dp.message_handler(content_types=['any'])
	async def echo(message: types.Message):
		await message.answer("Извините, сейчас проводятся техработы по улучшению бота\n\n*Мы скоро вернёмся!*", parse_mode="Markdown")
if on_server: keep_alive()

@dp.message_handler()
async def event():
	try:
		event_da = da.get_event()
		da.reset_event()
		if event_da != -1:
			for x in range(len(event_da)):
				await bot.send_message(event_da[x][1], f"Пополнение на {event_da[x][0]} RUB")
				await bot.send_message(chat_id=-1001980044675, text=f"{event_da[x][2]} пополнил баланс на {event_da[x][0]} RUB")

				if float(event_da[x][3]) < 200 and float(event_da[x][4]) >= 200:
					await bot.send_message(chat_id=-1001980044675, text=f"Сделать скин на картинку игроку {event_da[x][2]}")
			
	except Exception:
		pass


async def scheduler():
    schedule.every(5).seconds.do(event)
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)
        
async def on_startup(dp): 
    asyncio.create_task(scheduler())

if __name__ == '__main__':
	started = True
	while started:
		try:
			executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
			started = False
		except Exception:
			started = True
			print("An error has occurred, reboot in 10 seconds")
			time1.sleep(10)
			print("rebooting...")