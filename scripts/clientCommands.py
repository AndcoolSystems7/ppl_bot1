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
def findBadge(list, id1):
	id = -1
	for x in range(len(list)):
		if int(list[x][0]) == int(id1):
			id = x
			break
	return id
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
		link2 = link('сайт', 'https://pplbandagebot.ru')
		link4 = link('Шейп — Студия Minecraft', 'https://vk.com/shapestd')
		text7 = '\n\n*ЭТОТ БОТ НЕ ЯВЛЯЕТСЯ ОФИЦИАЛЬНЫМ [ПРОДУКТОМ/УСЛУГОЙ/СОБЫТИЕМ И т.п.] MINECRAFT. НЕ ОДОБРЕНО И НЕ СВЯЗАНО С КОМПАНИЕЙ MOJANG ИЛИ MICROSOFT*'

		text6 = f"Полезные ссылки:\n{link1} в Идеях\nОфициальный {link2} проекта\n\n"
		if on_server:
			f = open("pyproject.toml")
			ver = f.read().split("\n")[2][11:-1]
			text5 = f"Версия *{ver}*\n"
			f.close()
		else: text5 = ""
		text4 = f"*Created by AndсоolSystems*\nПродакшн: {link4}" #Продакшн: {link4}
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
			
			emotes = ["🥇", "🥈", "🥉"]
			for x in range(count):
				emote = emotes[x] if x < 3 else ""
				donate_text = f"{donate_text}{x + 1}. {emote}*{donateList[x][0]}* - {round(float(donateList[x][3]), 2)} *RUB*\n"

			donate_text = donate_text + "\nХотите сюда? Тогда вы можете поддержать разработчика, отправив /donate"



		bio = BytesIO()
		bio.name = f'{message.from_user.id}.png'
		help_renderer.render().save(bio, 'PNG')
		bio.seek(0)
		big_button_5: InlineKeyboardButton = InlineKeyboardButton(
			text='Контакты разработчиков', callback_data='contacts')

		keyboard1: InlineKeyboardMarkup = InlineKeyboardMarkup(
			inline_keyboard=[[big_button_5]])
		await message.reply_photo(bio, caption=text1+text2+text3+text6+text5+text4+donate_text+text7, parse_mode='Markdown', reply_markup=keyboard1)

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
		text = f"Вы можете поддержать разработчиков бота, отправив донат через сервис DonationAlerts\nВ начале сообщения к донату оставьте число `{message.from_user.id}` *\(нажмите по числу для копирования\)*, а затем, через пробел оставьте своё сообщение\.\nDonationAlerts иногда не видит пришедшие донаты, поэтому если через 2\-3 минуты донат не пришёл обращайтесь в /support"
		await message.answer(text, reply_markup=keyboard, parse_mode="MarkdownV2")


	#---------------------------------------------------------------------------------------------------

	@dp.message_handler(commands=['ban'])
	async def send_welcome(message: types.Message):
		if not os.path.isfile("data/banned.npy"):
			np.save(arr=np.array([]), file="data/banned.npy")
			reviewsList = []
		else: 
			reviewsListNp = np.load("data/banned.npy")
			reviewsList = reviewsListNp.tolist()
		id = int(message.text.split(" ")[1])
		andcool_id = -1001980044675
		if andcool_id == message.chat.id:
			if not id in reviewsList: 
				reviewsList.append(id)
				np.save(arr=np.array(reviewsList), file="data/banned.npy")
				await message.answer(text="Забанен!")
			else: await message.answer(text="Человек уже забанен!")

	#---------------------------------------------------------------------------------------------------

	@dp.message_handler(commands=['unban'])
	async def send_welcome(message: types.Message):
		if not os.path.isfile("data/banned.npy"):
			np.save(arr=np.array([]), file="data/banned.npy")
			reviewsList = []
		else: 
			reviewsListNp = np.load("data/banned.npy")
			reviewsList = reviewsListNp.tolist()
		id = int(message.text.split(" ")[1])
		andcool_id = -1001980044675
		if andcool_id == message.chat.id:
			if id in reviewsList: 
				reviewsList.remove(id)
				np.save(arr=np.array(reviewsList), file="data/banned.npy")
				await message.answer(text="Разбанен!")
			else: await message.answer(text="Человек не забанен")


	#---------------------------------------------------------------------------------------------------

	@dp.message_handler(commands=['info'])
	async def send_welcome(message: types.Message):
		id = int(message.text.split(" ")[1])
		andcool_id = -1001980044675
		try:
			member = await bot.get_chat_member(id, id)
			await message.answer(text=member)
		except Exception as e: await message.answer(text=e)
		#print(member)


	#---------------------------------------------------------------------------------------------------

	@dp.message_handler(commands=['changeBadge'])
	async def send_welcome(message: types.Message):
		try:
			id = int(message.text.split(" ")[1])
			t = message.text.split(" ")[2:]
			em = " ".join(t)
			andcool_id = 1197005557
			
			if andcool_id == message.from_user.id:
				badgesListn = np.load("data/badges.npy")
				badgesList = badgesListn.tolist()

				id1 = findBadge(badgesList, id)
				if id1 == -1: badgesList.append([int(id), em, em])
				else: 
					badgesList[id1][1] = em
					badgesList[id1][2] = em

				np.save(arr=np.array(badgesList), file="data/badges.npy")
				
				await message.answer(text="Badge changed!")
		except Exception as e: await message.answer(text=e)

	#---------------------------------------------------------------------------------------------------

	@dp.message_handler(commands=['badgesList'])
	async def send_welcome(message: types.Message):
		#try:
		if True:
			andcool_id = 1197005557
			
			if andcool_id == message.from_user.id:
				badgesListn = np.load("data/badges.npy")
				badgesList = badgesListn.tolist()
				text = []
				for x in badgesList:
					try:
						member = await bot.get_chat_member(int(x[0]), int(x[0]))
						first = str(member.user.first_name) if member.user.first_name != None else ""
						kast_a = " " if first != "" else ""
						last = (kast_a + str(member.user.last_name)) if member.user.last_name != None else ""
					
						text.append(f'{x[0]} - {first}{last} - {x[1]}\n')
					except:pass

				t = ''.join(text)
				await message.answer(text=t)
		#except Exception as e: await message.answer(text=e)

	#---------------------------------------------------------------------------------------------------

	@dp.message_handler(commands=['setBadgeCost'])
	async def send_welcome(message: types.Message):
		try:
			cost = float(message.text.split(" ")[1])
			
			andcool_id = 1197005557
			
			if andcool_id == message.from_user.id:
				if os.path.isfile("data/cost.npy"):
					badgesListn = np.load("data/cost.npy")
					badgesList = badgesListn.tolist()
					badgesList = [cost]
					np.save(arr=np.array(badgesList), file="data/cost.npy")
				else:
					badgesList = [cost]
					np.save(arr=np.array(badgesList), file="data/cost.npy")
				await message.answer(text="Cost changed!")
		except Exception as e: await message.answer(text=e)


	#---------------------------------------------------------------------------------------------------

	@dp.message_handler(commands=['setName'])
	async def send_welcome(message: types.Message):
		try:
			andcool_id = 1197005557
			
			if andcool_id == message.from_user.id:
				id = int(message.text.split(" ")[1])
				t = message.text.split(" ")[2:]
				em = " ".join(t)
				
				if os.path.isfile("data/names.npy"):
					badgesListn = np.load("data/names.npy")
					badgesList = badgesListn.tolist()
					f = False
					for x in range(len(badgesList)):
						if int(badgesList[x][0]) == id: 
							badgesList[x][1] = em
							f = True
							break
					if not f: badgesList.append([id, em])
					np.save(arr=np.array(badgesList), file="data/names.npy")
				else:
					badgesList = [[id, em]]
					np.save(arr=np.array(badgesList), file="data/names.npy")
				await message.answer(text="Nick changed!")
		except Exception as e: await message.answer(text=e)

	#---------------------------------------------------------------------------------------------------

	@dp.message_handler(commands=['releaseName'])
	async def send_welcome(message: types.Message):
		andcool_id = 1197005557
			
		if andcool_id == message.from_user.id:
			id = int(message.text.split(" ")[1])	
			try:
				if os.path.isfile("data/names.npy"):
					badgesListn = np.load("data/names.npy")
					badgesList = badgesListn.tolist()
					toPop = []
					for x in range(len(badgesList)):
						if int(badgesList[x][0]) == id: 
							toPop.append(x)
					popC = 0
					for x in toPop:
						badgesList.pop(x - popC)
						popC += 1
					np.save(arr=np.array(badgesList), file="data/names.npy")
				await message.answer(text="Nick released!")
			except Exception as e: await message.answer(text=e)

	@dp.message_handler(commands=['setDistribution'])
	async def send_welcome(message: types.Message):
		try:
			emoji = message.text.split(" ")[1]
			t = message.text.split(" ")[2:]
			em = " ".join(t)
			
			andcool_id = 1197005557
			
			if andcool_id == message.from_user.id:
				if os.path.isfile("data/distribution.npy"):
					badgesListn = np.load("data/distribution.npy")
					badgesList = badgesListn.tolist()
					badgesList = [emoji, em]
					np.save(arr=np.array(badgesList), file="data/distribution.npy")
				else:
					badgesList = [emoji, em]
					np.save(arr=np.array(badgesList), file="data/distribution.npy")
				await message.answer(text="distribution changed!")
		except Exception as e: await message.answer(text=e)


	#---------------------------------------------------------------------------------------------------



	
		