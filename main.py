"""
Pepeland bondage bot
Проект защищён авторским правом
created by AndcoolSystems, 2023©
"""

import logging
logging.basicConfig(level=logging.INFO)
try: 
	import replit
	on_server = True
except: on_server = False

server_text = "replit" if on_server else "local"
logging.info(f"Running on {server_text} server")
#print(f"INFO:Running on {server_text} server")

if on_server: from background import keep_alive

import client
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

if on_server: API_TOKEN = '6121533259:AAHe4O1XP63PtF6RfYf_hJ5QFyMp6J387SU'
else: API_TOKEN = '5850445478:AAFx4SZdD1IkSWc4h_0qU9IoXyT8VAElbTE'


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
listOfClients = []

#---------------------------------------------------------------------------------------------------
@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
	text1 = "PPL повязка - это бот, созданный для наложения повязки Пепеленда на ваш скин.\n"
	text2 = "Для начала работы с ботом отправьте /start и следуйте дальнейшим инструкциям.\n\n"
	text3 = "При возникновении вопросов или ошибок обращайтесь в Дискорд andcoolsystems\n\n"
	if on_server:
		f = open("pyproject.toml")
		ver = f.read().split("\n")[2][11:-1]
		text5 = f"Версия *{ver}*\n"
		f.close()
	else: text5 = ""
	text4 = "*Created by AndcoolSystems*"
	await message.answer(text=text1+text2+text3+text5+text4, parse_mode= 'Markdown')

#---------------------------------------------------------------------------------------------------
@dp.message_handler(commands=['changelog'])
async def send_welcome(message: types.Message):
	
	f = open("README.md", encoding="UTF8")
	ver = "Обновление" + f.read().split("Обновление")[1]
	f.close()

	text = link('тут', 'https://github.com/AndcoolSystems7/PepelandBotChangelog/blob/main/README.md')
	await message.answer(text=f"{ver}Полный список обновлений можно посмотреть {text}", parse_mode= 'Markdown')


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
	keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
		inline_keyboard=[[big_button_2], [big_button_1]])
	await message.answer("Привет! Давай начнём.\nОткуда брать скин?",
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

	if os.path.isfile("usr.txt"):
		userListFile = open("usr.txt", 'r', encoding='utf-8')
		f_usr_list = userListFile.read().split("\n")
		userListFile.close()
		userListFile = open("usr.txt", 'a', encoding='utf-8')

	else:
		userListFile = open("usr.txt", 'w', encoding='utf-8')
		userListFile.close()
		userListFile = open("usr.txt", 'a', encoding='utf-8')

	if os.path.isfile("usr_use.txt"):
		userListFile1 = open("usr_use.txt", 'a', encoding='utf-8')

	else:
		userListFile1 = open("usr_use.txt", 'w', encoding='utf-8')
		userListFile1.close()
		userListFile1 = open("usr_use.txt", 'a', encoding='utf-8')
	if f_usr_list != []:
		if not str(f"{message.from_user.username} - {message.from_user.id}") in f_usr_list:
			userListFile.write(f"{message.from_user.username} - {message.from_user.id}\n")

	userListFile1.write(f"{message.from_user.username} - {now_time_format} - {message.from_user.id}\n")
	userListFile.close()
	userListFile1.close()

#---------------------------------------------------------------------------------------------------
@dp.message_handler(commands=['donate'])
async def send_welcome(message: types.Message):

	big_button_1: InlineKeyboardButton = InlineKeyboardButton(
		text='DonationAlerts', url="https://www.donationalerts.com/r/andcool_systems")

	keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
		inline_keyboard=[[big_button_1]])
	await message.answer("Вы можете поддержать разработчиков бота, отправив донат через сервис DonationAlerts",
											 reply_markup=keyboard)

#---------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text="file")
async def from_f(message: CallbackQuery):
	global listOfClients
	id = client.find_client(listOfClients, message.message.chat.id)
	if id == -1: 
		await message.message.answer("Ваша сессия была завершена\nОтпраьте /start для начала работы")
		return
	await message.message.answer(
		'Хорошо, теперь отправь мне свой скин.\nОбязательно при отправке убери галочку "Сжать изображение"'
	)
	await message.message.delete()
	
	listOfClients[id].wait_to_file = 1

#---------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text="nick")
async def from_f(message: CallbackQuery):
	global listOfClients
	id = client.find_client(listOfClients, message.message.chat.id)
	if id == -1: 
		await message.message.answer("Ваша сессия была завершена\nОтпраьте /start для начала работы")
		return
	await message.message.answer("Хорошо, теперь отправь мне свой никнейм.")
	await message.message.delete()
	
	listOfClients[id].wait_to_file = 2

#---------------------------------------------------------------------------------------------------
@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message: types.Message):
	global listOfClients
	id = client.find_client(listOfClients, message.chat.id)
	if listOfClients[id].wait_to_file == 1:
		await message.reply('Пожалуйста, отправьте мне развёртку скина как файл или при отпраке снимите галочку "Сжать изображение"')

#---------------------------------------------------------------------------------------------------
@dp.message_handler(content_types=['document'])
async def handle_docs_photo(message: types.Message):
	global listOfClients
	id = client.find_client(listOfClients, message.chat.id)
	if id == -1: 
		await message.answer("Ваша сессия была завершена\nОтпраьте /start для начала работы")
		return

	if listOfClients[id].wait_to_file == 1:
		id1 = message.chat.id

		if document := message.document:
			await document.download(destination_file=f'{id1}.png', )
		try:
			usr_img = Image.open(f'{id1}.png').convert("RGBA")
			w, h = usr_img.size
			done = True
			for y_ch in range(3):
				for x_ch in range(3):
					r, g, b, t = usr_img.getpixel((x_ch, y_ch))
					if t != 0:
						done = False
						break

			if not done:
				await message.answer("У вашего скина непрозрачный фон!\nПредпросмотр будет некорректным!")
	
			if w == 64 and h == 64:
				await listOfClients[id].init_mc_f(usr_img)
				listOfClients[id].wait_to_file = 0

				await listOfClients[id].prerender()

				skin_rer = await listOfClients[id].rerender()
				bio = BytesIO()
				bio.name = f'{id1}.png'
				skin_rer.save(bio, 'PNG')
				bio.seek(0)

				msg = await message.answer_photo(bio,
												"Вот предварительный просмотр")
				listOfClients[id].prewiew_id = msg
				


				os.remove(f'{id1}.png')

				msg = await colorDialog(message, id)
				listOfClients[id].info_id = msg
			else:
				await message.reply(
					"Пожалуйста, отправьте развёртку скина в формате png с разрешением 64х64 пикселей"
				)
				usr_img.close()
				os.remove(f'{id1}.png')
		except:
			await message.reply(
				"Пожалуйста, отправьте развёртку скина в формате png с разрешением 64х64 пикселей"
			)
			os.remove(f'{id1}.png')


#---------------------------------------------------------------------------------------------------
colour_txt = ["blue", "yellow", "green", "red", "pink", "violet", "orange", "black", "white"]
@dp.callback_query_handler(text=colour_txt)
async def from_f(message: CallbackQuery):

	id1 = message.message.chat.id
	global listOfClients
	global colour_txt
	id = client.find_client(listOfClients, message.message.chat.id)
	if id == -1: 
		await message.message.answer("Ваша сессия была завершена\nОтпраьте /start для начала работы")
		return


	colours = [(61, 58, 201), (250, 213, 30), (85, 163, 64), (176, 30, 30), (252, 15, 192), (105, 0, 198), (255, 102, 0), (0, 0, 0), (255, 255, 255)]
	listOfClients[id].colour = colours[colour_txt.index(message.data)]

	await render_and_edit(message.message, id, id1)
	await acceptChoose(message.message)


#---------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text="done_c")
async def from_f(message: CallbackQuery):

	id1 = message.message.chat.id
	global listOfClients
	id = client.find_client(listOfClients, message.message.chat.id)
	if id == -1: 
		await message.message.answer("Ваша сессия была завершена\nОтпраьте /start для начала работы")
		return
	await start_set(message.message)

#---------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text="custom")
async def from_f(message: CallbackQuery):

	id1 = message.message.chat.id
	global listOfClients
	id = client.find_client(listOfClients, message.message.chat.id)
	if id == -1: 
		await message.message.answer("Ваша сессия была завершена\nОтпраьте /start для начала работы")
		return
	await listOfClients[id].info_id.delete()
	listOfClients[id].colour = 5

	listOfClients[id].wait_to_file = 3

	#await message.message.delete()

	msg = await message.message.answer(
		"Теперь отправьте свой цвет в формате *HEX* или *RGB*\nЦвет можно получить на сайте https://colorscheme.ru/color-converter.html", parse_mode= 'Markdown'
	)
	listOfClients[id].info_id = msg

#---------------------------------------------------------------------------------------------------
async def acceptChoose(message):
	global listOfClients
	id = client.find_client(listOfClients, message.chat.id)
	if id == -1: 
		await message.answer("Ваша сессия была завершена\nОтпраьте /start для начала работы")
		return
	big_button_4: InlineKeyboardButton = InlineKeyboardButton(
			text='Готово ✓', callback_data='done_d')

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
		await message.answer("Ваша сессия была завершена\nОтпраьте /start для начала работы")
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
		await message.message.answer("Ваша сессия была завершена\nОтпраьте /start для начала работы")
		return
	await start_set(message.message)


#---------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text="resetAccept")
async def from_f(message: CallbackQuery):
	global listOfClients
	id = client.find_client(listOfClients, message.message.chat.id)
	id1 = message.message.chat.id
	if id == -1: 
		await message.message.answer("Ваша сессия была завершена\nОтпраьте /start для начала работы")
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
		await message.message.answer("Ваша сессия была завершена\nОтпраьте /start для начала работы")
		return
	msg = await colorDialog(message.message, id)
	
	
#---------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text="done_d")
async def from_f(message: CallbackQuery):
	global listOfClients
	id = client.find_client(listOfClients, message.message.chat.id)
	if id == -1: 
		await message.message.answer("Ваша сессия была завершена\nОтпраьте /start для начала работы")
		return
	await start_set(message.message)
#---------------------------------------------------------------------------------------------------

async def done_accept(message):
	global listOfClients
	id = client.find_client(listOfClients, message.chat.id)
	if id == -1: 
		await message.answer("Ваша сессия была завершена\nОтпраьте /start для начала работы")
		return
	big_button_4: InlineKeyboardButton = InlineKeyboardButton(
			text='Да ✓', callback_data='donetAccept')

	big_button_5: InlineKeyboardButton = InlineKeyboardButton(
		text='Нет ✗', callback_data='doneDeny')

	keyboard1: InlineKeyboardMarkup = InlineKeyboardMarkup(
		inline_keyboard=[[big_button_4], [big_button_5]])
	await listOfClients[id].info_id.edit_text("Готово? После завершения отредактировать скин будет невозможно!", reply_markup=keyboard1)


#---------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text="donetAccept")
async def from_f(message: CallbackQuery):
	global listOfClients
	id1 = message.message.chat.id
	id = client.find_client(listOfClients, message.message.chat.id)
	if id == -1: 
		await message.message.answer("Ваша сессия была завершена\nОтпраьте /start для начала работы")
		return
	bio = BytesIO()
	bio.name = f'{id1}.png'
	listOfClients[id].skin_raw.save(bio, 'PNG')
	bio.seek(0)
	await message.message.answer_document(bio)
	await listOfClients[id].info_id.delete()
	listOfClients.pop(id)

@dp.callback_query_handler(text="doneDeny")
async def from_f(message: CallbackQuery):
	global listOfClients
	id1 = message.message.chat.id
	id = client.find_client(listOfClients, message.message.chat.id)
	if id == -1: 
		await message.message.answer("Ваша сессия была завершена\nОтпраьте /start для начала работы")
		return
	await start_set(message.message)
#---------------------------------------------------------------------------------------------------
async def colorDialog(message, id):
	global listOfClients
	
	big_button_1: InlineKeyboardButton = InlineKeyboardButton(
		text='Синий', callback_data='blue')

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
		await message.message.answer("Ваша сессия была завершена\nОтпраьте /start для начала работы")
		return
	await done_accept(message.message)

#---------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text="bandage_dwnd")
async def from_f(message: CallbackQuery):
	global listOfClients
	id1 = message.message.chat.id
	id = client.find_client(listOfClients, message.message.chat.id)
	if id == -1: 
		await message.message.answer("Ваша сессия была завершена\nОтпраьте /start для начала работы")
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
		await message.answer("Ваша сессия была завершена\nОтпраьте /start для начала работы")
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
	
	

	# Создаем объект инлайн-клавиатуры
	keyboard3: InlineKeyboardMarkup = InlineKeyboardMarkup()
	keyboard3.row(up_btn,   first_layer_btn, bodyPart_btn, pass_btn)
	keyboard3.row(info_btn, overlay_btn,     pepetype_btn, reset_btn)
	keyboard3.row(down_btn, pose_btn,        negative_btn, bndg_downl)
	keyboard3.row(pass_btn, delete_btn,        bw_btn,       donw_btn)
	

	
	listOfClients[id].change_e = not listOfClients[id].change_e
	listOfClients[id].delete_mess = True
	txt11 = "Алекс" if listOfClients[id].slim else "Стив"
	txt1 = f"*Версия скина:* {txt11}\n"
	txt2 = f"*Позиция повязки:* {listOfClients[id].pos}\n"
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
			f"*Параметры:*\n{txt1}{txt2}{txt3}{txt4}{txt5}{txt6}{txt7}{txt8}",
			reply_markup=keyboard3, parse_mode='Markdown')

	except:pass

#---------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text="reset")
async def from_f(message: CallbackQuery):

	id1 = message.message.chat.id
	global listOfClients
	id = client.find_client(listOfClients, message.message.chat.id)
	if id == -1: 
		await message.message.answer("Ваша сессия была завершена\nОтпраьте /start для начала работы")
		return

	await reset_accept(message.message)

#---------------------------------------------------------------------------------------------------
@dp.callback_query_handler(text="up")
async def from_f(message: CallbackQuery):

	id1 = message.message.chat.id
	global listOfClients
	id = client.find_client(listOfClients, message.message.chat.id)
	if id == -1: 
		await message.message.answer("Ваша сессия была завершена\nОтпраьте /start для начала работы")
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
		await message.message.answer("Ваша сессия была завершена\nОтпраьте /start для начала работы")
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
		await message.message.answer("Ваша сессия была завершена\nОтпраьте /start для начала работы")
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
		await message.message.answer("Ваша сессия была завершена\nОтпраьте /start для начала работы")
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
		await message.message.answer("Ваша сессия была завершена\nОтпраьте /start для начала работы")
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
		await message.message.answer("Ваша сессия была завершена\nОтпраьте /start для начала работы")
		return
	if listOfClients[id].pos < 7:
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
		await message.message.answer("Ваша сессия была завершена\nОтпраьте /start для начала работы")
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
		await message.message.answer("Ваша сессия была завершена\nОтпраьте /start для начала работы")
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
		await message.message.answer("Ваша сессия была завершена\nОтпраьте /start для начала работы")
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
		await message.message.answer("Ваша сессия была завершена\nОтпраьте /start для начала работы")
		return
	listOfClients[id].pepe_type += 1

	if listOfClients[id].pepe_type > len(listOfClients[id].pepes) - 1: listOfClients[id].pepe_type = 0

	await render_and_edit(message.message, id, id1)
	await start_set(message.message)
#---------------------------------------------------------------------------------------------------
@dp.message_handler(content_types=['text'])
async def echo(message: types.Message):
	global listOfClients
	id = client.find_client(listOfClients, message.chat.id)
	if id == -1: 
		await message.answer("Ваша сессия была завершена\nОтпраьте /start для начала работы")
		return
	id1 = message.chat.id
	#if listOfClients[id].delete_mess: await message.delete()
	if listOfClients[id].wait_to_file == 2:
		done = await listOfClients[id].init_mc_n(message.text)
		if done == 1 or done == 3:
			if done == 3: await message.answer("У вашего скина непрозрачный фон!\nПредпросмотр будет некорректным!")
			listOfClients[id].wait_to_file = 0

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

		elif done == 2: await message.answer("Извините, скины до версии 1.8 не поддерживаются(")
		

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
				text='Готово ✓', callback_data='done_c')

			big_button_5: InlineKeyboardButton = InlineKeyboardButton(
				text='Изменить цвет', callback_data='colD')

			# Создаем объект инлайн-клавиатуры
			keyboard1: InlineKeyboardMarkup = InlineKeyboardMarkup(
				inline_keyboard=[[big_button_4], [big_button_5]])
			msg = await listOfClients[id].info_id.edit_text("Готово?", reply_markup=keyboard1)
			listOfClients[id].info_id = msg

		except Exception as e:
			print(e)
			msg = await message.answer("Не удалось получить цвет(\nПопробуйте ещё раз")
			listOfClients[id].error_msg = msg


if on_server: keep_alive()
if __name__ == '__main__':
	started = True
	while started:
		try:
			executor.start_polling(dp, skip_updates=True)
			started = False
		except Exception:
			started = True
			print("An error has occurred, reboot in 10 seconds")
			time1.sleep(10)
			print("rebooting...")