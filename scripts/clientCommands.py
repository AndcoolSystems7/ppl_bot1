import scripts.da as da
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging 
from aiogram.utils.markdown import link
from io import BytesIO
import scripts.help_renderer as help_renderer
import os
import numpy as np
def init(bot, dp, on_server):
	@dp.message_handler(commands=['changeUsername', 'changeBalance'])
	async def send_welcome(message: types.Message):
		if message.from_user.id == 1197005557:
			message_list = message.text.split(" ")
			list = da.get_list()
			id = -1
			finded = False
			for x in range(len(list)):
				if int(list[x][2]) == int(message_list[1]):
					finded = True
					id = x
					break
			if not finded: await message.answer(text="User not found")
			else:
				if message_list[0] == '/changeUsername':
					list[id][0] = message_list[2]
					da.set_list(list)
					await message.answer(text=f"Done")
				
				if message_list[0] == '/changeBalance':
					list[id][1] = str(message_list[2])
					da.set_list(list)
					await message.answer(text="Done")
	#---------------------------------------------------------------------------------------------------

	@dp.message_handler(commands=['checkme'])
	async def send_welcome(message: types.Message):
		list = da.get_list()
		finded = False
		for x in range(len(list)):
			if int(list[x][2]) == message.from_user.id:
				await message.answer(text=f"Здравствуйте, {list[x][0]}, ваш баланс {list[x][1]} *RUB*", parse_mode="Markdown")
				finded = True
				break
		if not finded: await message.answer(text=f"Вы ещё не донатили :)")
	#---------------------------------------------------------------------------------------------------

	@dp.message_handler(commands=['sendToId'])
	async def send_welcome(message: types.Message):
		if message.from_user.id == 1197005557:
			id = message.text.split(" ")[1]
			text = " ".join(message.text.split(" ")[2:])
			await bot.send_message(id, "Ответ администратора:\n" + text)
	
	#---------------------------------------------------------------------------------------------------
	@dp.message_handler(commands=['help'])
	async def send_welcome(message: types.Message):
		link3 = link('Дискорд', 'https://discordapp.com/users/812990469482610729/')
		text1 = "PPL повязка - это бот, созданный для наложения повязки Пепеленда на ваш скин.\n"
		text2 = "Для начала работы с ботом отправьте /start и следуйте дальнейшим инструкциям.\n\n"
		text3 = f"При возникновении вопросов или ошибок обращайтесь в {link3}\nили *отправив команду* /support\n\n"
		link1 = link('Пост', 'https://discord.com/channels/447699225078136832/1114275416404922388')
		link2 = link('сайт', 'http://pplbandagebot.ru')

		text6 = f"Полезные ссылки:\n{link1} в Идеях\nОфициальный {link2} проекта\n\n"
		if on_server:
			f = open("pyproject.toml")
			ver = f.read().split("\n")[2][11:-1]
			text5 = f"Версия *{ver}*\n"
			f.close()
		else: text5 = ""
		text4 = "*Created by AndcoolSystems*"
		donate_text = ""
		if os.path.isfile("data/donations.npy"):
			donate_text = "\n\nЛюди, поддержавшие проект:\n"
			donateList_npy = np.load("data/donations.npy")
			donateList = donateList_npy.tolist()

			donateList = da.sortir(donateList)

			count = 0
			for x_p in range(len(donateList)):
				if donateList[x_p][0] != 0:
					count += 1
			count = min(count, 10)
			emotes = ["🥇", "🥈", "🥉"]
			for x in range(count):
				emote = emotes[x] if x < 3 else ""
				donate_text = f"{donate_text}{x + 1}. {emote}*{donateList[x][0]}* - {round(float(donateList[x][1]), 2)} *RUB*\n"

			donate_text = donate_text + "\nХотите сюда? Тогда вы можете поддержать разработчика, отправив /donate"



		bio = BytesIO()
		bio.name = f'{message.from_user.id}.png'
		help_renderer.render().save(bio, 'PNG')
		bio.seek(0)

		await message.reply_photo(bio, caption=text1+text2+text3+text6+text5+text4+donate_text, parse_mode='Markdown')

	#---------------------------------------------------------------------------------------------------
	@dp.message_handler(commands=['changelog'])
	async def send_welcome(message: types.Message):
		
		f = open("README.md", encoding="UTF8")
		ver = "Обновление" + f.read().split("Обновление")[1]
		f.close()

		big_button_1: InlineKeyboardButton = InlineKeyboardButton(
			text='Полный список обновлений', url="http://pplbandagebot.ru/changelog.html")

		keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
			inline_keyboard=[[big_button_1]])
		await message.answer(text=f"{ver}", parse_mode= 'Markdown', reply_markup=keyboard)


	#---------------------------------------------------------------------------------------------------

	@dp.message_handler(commands=['donate'])
	async def send_welcome(message: types.Message):
		"""img = Image.open("res/presets/thanks.png")
		bio = BytesIO()
		bio.name = f'{id}.png'
		img.save(bio, 'PNG')
		bio.seek(0)"""
	
		big_button_1: InlineKeyboardButton = InlineKeyboardButton(
			text='DonationAlerts', url="https://www.donationalerts.com/r/andcool_systems")

		keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
			inline_keyboard=[[big_button_1]])
		"""await message.answer_photo(photo=bio, caption=f"Вы можете поддержать разработчиков бота, отправив донат через сервис DonationAlerts\nВ начале сообщения к донату оставьте число *{message.from_user.id}*, а затем, через пробел оставьте своё сообщение.",
												reply_markup=keyboard, parse_mode="Markdown")"""
		text = f"Вы можете поддержать разработчиков бота, отправив донат через сервис DonationAlerts\nВ начале сообщения к донату оставьте число `{message.from_user.id}`, а затем, через пробел оставьте своё сообщение."
		await message.answer(text, reply_markup=keyboard)

	#---------------------------------------------------------------------------------------------------