import telebot
import config
import os
import sys
import logging
import asyncio
from datetime import datetime
import sqlite3
import itertools
import re
from datetime import datetime

from telebot import types
from keyboa import Button
from keyboa import Keyboa

user_data = {}

globalIDSubtypeClient = 0
globalIDSubtype = 0
globalIDProduct = 0

##ИНФА для добавления товара
globalPhoto = '0'
globaldescription = '0'
globalName = '0'
globalPrice = 0

##ИНФА текущего клиента
globalNameClient = "0"
globalPhoneClient = "0"
globalAdress = "0"

##АЙДИ текущего клиента
globalIDClient = 0

##Для редактирования
globalEditProductID = 0
globalCountEditProduct = 0
globalEditIndex = 0
##ID сообщения
globalMessengID = 0
#Удаляем?
globalDell = 0
#Ищим
globalsearch = '0'
#Все заказы Админ
globalAllZakaz = 0
globalAllZakazFIOID = 0
#Для редактирование товаров у админа
globalRedag = 0 
#Для удаления сообщения товара 
send_photo = 0

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
	con = sqlite3.connect('example.db')
	cur = con.cursor()
	cur.execute('SELECT * FROM Client WHERE user_id = ?;', (message.chat.id,))
	all_results = cur.fetchall()
	if len(all_results) == 0:		
		sti = open('sticker.webp', 'rb')
		bot.send_sticker(message.chat.id, sti)
		bot.send_message(message.chat.id, "Добро пожалувати, {0.first_name}!\nЯ - <b>{1.first_name}</b>, створений що б допомогти обрати спортивне харчування.".format(message.from_user, bot.get_me()), parse_mode='html')
		msg = bot.send_message(message.chat.id, "Введіть своє Прізвище Ім'я")
		bot.register_next_step_handler(msg, process_NameClient_step)

	else: bot.send_message(message.chat.id,'Ви зареєстровані')

@bot.message_handler(content_types=['photo'])
def photo(message):
	if message.chat.type == 'private':
		file_photo = bot.get_file(message.photo[-1].file_id)
		#bot.send_message(message.chat.id, file_photo)

		filename, file_extension = os.path.splitext(file_photo.file_path)
		#bot.send_message(message.chat.id, file_extension)

		downloaded_file_photo = bot.download_file(file_photo.file_path)

		src = 'Photos/' + message.photo[-1].file_id + file_extension#D:/Проекты/
		with open(src,'wb') as new_file:
			new_file.write(downloaded_file_photo)
			#bot.send_message(message.chat.id, src)
			global globalPhoto
			global globalRedag
			con = sqlite3.connect('example.db')
			cur = con.cursor()

			cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (message.chat.id,))
			idclient = cur.fetchall()

			StrA = " ".join([str(_) for _ in idclient])
			globalIDClien=re.sub("['|(|)|,]","",StrA)

			cur.execute("SELECT Client_ID_Product.globalRedag  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
			Redag = cur.fetchall()


			St = " ".join([str(_) for _ in Redag])
			Redag=re.sub("['|(|)|,]","",St)
			#global globalMessengID
			globalPhoto = src
			
			
			if int(Redag) == 1:
				Client=(globalIDClien)
				cur.execute("SELECT Client_ID_Product.ID_Product  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				#bot.send_message(call.message.chat.id,str(ke))

				St = " ".join([str(_) for _ in ke])
				ke=re.sub("['|(|)|,]","",St)
				id = int(ke)
				cur.execute("UPDATE Product SET Photo = ? WHERE ID_Product = ?",(globalPhoto, id))
				con.commit()

				TypeProduct=(ke)
				cur.execute("SELECT Product.Name_Product FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
				key2 = cur.fetchall()
				cur.execute("SELECT Product.Price  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
				key3 = cur.fetchall()
				cur.execute("SELECT Product.Photo  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
				key4 = cur.fetchall()
				cur.execute("SELECT Product.Description  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
				key6 = cur.fetchall()
				cur.execute("SELECT Product.Name_Product,Product.Price, Product.Photo  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
				key5 = cur.fetchall()

				#bot.send_message(call.message.chat.id, key5.format(n), parse_mode='Markdown')
				#``'Всего:\n{}'.
				StrA = " ".join([str(_) for _ in key2])
				s1=re.sub("['|(|)|,]","",StrA)

				StrB = " ".join([str(_) for _ in key3])
				s2=re.sub("['|(|)|,]","",StrB)

				StrV = " ".join([str(_) for _ in key6])
				s3=re.sub("['|(|)|,]","",StrV)

				StrC = " ".join([str(_) for _ in key4])
				s4=re.sub("['|(|)|,]","",StrC)
					#f'{text}\n{img}'
				markup3 = types.InlineKeyboardMarkup(row_width=5)
				lline3 = types.InlineKeyboardButton("Завершити", callback_data='back')
				lline4 = types.InlineKeyboardButton("Редагувати назву", callback_data='redakNameProduct')
				lline7 = types.InlineKeyboardButton("Редагувати ціну", callback_data='redakPriceProduct')
				lline8 = types.InlineKeyboardButton("Редагувати опис", callback_data='redakDescProduct')
				lline9 = types.InlineKeyboardButton("Редагувати зображення", callback_data='redakPhotoProduct')

				markup3.add(lline4,lline7)
				markup3.add(lline8,lline9)
				markup3.add(lline3)

				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()

				globalMessengID = bot.send_photo(message.chat.id, open(s4, 'rb'), caption= s1 +"\nЦіна: "+ s2 + "\nОпис: "+s3, parse_mode='Markdown', reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(globalIDClien,))
				con.commit()

			else:
				bot.send_message(message.chat.id, "Зображення додано!")
				markup3 = types.InlineKeyboardMarkup(row_width=4)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline3 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline4 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)

				# remove inline buttons
				cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				ke=re.sub("['|(|)|,]","",St)
				bot.delete_message(message.chat.id, ke)
				globalMessengID = bot.send_message(message.chat.id, "Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(globalIDClien,))
				con.commit()

def FioCorrectly(message):
	copyText = message.text
	
	copyText = message.text.split(" ")
	
	if len(copyText) == 1:
		return 0
	for i in range(len(copyText)):
		if copyText[i].isalpha() == False:
			return 0
	return 1

def AdressCorrectly(message):
	copyText = message.text
	if copyText.isdigit() == True:
		return 0
	if copyText.isalpha() == True:
		return 0
	return 1

def NumberCorrectly(message):
	copyText = message.text
	if len(copyText) == 10:
		if copyText.isdigit() == True:
			return 1
	return 0

def NameProductCorrectly(message):
	copyText = message.text
	if len(copyText) < 3:
		return 0
	if copyText.isdigit() == True:
		return 0
	return 1

def PriceProductCorrectly(message):
	copyText = message.text
	if len(copyText) > 0:
		if copyText.isdigit() == True:
			return 1
	return 0

def DescriptionProductCorrectly(message):
	copyText = message.text
	if len(copyText) < 3:
		return 0
	if copyText.isdigit() == True:
		return 0
	return 1

def process_NameClient_step(message):
	try:
		correctly = FioCorrectly(message)
		if correctly == 0:
			msg =bot.send_message(message.chat.id, "Не коректні дані, спробуйте ще")
			bot.register_next_step_handler(msg, process_NameClient_step)
		else:
			user_id = message.from_user.id
			user_data[user_id] = message.text
			global globalNameClient
			globalNameClient = message.text

			bot.send_message(user_id, "Вас звуть "+ globalNameClient)
			msg1 = bot.send_message(message.chat.id, "Введіть свій Номер Телефону у форматі:\n+38(***)*******")

			bot.register_next_step_handler(msg1, process_Number_Phone_step)
			
	except Exception as e:
		bot.reply_to(message, 'oooops')

def process_Number_Phone_step(message):
	try:
		correctly = NumberCorrectly(message)
		if correctly == 0:
			msg = bot.send_message(message.chat.id, "Не коректні дані, спробуйте ще")
			bot.register_next_step_handler(msg, process_Number_Phone_step)

		else:
			user_id = message.from_user.id
			user_data[user_id] = message.text
			global globalPhoneClient
			globalPhoneClient = message.text
			bot.send_message(user_id, "Ваш номер телефону "+ globalPhoneClient)

			msg2 = bot.send_message(message.chat.id, "Введіть свою Адресу")
			bot.register_next_step_handler(msg2, process_Address_step)
			#bot.send_message(user_id, "Введенна назва товару "+ message.text)
	except Exception as e:
		bot.reply_to(message, 'oooops')

def process_Address_step(message):
		correctly = AdressCorrectly(message)
		if correctly == 0:
			msg = bot.send_message(message.chat.id, "Не коректні дані, спробуйте ще")
			bot.register_next_step_handler(msg, process_Address_step)

		else:
			user_id = message.from_user.id
			user_data[user_id] = message.text
			global globalAdress
			globalAdress = message.text
			bot.send_message(user_id, "Ваша адреса "+ globalAdress)

			con = sqlite3.connect('example.db')
			cur = con.cursor()
			user=(message.chat.id, globalNameClient, globalPhoneClient, globalAdress)
			cur.execute("INSERT INTO Client (user_id, FIO, Number_Phone, Address) Values (?,?,?,?);", user)
			con.commit()

			cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (message.chat.id,))
			idclient = cur.fetchall()

			#bot.send_message(user_id, idclient)
			global globalIDClient
			StrA = " ".join([str(_) for _ in idclient])
			globalIDClient=re.sub("['|(|)|,]","",StrA)
			
			id = int(globalIDClient)
			order=(id, 0, "2021-05-02")
			cur.execute("INSERT INTO [Order] (ID_Client, Status, Date_Order) Values (?,?,?);", order)
			con.commit()

			order2=(0,id,0,0,0,0,0,0,0,0,0)
			cur.execute("INSERT INTO Client_ID_Product (ID_Product ,ID_Client, send_photo, globalMessengID, globalEditIndex, globalCountEditProduct, globalEditProductID,globalDell,globalsearch,globalAllZakaz,globalRedag) Values (?,?,?,?,?,?,?,?,?,?,?);", order2)
			con.commit()
			#keyboard
			markup = types.ReplyKeyboardMarkup()
			item1 = types.KeyboardButton("📗Каталог")
			item2 = types.KeyboardButton("🛒Kошик")
			item3 = types.KeyboardButton("🔍Пошук")
			item4 = types.KeyboardButton("📜Замовлення")
			item5 = types.KeyboardButton("❓Інформація")
			item6 = types.KeyboardButton("📱Контакти")
			item7 = types.KeyboardButton("🤵‍Особистий кабінет")
			markup.row(item1, item2)
			markup.row(item3, item4)
			markup.row(item5, item6)
			markup.row(item7)
			bot.send_message(user_id, "Можете користуватися мною, дякую ☺", reply_markup=markup)

def process_EditFIO_step(message):###Редактирование ФИО
	try:

		correctly = FioCorrectly(message)
		if correctly == 0:
			msg =bot.send_message(message.chat.id, "Не коректні дані, спробуйте ще")
			bot.register_next_step_handler(msg, process_EditFIO_step)

		else:
			con = sqlite3.connect('example.db')
			cur = con.cursor()

			s2 = message.text
			name = str.capitalize(s2)

			cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (message.chat.id,))
			idclient = cur.fetchall()
			StrA = " ".join([str(_) for _ in idclient])
			globalIDClien=re.sub("['|(|)|,]","",StrA)
			id = int(globalIDClien)
			
			cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
			ke = cur.fetchall()
			St = " ".join([str(_) for _ in ke])
			send_photo=re.sub("['|(|)|,]","",St)
			if int(send_photo) == 1:
				cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				ke=re.sub("['|(|)|,]","",St)
				bot.delete_message(message.chat.id, ke)
				cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
				con.commit()

			cur.execute("UPDATE Client SET FIO = ? WHERE ID_Client = ?",(message.text, id))
			#cur.execute(sql)
			con.commit()
			

			cur.execute('SELECT Client.FIO FROM Client WHERE Client.ID_Client = ?;', (id,))
			fioclient = cur.fetchall()
			StrA = " ".join([str(_) for _ in fioclient])
			fioclient=re.sub("['|(|)|,]","",StrA)


			cur.execute('SELECT Client.Address FROM Client WHERE Client.ID_Client = ?;', (id,))
			Address = cur.fetchall()
			StrA = " ".join([str(_) for _ in Address])
			Address=re.sub("['|(|)|,]","",StrA)


			cur.execute('SELECT Client.Number_Phone FROM Client WHERE Client.ID_Client = ?;', (id,))
			Number_Phone = cur.fetchall()
			StrA = " ".join([str(_) for _ in Number_Phone])
			Number_Phone=re.sub("['|(|)|,]","",StrA)


			markup2 = types.InlineKeyboardMarkup(row_width=3)

			line1 = types.InlineKeyboardButton("Прізвище Ім'я", callback_data='fio')
			line2 = types.InlineKeyboardButton("Адреса", callback_data='address')
			line3 = types.InlineKeyboardButton("Номер телефону", callback_data='numberPhone')

			markup2.add(line1, line2, line3)

			globalMessengID=bot.send_message(message.chat.id, "Ваші дані:\nПрізвище Ім'я: "+fioclient+"\nАдреса: "+Address+"\nНомер телефону: "+Number_Phone+'\nОберіть що змінити, якщо треба:', reply_markup=markup2)#выводим доп кнопки
			cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
			con.commit()
			cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
			con.commit()
			
	except Exception as e:
		bot.reply_to(message, 'Помилка')

def process_EditAdress_step(message):###Редактирование Адресса
	try:
		correctly = AdressCorrectly(message)
		if correctly == 0:
			msg = bot.send_message(message.chat.id, "Не коректні дані, спробуйте ще")
			bot.register_next_step_handler(msg, process_EditAdress_step)

		else:
			con = sqlite3.connect('example.db')
			cur = con.cursor()
			s2 = message.text
			name = str.capitalize(s2)

			cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (message.chat.id,))
			idclient = cur.fetchall()
			StrA = " ".join([str(_) for _ in idclient])
			globalIDClien=re.sub("['|(|)|,]","",StrA)
			id = int(globalIDClien)
			
			cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
			ke = cur.fetchall()
			St = " ".join([str(_) for _ in ke])
			send_photo=re.sub("['|(|)|,]","",St)
			if int(send_photo) == 1:
				cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				ke=re.sub("['|(|)|,]","",St)
				bot.delete_message(message.chat.id, ke)
				cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
				con.commit()

			cur.execute("UPDATE Client SET Address = ? WHERE ID_Client = ?",(message.text, id))
			#cur.execute(sql)
			con.commit()

			cur.execute('SELECT Client.FIO FROM Client WHERE Client.ID_Client = ?;', (id,))
			fioclient = cur.fetchall()
			StrA = " ".join([str(_) for _ in fioclient])
			fioclient=re.sub("['|(|)|,]","",StrA)

			cur.execute('SELECT Client.Address FROM Client WHERE Client.ID_Client = ?;', (id,))
			Address = cur.fetchall()
			StrA = " ".join([str(_) for _ in Address])
			Address=re.sub("['|(|)|,]","",StrA)

			cur.execute('SELECT Client.Number_Phone FROM Client WHERE Client.ID_Client = ?;', (id,))
			Number_Phone = cur.fetchall()
			StrA = " ".join([str(_) for _ in Number_Phone])
			Number_Phone=re.sub("['|(|)|,]","",StrA)

			markup2 = types.InlineKeyboardMarkup(row_width=3)

			line1 = types.InlineKeyboardButton("Прізвище Ім'я", callback_data='fio')
			line2 = types.InlineKeyboardButton("Адреса", callback_data='address')
			line3 = types.InlineKeyboardButton("Номер телефону", callback_data='numberPhone')

			markup2.add(line1, line2, line3)
	
			globalMessengID=bot.send_message(message.chat.id, "Ваші дані:\nПрізвище Ім'я: "+fioclient+"\nАдреса: "+Address+"\nНомер телефону: "+Number_Phone+'\nОберіть що змінити, якщо треба:', reply_markup=markup2)#выводим доп кнопки
			cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
			con.commit()
			cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
			con.commit()
	except Exception as e:
		bot.reply_to(message, 'Помилка')

def process_EditNumber_step(message):###Редактирование Номера телефона
	try:
		correctly = NumberCorrectly(message)
		if correctly == 0:
			msg = bot.send_message(message.chat.id, "Не коректні дані, спробуйте ще")
			bot.register_next_step_handler(msg, process_EditNumber_step)
		else:
			con = sqlite3.connect('example.db')
			cur = con.cursor()
			s2 = message.text
			name = str.capitalize(s2)

			cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (message.chat.id,))
			idclient = cur.fetchall()
			StrA = " ".join([str(_) for _ in idclient])
			globalIDClien=re.sub("['|(|)|,]","",StrA)
			id = int(globalIDClien)
			
			cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
			ke = cur.fetchall()
			St = " ".join([str(_) for _ in ke])
			send_photo=re.sub("['|(|)|,]","",St)
			if int(send_photo) == 1:
				cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				ke=re.sub("['|(|)|,]","",St)
				bot.delete_message(message.chat.id, ke)
				cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
				con.commit()

			cur.execute("UPDATE Client SET Number_Phone = ? WHERE ID_Client = ?",(message.text, id))
			#cur.execute(sql)
			con.commit()

			cur.execute('SELECT Client.FIO FROM Client WHERE Client.ID_Client = ?;', (id,))
			fioclient = cur.fetchall()
			StrA = " ".join([str(_) for _ in fioclient])
			fioclient=re.sub("['|(|)|,]","",StrA)

			cur.execute('SELECT Client.Address FROM Client WHERE Client.ID_Client = ?;', (id,))
			Address = cur.fetchall()
			StrA = " ".join([str(_) for _ in Address])
			Address=re.sub("['|(|)|,]","",StrA)

			cur.execute('SELECT Client.Number_Phone FROM Client WHERE Client.ID_Client = ?;', (id,))
			Number_Phone = cur.fetchall()
			StrA = " ".join([str(_) for _ in Number_Phone])
			Number_Phone=re.sub("['|(|)|,]","",StrA)

			markup2 = types.InlineKeyboardMarkup(row_width=3)

			line1 = types.InlineKeyboardButton("Прізвище Ім'я", callback_data='fio')
			line2 = types.InlineKeyboardButton("Адреса", callback_data='address')
			line3 = types.InlineKeyboardButton("Номер телефону", callback_data='numberPhone')

			markup2.add(line1, line2, line3)

			globalMessengID=bot.send_message(message.chat.id, "Ваші дані:\nПрізвище Ім'я: "+fioclient+"\nАдреса: "+Address+"\nНомер телефону: "+Number_Phone+'\nОберіть що змінити, якщо треба:', reply_markup=markup2)#выводим доп кнопки
			cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
			con.commit()
			cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
			con.commit()
	except Exception as e:
		bot.reply_to(message, 'Помилка')

def process_NameProduct_step(message):
	correctly = NameProductCorrectly(message)
	if correctly == 0:
		msg = bot.send_message(message.chat.id, "Не коректні дані, спробуйте ще")
		bot.register_next_step_handler(msg, process_NameProduct_step)
	else:
		global NameProduct
		NameProduct = message.text
		con = sqlite3.connect('example.db')
		cur = con.cursor()
		cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (message.chat.id,))
		idclient = cur.fetchall()
		cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (message.chat.id,))
		idclient = cur.fetchall()
		StrA = " ".join([str(_) for _ in idclient])
		globalIDClien=re.sub("['|(|)|,]","",StrA)
		id = int(globalIDClien)
		
		cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
		ke = cur.fetchall()
		St = " ".join([str(_) for _ in ke])
		send_photo=re.sub("['|(|)|,]","",St)
		if int(send_photo) == 1:
			cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
			ke = cur.fetchall()
			St = " ".join([str(_) for _ in ke])
			ke=re.sub("['|(|)|,]","",St)
			bot.delete_message(message.chat.id, ke)
			cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
			con.commit()
		StrA = " ".join([str(_) for _ in idclient])
		globalIDClien=re.sub("['|(|)|,]","",StrA)
		cur.execute("SELECT Client_ID_Product.ID_Product  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
		ke = cur.fetchall()
		#bot.send_message(call.message.chat.id,str(ke))

		St = " ".join([str(_) for _ in ke])
		ke=re.sub("['|(|)|,]","",St)
		id = int(ke)
		cur.execute("UPDATE Product SET Name_Product = ? WHERE ID_Product = ?",(message.text, id))
		con.commit()

		TypeProduct=(ke)
		cur.execute("SELECT Product.Name_Product FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
		key2 = cur.fetchall()
		cur.execute("SELECT Product.Price  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
		key3 = cur.fetchall()
		cur.execute("SELECT Product.Photo  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
		key4 = cur.fetchall()
		cur.execute("SELECT Product.Description  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
		key6 = cur.fetchall()
		cur.execute("SELECT Product.Name_Product,Product.Price, Product.Photo  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
		key5 = cur.fetchall()

		#bot.send_message(call.message.chat.id, key5.format(n), parse_mode='Markdown')
		#``'Всего:\n{}'.
		StrA = " ".join([str(_) for _ in key2])
		s1=re.sub("['|(|)|,]","",StrA)

		StrB = " ".join([str(_) for _ in key3])
		s2=re.sub("['|(|)|,]","",StrB)

		StrV = " ".join([str(_) for _ in key6])
		s3=re.sub("['|(|)|,]","",StrV)

		StrC = " ".join([str(_) for _ in key4])
		s4=re.sub("['|(|)|,]","",StrC)
			#f'{text}\n{img}'
		markup3 = types.InlineKeyboardMarkup(row_width=5)
		lline3 = types.InlineKeyboardButton("Завершити", callback_data='back')
		lline4 = types.InlineKeyboardButton("Редагувати назву", callback_data='redakNameProduct')
		lline7 = types.InlineKeyboardButton("Редагувати ціну", callback_data='redakPriceProduct')
		lline8 = types.InlineKeyboardButton("Редагувати опис", callback_data='redakDescProduct')
		lline9 = types.InlineKeyboardButton("Редагувати зображення", callback_data='redakPhotoProduct')

		markup3.add(lline4,lline7)
		markup3.add(lline8,lline9)
		markup3.add(lline3)

		globalMessengID = bot.send_photo(message.chat.id, open(s4, 'rb'), caption= s1 +"\nЦіна: "+ s2 + "\nОпис: "+s3, parse_mode='Markdown', reply_markup=markup3)
		cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, globalIDClien))
		con.commit()
		cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(globalIDClien,))
		con.commit()


def process_PriceProduct_step(message):

	correctly = PriceProductCorrectly(message)
	if correctly == 0:
		msg = bot.send_message(message.chat.id, "Не коректні дані, спробуйте ще")
		bot.register_next_step_handler(msg, process_PriceProduct_step)
	else:
		global PriceProduct
		PriceProduct = message.text
		con = sqlite3.connect('example.db')
		cur = con.cursor()
		cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (message.chat.id,))
		idclient = cur.fetchall()
		cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (message.chat.id,))
		idclient = cur.fetchall()
		StrA = " ".join([str(_) for _ in idclient])
		globalIDClien=re.sub("['|(|)|,]","",StrA)
		id = int(globalIDClien)
		
		cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
		ke = cur.fetchall()
		St = " ".join([str(_) for _ in ke])
		send_photo=re.sub("['|(|)|,]","",St)
		if int(send_photo) == 1:
			cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
			ke = cur.fetchall()
			St = " ".join([str(_) for _ in ke])
			ke=re.sub("['|(|)|,]","",St)
			bot.delete_message(message.chat.id, ke)
			cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
			con.commit()
		StrA = " ".join([str(_) for _ in idclient])
		globalIDClien=re.sub("['|(|)|,]","",StrA)
		cur.execute("SELECT Client_ID_Product.ID_Product  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
		ke = cur.fetchall()
		#bot.send_message(call.message.chat.id,str(ke))

		St = " ".join([str(_) for _ in ke])
		ke=re.sub("['|(|)|,]","",St)
		id = int(ke)
		cur.execute("UPDATE Product SET Price = ? WHERE ID_Product = ?",(message.text, id))
		con.commit()

		TypeProduct=(ke)
		cur.execute("SELECT Product.Name_Product FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
		key2 = cur.fetchall()
		cur.execute("SELECT Product.Price  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
		key3 = cur.fetchall()
		cur.execute("SELECT Product.Photo  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
		key4 = cur.fetchall()
		cur.execute("SELECT Product.Description  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
		key6 = cur.fetchall()
		cur.execute("SELECT Product.Name_Product,Product.Price, Product.Photo  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
		key5 = cur.fetchall()

		#bot.send_message(call.message.chat.id, key5.format(n), parse_mode='Markdown')
		#``'Всего:\n{}'.
		StrA = " ".join([str(_) for _ in key2])
		s1=re.sub("['|(|)|,]","",StrA)

		StrB = " ".join([str(_) for _ in key3])
		s2=re.sub("['|(|)|,]","",StrB)

		StrV = " ".join([str(_) for _ in key6])
		s3=re.sub("['|(|)|,]","",StrV)

		StrC = " ".join([str(_) for _ in key4])
		s4=re.sub("['|(|)|,]","",StrC)
			#f'{text}\n{img}'
		markup3 = types.InlineKeyboardMarkup(row_width=5)
		lline3 = types.InlineKeyboardButton("Завершити", callback_data='back')
		lline4 = types.InlineKeyboardButton("Редагувати назву", callback_data='redakNameProduct')
		lline7 = types.InlineKeyboardButton("Редагувати ціну", callback_data='redakPriceProduct')
		lline8 = types.InlineKeyboardButton("Редагувати опис", callback_data='redakDescProduct')
		lline9 = types.InlineKeyboardButton("Редагувати зображення", callback_data='redakPhotoProduct')

		markup3.add(lline4,lline7)
		markup3.add(lline8,lline9)
		markup3.add(lline3)

		globalMessengID=bot.send_photo(message.chat.id, open(s4, 'rb'), caption= s1 +"\nЦіна: "+ s2 + "\nОпис: "+s3, parse_mode='Markdown', reply_markup=markup3)
		cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, globalIDClien))
		con.commit()
		cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(globalIDClien,))
		con.commit()


def process_DescProduct_step(message):
	correctly = DescriptionProductCorrectly(message)
	if correctly == 0:
		msg = bot.send_message(message.chat.id, "Не коректні дані, спробуйте ще")
		bot.register_next_step_handler(msg, process_DescProduct_step)
	else:
		global DescProduct
		DescProduct = message.text
		con = sqlite3.connect('example.db')
		cur = con.cursor()
		cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (message.chat.id,))
		idclient = cur.fetchall()
		cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (message.chat.id,))
		idclient = cur.fetchall()
		StrA = " ".join([str(_) for _ in idclient])
		globalIDClien=re.sub("['|(|)|,]","",StrA)
		id = int(globalIDClien)
		
		cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
		ke = cur.fetchall()
		St = " ".join([str(_) for _ in ke])
		send_photo=re.sub("['|(|)|,]","",St)
		if int(send_photo) == 1:
			cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
			ke = cur.fetchall()
			St = " ".join([str(_) for _ in ke])
			ke=re.sub("['|(|)|,]","",St)
			bot.delete_message(message.chat.id, ke)
			cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
			con.commit()
		StrA = " ".join([str(_) for _ in idclient])
		globalIDClien=re.sub("['|(|)|,]","",StrA)
		cur.execute("SELECT Client_ID_Product.ID_Product  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
		ke = cur.fetchall()
		#bot.send_message(call.message.chat.id,str(ke))

		St = " ".join([str(_) for _ in ke])
		ke=re.sub("['|(|)|,]","",St)
		id = int(ke)
		cur.execute("UPDATE Product SET Description = ? WHERE ID_Product = ?",(message.text, id))
		con.commit()

		TypeProduct=(ke)
		cur.execute("SELECT Product.Name_Product FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
		key2 = cur.fetchall()
		cur.execute("SELECT Product.Price  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
		key3 = cur.fetchall()
		cur.execute("SELECT Product.Photo  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
		key4 = cur.fetchall()
		cur.execute("SELECT Product.Description  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
		key6 = cur.fetchall()
		cur.execute("SELECT Product.Name_Product,Product.Price, Product.Photo  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
		key5 = cur.fetchall()

		#bot.send_message(call.message.chat.id, key5.format(n), parse_mode='Markdown')
		#``'Всего:\n{}'.
		StrA = " ".join([str(_) for _ in key2])
		s1=re.sub("['|(|)|,]","",StrA)

		StrB = " ".join([str(_) for _ in key3])
		s2=re.sub("['|(|)|,]","",StrB)

		StrV = " ".join([str(_) for _ in key6])
		s3=re.sub("['|(|)|,]","",StrV)

		StrC = " ".join([str(_) for _ in key4])
		s4=re.sub("['|(|)|,]","",StrC)
			#f'{text}\n{img}'
		markup3 = types.InlineKeyboardMarkup(row_width=5)
		lline3 = types.InlineKeyboardButton("Завершити", callback_data='back')
		lline4 = types.InlineKeyboardButton("Редагувати назву", callback_data='redakNameProduct')
		lline7 = types.InlineKeyboardButton("Редагувати ціну", callback_data='redakPriceProduct')
		lline8 = types.InlineKeyboardButton("Редагувати опис", callback_data='redakDescProduct')
		lline9 = types.InlineKeyboardButton("Редагувати зображення", callback_data='redakPhotoProduct')

		markup3.add(lline4,lline7)
		markup3.add(lline8,lline9)
		markup3.add(lline3)

		globalMessengID=bot.send_photo(message.chat.id, open(s4, 'rb'), caption= s1 +"\nЦіна: "+ s2 + "\nОпис: "+s3, parse_mode='Markdown', reply_markup=markup3)
		cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, globalIDClien))
		con.commit()
		cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(globalIDClien,))
		con.commit()


def process_name_step(message):
	try:
		correctly = NameProductCorrectly(message)
		if correctly == 0:
			msg = bot.send_message(message.chat.id, "Не коректні дані, спробуйте ще")
			bot.register_next_step_handler(msg, process_name_step)
		else:

			user_id = message.from_user.id
			user_data[user_id] = message.text
			global globalName
			globalName = message.text
			bot.send_message(user_id, "Введенна назва товару "+ globalName)
			#bot.send_message(user_id, "Введенна назва товару "+ message.text)
	except Exception as e:
		bot.reply_to(message, 'oooops')

def process_price_step(message):
	correctly = PriceProductCorrectly(message)
	if correctly == 0:
		msg = bot.send_message(message.chat.id, "Не коректні дані, спробуйте ще")
		bot.register_next_step_handler(msg, process_price_step)
	else:
		user_id = message.from_user.id
		user_data[user_id] = message.text
		global globalPrice
		globalPrice = message.text
		bot.send_message(user_id, "Введенна ціна товару "+ globalPrice)
		#bot.send_message(user_id, "Введенна ціна товару "+ int(message.text))

def process_description_step(message):
	try:
		correctly = DescriptionProductCorrectly(message)
		if correctly == 0:
			msg = bot.send_message(message.chat.id, "Не коректні дані, спробуйте ще")
			bot.register_next_step_handler(msg, process_description_step)
		else:
			user_id = message.from_user.id
			user_data[user_id] = message.text
			global globaldescription
			globaldescription = message.text
			bot.send_message(user_id, "Введенний опис товару "+ globaldescription)
			#bot.send_message(user_id, "Введенний опис товару "+ message.text)
	except Exception as e:
		bot.reply_to(message, 'oooops')

def process_search1_step(message):
	try:
		global globalsearch
		global globalsearchName
		global globalMessengID
		globalsearch = 1
		user_id = message.from_user.id
		user_data[user_id] = message.text
		globalsearchName = message.text
		#global globalNameClient
		name = message.text
		
		con = sqlite3.connect('example.db')
		cur = con.cursor() 
		
		
		cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (message.chat.id,))
		idclient = cur.fetchall()
		StrA = " ".join([str(_) for _ in idclient])
		globalIDClien=re.sub("['|(|)|,]","",StrA)
		
		#cur.execute("UPDATE Client_ID_Product SET globalsearch = ? WHERE ID_Client = ?",('1', globalIDClien))
		#con.commit()

		cur.execute('SELECT Product.Name_Product, Product.ID_Product FROM Product Where Product.Status = 1 and Product.Name_Product LIKE ? ORDER BY Product.Name_Product;', ('%{}%'.format(name),))
		key1 = cur.fetchall()
		cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (message.chat.id,))
		idclient = cur.fetchall()

		StrA = " ".join([str(_) for _ in idclient])
		globalIDClien=re.sub("['|(|)|,]","",StrA)
		kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
		globalMessengID = bot.send_message(chat_id=message.chat.id, reply_markup=kb_product, text="Оберіть товар:")
		cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, globalIDClien,))
		con.commit()
		
	except Exception as e:
		bot.reply_to(message, 'Нічього не знайдено')

def process_search2_step(message):
	try:
		global globalsearch
		global globalsearchName
		global globalMessengID
		globalsearch = 2
		globalsearchName = message.text
		user_id = message.from_user.id
		user_data[user_id] = message.text
		#global globalNameClient
		s2 = message.text
		name = str.capitalize(s2)
		con = sqlite3.connect('example.db')
		cur = con.cursor() 
		
		
		cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (message.chat.id,))
		idclient = cur.fetchall()
		StrA = " ".join([str(_) for _ in idclient])
		globalIDClien=re.sub("['|(|)|,]","",StrA)
		
		#cur.execute("UPDATE Client_ID_Product SET globalsearch = ? WHERE ID_Client = ?",('2', globalIDClien))
		#con.commit()

		cur.execute('SELECT Product.Name_Product, Product.ID_Product FROM Product, Type_product, Subtype_product Where Product.Status = 1 and Product.ID_Subtype = Subtype_product.ID_Subtype and Subtype_product.ID_Type = Type_product.ID_Type and Type_product.Name_Type LIKE ? ORDER BY Product.Name_Product;', ('%{}%'.format(name),))
		key1 = cur.fetchall()
		cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (message.chat.id,))
		idclient = cur.fetchall()

		StrA = " ".join([str(_) for _ in idclient])
		globalIDClien=re.sub("['|(|)|,]","",StrA)
		kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
		globalMessengID = bot.send_message(chat_id=message.chat.id, reply_markup=kb_product, text="Оберіть товар:")
		cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, globalIDClien,))
		con.commit()
		
	except Exception as e:
		bot.reply_to(message, 'Нічього не знайдено')

def process_searchFIO_step(message):
	try:
		con = sqlite3.connect('example.db')
		cur = con.cursor()
		s2 = message.text
		name = str.capitalize(s2)
		cur.execute('SELECT Client.FIO, Client.ID_Client FROM Client Where Client.FIO LIKE ? ORDER BY Client.FIO;', ('%{}%'.format(name),))
	
		key1 = cur.fetchall()

		kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
		bot.send_message(chat_id=message.chat.id, reply_markup=kb_product, text="Усі клієнти що робили замовлення\nОберіть клиента:")
	except Exception as e:
		bot.reply_to(message, 'Нічього не знайдено')

def validate(date_text):
	try:
		if date_text != datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d'):
			raise ValueError
		return True
	except ValueError:
		return False

@bot.message_handler(content_types=['text'])

def KeyboardInline(message):
	if message.chat.type == 'private':
		global globalIDClient
		global globalDell
		global globalsearch
		global globalAllZakaz
		global globalRedag
		global send_photo

		if message.text == '🤵‍Особистий кабінет':
			con = sqlite3.connect('example.db')
			cur = con.cursor() 
			cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (message.chat.id,))
			idclient = cur.fetchall()
			StrA = " ".join([str(_) for _ in idclient])
			globalIDClien=re.sub("['|(|)|,]","",StrA)
			id = int(globalIDClien)

			cur.execute('SELECT Client.FIO FROM Client WHERE Client.ID_Client = ?;', (id,))
			fioclient = cur.fetchall()
			StrA = " ".join([str(_) for _ in fioclient])
			fioclient=re.sub("['|(|)|,]","",StrA)

			cur.execute('SELECT Client.Address FROM Client WHERE Client.ID_Client = ?;', (id,))
			Address = cur.fetchall()
			StrA = " ".join([str(_) for _ in Address])
			Address=re.sub("['|(|)|,]","",StrA)

			cur.execute('SELECT Client.Number_Phone FROM Client WHERE Client.ID_Client = ?;', (id,))
			Number_Phone = cur.fetchall()
			StrA = " ".join([str(_) for _ in Number_Phone])
			Number_Phone=re.sub("['|(|)|,]","",StrA)

			markup2 = types.InlineKeyboardMarkup(row_width=3)

			line1 = types.InlineKeyboardButton("Прізвище Ім'я", callback_data='fio')
			line2 = types.InlineKeyboardButton("Адреса", callback_data='address')
			line3 = types.InlineKeyboardButton("Номер телефону", callback_data='numberPhone')

			markup2.add(line1, line2, line3)

			globalMessengID=bot.send_message(message.chat.id, "Ваші дані:\nПрізвище Ім'я: "+fioclient+"\nАдреса: "+Address+"\nНомер телефону: "+Number_Phone+'\nОберіть що змінити, якщо треба:', reply_markup=markup2)#выводим доп кнопки
			cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
			con.commit()
			cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
			con.commit()

		elif message.text == '📗Каталог':#пункт меню
			globalDell = 0
			globalsearch = 0
			globalAllZakaz = 0
			globalRedag = 0
			markup2 = types.InlineKeyboardMarkup(row_width=8)

			line1 = types.InlineKeyboardButton("Протеїн", callback_data='prot')
			line2 = types.InlineKeyboardButton("BCA", callback_data='bca')
			line3 = types.InlineKeyboardButton("Гейнер", callback_data='geaner')
			line4 = types.InlineKeyboardButton("Амінокислоти", callback_data='ami')
			line5 = types.InlineKeyboardButton("Креатин", callback_data='kreat')
			line6 = types.InlineKeyboardButton("L-Карнетин", callback_data='l_kor')
			line7 = types.InlineKeyboardButton("Жироспалювачі", callback_data='jir')
			line8 = types.InlineKeyboardButton("Вітаміни-Мінерали", callback_data='vit')

			markup2.add(line1, line2)
			markup2.add(line3, line4)
			markup2.add(line5, line6)
			markup2.add(line7, line8)
			#bot.delete_message(message.chat.id, message.message_id-1)
			con = sqlite3.connect('example.db')
			cur = con.cursor() 
			
			
			cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (message.chat.id,))
			idclient = cur.fetchall()
			StrA = " ".join([str(_) for _ in idclient])
			globalIDClien=re.sub("['|(|)|,]","",StrA)
			cur.execute("UPDATE Client_ID_Product SET globalDell = ? WHERE ID_Client = ?",('0', globalIDClien))
			con.commit()
			cur.execute("UPDATE Client_ID_Product SET globalsearch = ? WHERE ID_Client = ?",('0', globalIDClien))
			con.commit()
			cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
			con.commit()
			cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
			con.commit()
			cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
			ke = cur.fetchall()
			St = " ".join([str(_) for _ in ke])
			send_photo=re.sub("['|(|)|,]","",St)
			if int(send_photo) == 1:
				cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				ke=re.sub("['|(|)|,]","",St)
				bot.delete_message(message.chat.id, ke)
				cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
				con.commit()


			bot.send_message(message.chat.id, 'Оберіть категорію товару:', reply_markup=markup2)#выводим доп кнопки

		elif message.text == '🛒Kошик':
			con = sqlite3.connect('example.db')
			cur = con.cursor()
			globalAllZakaz = 0 
			cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (message.chat.id,))
			idclient = cur.fetchall()
			StrA = " ".join([str(_) for _ in idclient])
			globalIDClien=re.sub("['|(|)|,]","",StrA)
			id = int(globalIDClien)
	
			cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
			con.commit()
		
			
			cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
			ke = cur.fetchall()
			St = " ".join([str(_) for _ in ke])
			send_photo=re.sub("['|(|)|,]","",St)
			if int(send_photo) == 1:
				cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				ke=re.sub("['|(|)|,]","",St)
				bot.delete_message(message.chat.id, ke)
				cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
				con.commit()

			cur.execute("SELECT Product.Name_Product FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 0 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ?;", (id,))
			tovar = cur.fetchall()


			Str = " ".join([str(_) for _ in tovar])
			tovar = re.sub("['|(|)|,]","",Str)
			if tovar == '':
				bot.send_message(message.chat.id,"Кошик порожній")
			else:
				#spisok_tovar = tovar.split('. ')
				#bot.send_message(message.chat.id, str(tovar))
				#for i in range(len(spisok_tovar)):
				#bot.send_message(call.message.chat.id, spisok_tovar[i])
				cur.execute("SELECT Product.Price, Order_Product.Count FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 0 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ?;", (id,))
				korzina = cur.fetchall()
				
				Str = " ".join([str(_) for _ in korzina])
				korzina = re.sub("['|(|)|,]","",Str)

				mas = korzina.split(' ')
				mas2 = []
				mas2 = list(map(float, mas))
				allPrice = 0 
				indexMassum = 0
				
				massum = [] 

				#otv = [] 
				for i in range(len(mas2)):
					if (i+1) % 2 == 0:
						massum.append(mas2[i-1] * mas2[i])
						#bot.send_message(call.message.chat.id,massum[indexMassum])
						allPrice += mas2[i-1] * mas2[i]
						if indexMassum + 1 != (len(mas2) / 2):
							indexMassum += 1

				cur.execute("SELECT Product.Name_Product , Order_Product.Count ,Product.Price, Order_Product.Count * Product.Price  FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 0 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ?;", (id,))
				korzina = cur.fetchall()
				#bot.send_message(call.message.chat.id, str(korzina))

				#####2 вариант вывода корзины
				Str = " ".join([str(_) for _ in korzina])
				korzina = re.sub("[|']","",Str)
				start = -1
				index = []
				i = 0

				while True:
					start = korzina.find(") (", start + 1)
					if start == -1:
						#bot.send_message(call.message.chat.id, "Не нашел")
						break
					else:
						index.append(start+2)
						#bot.send_message(call.message.chat.id, index[i])
						i += 1

				for x in range(len(index)):
					korzina = korzina[:index[x]-1] + "\n\n" + korzina[index[x]+1:]
				#bot.send_message(call.message.chat.id, korzina)
				start1 = -1
				index1 = []
				t = 0

				while True:
					start1 = korzina.find(".), ", start1 + 1)
					if start1 == -1:
						#bot.send_message(call.message.chat.id, "Не нашел")
						break
					else:
						index1.append(start1+2)
						#bot.send_message(call.message.chat.id, index1[t])
						t += 1

				for x in range(len(index1)):
					korzina = korzina[:index1[x]] + " " + korzina[index1[x]+1:]
				##bot.send_message(call.message.chat.id, korzina)
								
				start2 = -1
				index2 = []
				indexRavno = []
				r = 0

				while True:
					start2 = korzina.find(", ", start2 + 1)
					if start2 == -1:
						#bot.send_message(call.message.chat.id, "Не нашел")
						break
					else:
						if (r + 1) % 2 != 0:
							index2.append(start2)
							#bot.send_message(call.message.chat.id, index2[r])
							r += 1
						else: 
							indexRavno.append(start2)
							r += 1

				for x in range(len(index2)):
					korzina = korzina[:index2[x]] + "X " + korzina[index2[x]+2:]
				##bot.send_message(call.message.chat.id, korzina)

				for x in range(len(indexRavno)):
					korzina = korzina[:indexRavno[x]] + " =" + korzina[indexRavno[x]+2:]

				start3 = -1
				index3 = []
				g = 0

				while True:
					start3 = korzina.find(".)", start3 + 1)
					if start3 == -1:
						#bot.send_message(call.message.chat.id, "Не нашел")
						break
					else:
							index3.append(start3+2)
							g += 1

				for x in range(len(index3)):
					korzina = korzina[:index3[x]] + "\n" + korzina[index3[x]+1:]
				##bot.send_message(call.message.chat.id, korzina)

				Str = re.sub("[(|)]","",korzina)

				#bot.send_message(call.message.chat.id, "Кошик\n-----\nНазва, кількість, грн")
				#bot.send_message(call.message.chat.id,"Кошик\n-----\nНазва, кількість, грн\n\n" + str(Str) +'\n\nЗагалом: ' + str(allPrice)+"грн\n-----")
				##
				##ВЫВЕСТИ КНОПКИ ДЛЯ УДАЛЕНИЯ КОРЗИНЫ, РЕДАКТИРОВАНИЕ, ОФОРМЛЕНИЯ ЗАКАЗА
				##
				markup3 = types.InlineKeyboardMarkup(row_width=3)

				lline1 = types.InlineKeyboardButton("✏ Редагувати", callback_data='edit')
				lline2 = types.InlineKeyboardButton("❌ Видалити кошик", callback_data='deleteKorzina')
				lline3 = types.InlineKeyboardButton("✅ Оформити замовлення", callback_data='registration')
				markup3.add(lline1, lline2)
				markup3.add(lline3)

				# remove inline buttons
				globalMessengID=bot.send_message(message.chat.id,"Кошик\n-----\nНазва, кількість, грн\n\n" + str(Str) +'\n\nЗагалом: ' + str(allPrice)+"грн\n-----",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

		elif message.text == '🔍Пошук':#пункт меню
			con = sqlite3.connect('example.db')
			cur = con.cursor()
			globalAllZakaz = 0 
			cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (message.chat.id,))
			idclient = cur.fetchall()
			StrA = " ".join([str(_) for _ in idclient])
			globalIDClien=re.sub("['|(|)|,]","",StrA)
			id = int(globalIDClien) 
			cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
			ke = cur.fetchall()
			St = " ".join([str(_) for _ in ke])
			send_photo=re.sub("['|(|)|,]","",St)
			if int(send_photo) == 1:
				cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				ke=re.sub("['|(|)|,]","",St)
				bot.delete_message(message.chat.id, ke)
				cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
				con.commit()
			cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
			con.commit()
		
			markup3 = types.InlineKeyboardMarkup(row_width=2)

			lline1 = types.InlineKeyboardButton("Пошук За Назвою товару", callback_data='search1')
			lline2 = types.InlineKeyboardButton("Пошук За Типом товару", callback_data='search2') 
			markup3.add(lline1, lline2)

			bot.send_message(message.chat.id,"Обери тип пошуку",reply_markup=markup3)


		elif message.text == '📜Замовлення':
			con = sqlite3.connect('example.db')
			cur = con.cursor()
			globalAllZakaz = 0

			cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (message.chat.id,))
			idclient = cur.fetchall()

			#bot.send_message(user_id, idclient)
			#global globalIDClient
			StrA = " ".join([str(_) for _ in idclient])
			globalIDClien=re.sub("['|(|)|,]","",StrA)
			id = int(globalIDClien)
		
			cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
			con.commit()
	

			cur.execute("SELECT Product.Name_Product FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ?;", (id,))
			tovar = cur.fetchall()

			Str = " ".join([str(_) for _ in tovar])
			tovar = re.sub("['|(|)|,]","",Str)
			if tovar == '':
				bot.send_message(message.chat.id,"Зробіть замовлення, щоб побачити його тут!")
			else:
				cur.execute('SELECT DISTINCT [Order].Date_Order FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ? ORDER BY [Order].Date_Order', (id,))
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				bot.send_message(chat_id=message.chat.id, reply_markup=kb_product, text="Усі дати коли ви робили замовлення\nОберіть дату:")

				
		elif message.text == '❓Інформація':#пункт меню
			markup2 = types.InlineKeyboardMarkup(row_width=8)

			line1 = types.InlineKeyboardButton("Вартість доставки", callback_data='cina_dost')
			line2 = types.InlineKeyboardButton("Умови доставки", callback_data='ymova_dost')

			markup2.add(line1, line2)

			bot.send_message(message.chat.id, 'Вітаю! Я телеграм бот\nофіційного Інтернет магазину\nспортивного харчування ❤\nОберіть те що вас цікавить:', reply_markup=markup2)#выводим доп кнопки
		elif message.text == '📱Контакти':
			markup2 = types.InlineKeyboardMarkup(row_width=2)


			line1 = types.InlineKeyboardButton("Адреса", callback_data='adres')
			line2 = types.InlineKeyboardButton("Інтернет Магазин", url='https://bodymarket.ua/')
			markup2.add(line1)
			markup2.add(line2)

			bot.send_message(message.chat.id, 'Контактний номер телефона\n+380502746960', reply_markup=markup2)

		elif message.text == 'Пароль22087404':
			markup = types.ReplyKeyboardMarkup()
			item1 = types.KeyboardButton("📗Додати товар у Каталог")
			item2 = types.KeyboardButton("❌📗Видалити товар з Каталогу")
			item3 = types.KeyboardButton("✏Відредагувати товар з Каталогу")
			item4 = types.KeyboardButton("🛒Переглянути замовлення")
			markup.row(item1, item2, item3)
			markup.row(item4)

			bot.send_message(message.chat.id, "Добро пожалувати, {0.first_name}!\nЯ - <b>{1.first_name}</b>, ви увійшли під правами адміністратора.".format(message.from_user, bot.get_me()),parse_mode='html', reply_markup=markup)
		
		elif message.text == '✏Відредагувати товар з Каталогу':
			globalAllZakaz = 0 
			markup2 = types.InlineKeyboardMarkup(row_width=8)
			globalDell = 0
			globalsearch = 0
			globalRedag = 1
			con = sqlite3.connect('example.db')
			cur = con.cursor() 
			cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (message.chat.id,))
			idclient = cur.fetchall()
			StrA = " ".join([str(_) for _ in idclient])
			globalIDClien=re.sub("['|(|)|,]","",StrA)
			cur.execute("UPDATE Client_ID_Product SET globalDell = ? WHERE ID_Client = ?",('0', globalIDClien))
			con.commit()
			cur.execute("UPDATE Client_ID_Product SET globalsearch = ? WHERE ID_Client = ?",('0', globalIDClien))
			con.commit()
			cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
			con.commit()
			cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('1', globalIDClien))
			con.commit()
			cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
			ke = cur.fetchall()
			St = " ".join([str(_) for _ in ke])
			send_photo=re.sub("['|(|)|,]","",St)
			if int(send_photo) == 1:
				cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				ke=re.sub("['|(|)|,]","",St)
				bot.delete_message(message.chat.id, ke)
				cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
				con.commit()
			globalAllZakaz = 0 
			cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (message.chat.id,))
			idclient = cur.fetchall()
			StrA = " ".join([str(_) for _ in idclient])
			globalIDClien=re.sub("['|(|)|,]","",StrA)
			id = int(globalIDClien)
			
			cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
			ke = cur.fetchall()
			St = " ".join([str(_) for _ in ke])
			send_photo=re.sub("['|(|)|,]","",St)
			if int(send_photo) == 1:
				cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				ke=re.sub("['|(|)|,]","",St)
				bot.delete_message(message.chat.id, ke)
				cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
				con.commit()
			line1 = types.InlineKeyboardButton("Протеїн", callback_data='prot')
			line2 = types.InlineKeyboardButton("BCA", callback_data='bca')
			line3 = types.InlineKeyboardButton("Гейнер", callback_data='geaner')
			line4 = types.InlineKeyboardButton("Амінокислоти", callback_data='ami')
			line5 = types.InlineKeyboardButton("Креатин", callback_data='kreat')
			line6 = types.InlineKeyboardButton("L-Карнетин", callback_data='l_kor')
			line7 = types.InlineKeyboardButton("Жироспалювачі", callback_data='jir')
			line8 = types.InlineKeyboardButton("Вітаміни-Мінерали", callback_data='vit')

			markup2.add(line1, line2)
			markup2.add(line3, line4)
			markup2.add(line5, line6)
			markup2.add(line7, line8)

			bot.send_message(message.chat.id, 'Оберіть категорію товару:', reply_markup=markup2)#выводим доп кнопки

		elif message.text == '❌📗Видалити товар з Каталогу':
			globalAllZakaz = 0 
			markup2 = types.InlineKeyboardMarkup(row_width=8)
			globalDell = 1
			globalsearch = 0
			globalRedag = 0
			con = sqlite3.connect('example.db')
			cur = con.cursor() 
			cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (message.chat.id,))
			idclient = cur.fetchall()
			StrA = " ".join([str(_) for _ in idclient])
			globalIDClien=re.sub("['|(|)|,]","",StrA)
			cur.execute("UPDATE Client_ID_Product SET globalDell = ? WHERE ID_Client = ?",('1', globalIDClien))
			con.commit()
			cur.execute("UPDATE Client_ID_Product SET globalsearch = ? WHERE ID_Client = ?",('0', globalIDClien))
			con.commit()
			cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
			con.commit()
			cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
			con.commit()
			cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
			ke = cur.fetchall()
			St = " ".join([str(_) for _ in ke])
			send_photo=re.sub("['|(|)|,]","",St)
			if int(send_photo) == 1:
				cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				ke=re.sub("['|(|)|,]","",St)
				bot.delete_message(message.chat.id, ke)
				cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
				con.commit()
			globalAllZakaz = 0 
			cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (message.chat.id,))
			idclient = cur.fetchall()
			StrA = " ".join([str(_) for _ in idclient])
			globalIDClien=re.sub("['|(|)|,]","",StrA)
			id = int(globalIDClien)
			
			cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
			ke = cur.fetchall()
			St = " ".join([str(_) for _ in ke])
			send_photo=re.sub("['|(|)|,]","",St)
			if int(send_photo) == 1:
				cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				ke=re.sub("['|(|)|,]","",St)
				bot.delete_message(message.chat.id, ke)
				cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
				con.commit()
			line1 = types.InlineKeyboardButton("Протеїн", callback_data='prot')
			line2 = types.InlineKeyboardButton("BCA", callback_data='bca')
			line3 = types.InlineKeyboardButton("Гейнер", callback_data='geaner')
			line4 = types.InlineKeyboardButton("Амінокислоти", callback_data='ami')
			line5 = types.InlineKeyboardButton("Креатин", callback_data='kreat')
			line6 = types.InlineKeyboardButton("L-Карнетин", callback_data='l_kor')
			line7 = types.InlineKeyboardButton("Жироспалювачі", callback_data='jir')
			line8 = types.InlineKeyboardButton("Вітаміни-Мінерали", callback_data='vit')

			markup2.add(line1, line2)
			markup2.add(line3, line4)
			markup2.add(line5, line6)
			markup2.add(line7, line8)

			bot.send_message(message.chat.id, 'Оберіть категорію товару:', reply_markup=markup2)#выводим доп кнопки

		elif message.text == '📗Додати товар у Каталог':
			globalAllZakaz = 0 
			markup2 = types.InlineKeyboardMarkup(row_width=8)
			con = sqlite3.connect('example.db')
			cur = con.cursor()
			globalAllZakaz = 0 
			cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (message.chat.id,))
			idclient = cur.fetchall()
			StrA = " ".join([str(_) for _ in idclient])
			globalIDClien=re.sub("['|(|)|,]","",StrA)
			id = int(globalIDClien)
			
			cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
			con.commit()
			
			
			cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
			ke = cur.fetchall()
			St = " ".join([str(_) for _ in ke])
			send_photo=re.sub("['|(|)|,]","",St)
			if int(send_photo) == 1:
				cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				ke=re.sub("['|(|)|,]","",St)
				bot.delete_message(message.chat.id, ke)
				cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
				con.commit()
			line1 = types.InlineKeyboardButton("Протеїн", callback_data='prot_add')
			line2 = types.InlineKeyboardButton("BCA", callback_data='bca_add')
			line3 = types.InlineKeyboardButton("Гейнер", callback_data='geaner_add')
			line4 = types.InlineKeyboardButton("Амінокислоти", callback_data='ami_add')
			line5 = types.InlineKeyboardButton("Креатин", callback_data='kreat_add')
			line6 = types.InlineKeyboardButton("L-Карнетин", callback_data='l_kor_add')
			line7 = types.InlineKeyboardButton("Жиросжигатель", callback_data='jir_add')
			line8 = types.InlineKeyboardButton("Вітаміни-Мінерали", callback_data='vit_add')

			markup2.add(line1, line2)
			markup2.add(line3, line4)
			markup2.add(line5, line6)
			markup2.add(line7, line8)

			bot.send_message(message.chat.id, 'Оберіть категорію товару:', reply_markup=markup2)#выводим доп кнопки
		
		elif message.text == '🛒Переглянути замовлення':
			markup2 = types.InlineKeyboardMarkup(row_width=8)

			line1 = types.InlineKeyboardButton("Фільтр за датою", callback_data='ZakazOfDate')
			line2 = types.InlineKeyboardButton("Фільтр за Прізвищем Ім'ям клієнта", callback_data='ZakazOfFIO')
			line3 = types.InlineKeyboardButton("Пошук за Прізвищем Ім'ям клієнта ", callback_data='ZakazOfFIOSearch')

			markup2.add(line1, line2)
			markup2.add(line3)
		

			bot.send_message(message.chat.id, 'Перегляд замовлення:', reply_markup=markup2)#выводим доп кнопки

		elif message.text == 'Назад':
			markup = types.ReplyKeyboardMarkup()
			item1 = types.KeyboardButton("📗Каталог")
			item2 = types.KeyboardButton("🛒Kошик")
			item3 = types.KeyboardButton("🔍Пошук")
			item4 = types.KeyboardButton("📜Замовлення")
			item5 = types.KeyboardButton("❓Інформація")
			item6 = types.KeyboardButton("📱Контакти")
			item7 = types.KeyboardButton("🤵‍Особистий кабінет")
			markup.row(item1, item2)
			markup.row(item3, item4)
			markup.row(item5, item6)
			markup.row(item7)

			bot.send_message(message.chat.id, "Добро пожалувати, {0.first_name}!\nЯ - <b>{1.first_name}</b>, створений що б допомогти обрати спортивне харчування.".format(message.from_user, bot.get_me()),parse_mode='html', reply_markup=markup)

		else:
			bot.send_message(message.chat.id, 'Нажаль я не можу на це відповісти😥')

#ФУНКЦИИ ДЛЯ РАБОТЫ С ИНЛАЙНОВЫМИ КНОПКАМИ
@bot.callback_query_handler(func=lambda call: True)	
def callback_inline(call):
	try:
		if call.message:#основные кнопки
			global globalIDSubtype
			global globalIDSubtypeClient
			global globalIDProduct
			global globalIDClient
			#global globalEditProductID 
			#global globalCountEditProduct 
			#global globalEditIndex
			global globalMessengID
			global globalAllZakaz
			global globalAllZakazFIOID
			global globalRedag
			global globalPhoto 
			global globaldescription 
			global globalName 
			global globalPrice
			global send_photo
			if call.data == 'prot':#каталог товаров протеин
				markup3 = types.InlineKeyboardMarkup(row_width=6)

				lline1 = types.InlineKeyboardButton("Cироватковий концентрат", callback_data='prot_1')
				lline2 = types.InlineKeyboardButton("Cироватковий ізолят", callback_data='prot_2')
				lline3 = types.InlineKeyboardButton("Cироватковий гідролізат", callback_data='prot_3')
				lline4 = types.InlineKeyboardButton("Комплексний протеїн", callback_data='prot_4')
				lline5 = types.InlineKeyboardButton("Kазеїн", callback_data='prot_5')
				lline6 = types.InlineKeyboardButton("Суміш протеїнів рослинного походження", callback_data='prot_6')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5, lline6)

				# remove inline buttons
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть тип протеїну:",reply_markup=markup3)
			
			elif call.data == 'prot_1':
				globalIDSubtypeClient = 0
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				#bot.delete_message(call.message.chat.id, call.message.message_id)
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, call.message.message_id)
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 0;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")				

			elif call.data == 'prot_2':
				globalIDSubtypeClient = 1
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 1;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

			elif call.data == 'prot_3':
				globalIDSubtypeClient = 2
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 2;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")						

			elif call.data == 'prot_4':
				globalIDSubtypeClient = 3
				con = sqlite3.connect('example.db')
				cur = con.cursor()

				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 3;")
				key1 = cur.fetchall()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

			elif call.data == 'prot_5':
				globalIDSubtypeClient = 4
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 4;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")	

			elif call.data == 'prot_6':
				globalIDSubtypeClient = 5
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 5;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")	



			elif call.data == 'bca':#каталог товаров бца
				markup3 = types.InlineKeyboardMarkup(row_width=7)

				lline1 = types.InlineKeyboardButton("12:1:1", callback_data='bca_1')
				lline2 = types.InlineKeyboardButton("20:1:1", callback_data='bca_2')
				lline3 = types.InlineKeyboardButton("2:1:1", callback_data='bca_3')
				lline4 = types.InlineKeyboardButton("3:1:2", callback_data='bca_4')
				lline5 = types.InlineKeyboardButton("3:2:1", callback_data='bca_5')
				lline6 = types.InlineKeyboardButton("4:1:1", callback_data='bca_6')
				lline7 = types.InlineKeyboardButton("8:1:1", callback_data='bca_7')
				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5, lline6)
				markup3.add(lline7)

				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Співвідношення амінокислот:",reply_markup=markup3)
				
			elif call.data == 'bca_1':
				globalIDSubtypeClient = 6
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 6;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")	

			elif call.data == 'bca_2':
				globalIDSubtypeClient = 7
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 7;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")	

			elif call.data == 'bca_3':
				globalIDSubtypeClient = 8
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 8;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")	

			elif call.data == 'bca_4':
				globalIDSubtypeClient = 9
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 9;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")					

			elif call.data == 'bca_5':
				globalIDSubtypeClient = 10
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 10;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")	

			elif call.data == 'bca_6':
				globalIDSubtypeClient = 11
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 11;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")	

			elif call.data == 'bca_7':
				globalIDSubtypeClient = 12
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 12;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")	


			elif call.data == 'geaner':#каталог товаров гейнер
				markup3 = types.InlineKeyboardMarkup(row_width=6)

				lline1 = types.InlineKeyboardButton("Амінокислоти", callback_data='geaner_1')
				lline2 = types.InlineKeyboardButton("Вітаміни", callback_data='geaner_2')
				lline3 = types.InlineKeyboardButton("Креатин", callback_data='geaner_3')
				lline4 = types.InlineKeyboardButton("Таурин", callback_data='geaner_4')
				lline5 = types.InlineKeyboardButton("Трибулус", callback_data='geaner_5')
				lline6 = types.InlineKeyboardButton("Ферменти", callback_data='geaner_6')
				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5, lline6)

				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Містить добавки:",reply_markup=markup3)

			elif call.data == 'geaner_1':
				globalIDSubtypeClient = 13
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 13;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

			elif call.data == 'geaner_2':
				globalIDSubtypeClient = 14
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 14;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

			elif call.data == 'geaner_3':
				globalIDSubtypeClient = 15
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 15;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

			elif call.data == 'geaner_4':
				globalIDSubtypeClient = 16
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 16;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

			elif call.data == 'geaner_5':
				globalIDSubtypeClient = 17
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 17;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

			elif call.data == 'geaner_6':
				globalIDSubtypeClient = 18
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 18;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")				

			elif call.data == 'ami':#каталог товаров аминокислоты
				markup3 = types.InlineKeyboardMarkup(row_width=10)

				lline1 = types.InlineKeyboardButton("BCA", callback_data='ami_1')
				lline2 = types.InlineKeyboardButton("Аргінін", callback_data='ami_2')
				lline3 = types.InlineKeyboardButton("Бета-аланін", callback_data='ami_3')
				lline4 = types.InlineKeyboardButton("Вітаміни", callback_data='ami_4')
				lline5 = types.InlineKeyboardButton("Глютамін", callback_data='ami_5')
				lline6 = types.InlineKeyboardButton("Кофеїн", callback_data='ami_6')
				lline7 = types.InlineKeyboardButton("Мелатонін", callback_data='ami_7')
				lline8 = types.InlineKeyboardButton("Таурин", callback_data='ami_8')
				lline9 = types.InlineKeyboardButton("Цитруллін", callback_data='ami_9')
				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5, lline6)
				markup3.add(lline7, lline8)
				markup3.add(lline9)

				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Містить добавки:",reply_markup=markup3)

			elif call.data == 'ami_1':
				globalIDSubtypeClient = 19
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 19;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

			elif call.data == 'ami_2':
				globalIDSubtypeClient = 20
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 20;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

			elif call.data == 'ami_3':
				globalIDSubtypeClient = 21
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 21;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

			elif call.data == 'ami_4':
				globalIDSubtypeClient = 22
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 22;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

			elif call.data == 'ami_5':
				globalIDSubtypeClient = 23
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 23;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

			elif call.data == 'ami_6':
				globalIDSubtypeClient = 24
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 24;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

			elif call.data == 'ami_7':
				globalIDSubtypeClient = 25
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 25;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

			elif call.data == 'ami_8':
				globalIDSubtypeClient = 26
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 26;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

			elif call.data == 'ami_9':
				globalIDSubtypeClient = 27
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 27;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

			elif call.data == 'kreat':#каталог товаров креатин
				markup3 = types.InlineKeyboardMarkup(row_width=4)

				lline1 = types.InlineKeyboardButton("Моногідрат", callback_data='kreat_1')
				lline2 = types.InlineKeyboardButton("Суміш креатинів", callback_data='kreat_2')
				lline3 = types.InlineKeyboardButton("Креатин гідрохлорид", callback_data='kreat_3')
				lline4 = types.InlineKeyboardButton("Три креатин малат", callback_data='kreat_4')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)

				# remove inline buttons
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть тип креатину:",reply_markup=markup3)

			elif call.data == 'kreat_1':
				globalIDSubtypeClient = 28
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 28;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

			elif call.data == 'kreat_2':
				globalIDSubtypeClient = 29
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 29;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

			elif call.data == 'kreat_3':
				globalIDSubtypeClient = 30
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 30;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

			elif call.data == 'kreat_4':
				globalIDSubtypeClient = 31
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 31;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")


			elif call.data == 'l_kor':#каталог товаров л-корнитин
				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("CARNIPURE", callback_data='l_kor_1')
				lline2 = types.InlineKeyboardButton("L-Карнетин без добавок", callback_data='l_kor_2')
				lline3 = types.InlineKeyboardButton("L-Карнетин з добавками", callback_data='l_kor_3')
				lline4 = types.InlineKeyboardButton("Ацетил L-Карнетин", callback_data='l_kor_4')
				lline5 = types.InlineKeyboardButton("Суміш Карнетинів", callback_data='l_kor_5')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть тип L-Карнетину:",reply_markup=markup3)

			elif call.data == 'l_kor_1':
				globalIDSubtypeClient = 32
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 32;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

			elif call.data == 'l_kor_2':
				globalIDSubtypeClient = 33
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 33;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

			elif call.data == 'l_kor_3':
				globalIDSubtypeClient = 34
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 34;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

			elif call.data == 'l_kor_4':
				globalIDSubtypeClient = 35
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 35;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

			elif call.data == 'l_kor_5':
				globalIDSubtypeClient = 36
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 36;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

			elif call.data == 'jir':#каталог товаров жиросжигатель
				markup3 = types.InlineKeyboardMarkup(row_width=7)

				lline1 = types.InlineKeyboardButton("CLA", callback_data='jir_1')
				lline2 = types.InlineKeyboardButton("Зовнішні жироспалювачі", callback_data='jir_2')
				lline3 = types.InlineKeyboardButton("Зелений чай", callback_data='jir_3')
				lline4 = types.InlineKeyboardButton("Ліпотропні жироспалювачі", callback_data='jir_4')
				lline5 = types.InlineKeyboardButton("Оптимізатори щитовидної залози", callback_data='jir_5')
				lline6 = types.InlineKeyboardButton("Термогенні жироспалювачі", callback_data='jir_6')
				lline7 = types.InlineKeyboardButton("Універсальні жироспалювачі", callback_data='jir_7')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5, lline6)
				markup3.add(lline7)

				# remove inline buttons
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть тип Жироспалювача:",reply_markup=markup3)

			elif call.data == 'jir_1':
				globalIDSubtypeClient = 37
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 37;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

			elif call.data == 'jir_2':
				globalIDSubtypeClient = 38
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 38;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

			elif call.data == 'jir_3':
				globalIDSubtypeClient = 39
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 39;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

			elif call.data == 'jir_4':
				globalIDSubtypeClient = 40
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 40;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

			elif call.data == 'jir_5':
				globalIDSubtypeClient = 41
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 41;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

			elif call.data == 'jir_6':
				globalIDSubtypeClient = 42
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 42;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

			elif call.data == 'jir_7':
				globalIDSubtypeClient = 43
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 43;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

			elif call.data == 'vit':#каталог товаров витамины
				markup3 = types.InlineKeyboardMarkup(row_width=2)

				lline1 = types.InlineKeyboardButton("Для жінок", callback_data='vit_1')
				lline2 = types.InlineKeyboardButton("Для Чоловіків", callback_data='vit_2')

				markup3.add(lline1, lline2)

				# remove inline buttons
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть для кого:",reply_markup=markup3)

			elif call.data == 'vit_1':
				globalIDSubtypeClient = 44
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 44;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

			elif call.data == 'vit_2':
				globalIDSubtypeClient = 45
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				if send_photo == 1:
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					send_photo = 0
				cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 45;")
				key1 = cur.fetchall()

				kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

			elif call.data == 'cina_dost':
				bot.send_message(call.message.chat.id, 'Мінімальна сума замовлення: 1 грн 🥰\nПри замовленні до 600 грн - вартість доставки 50 грн. Якщо\n вартість замовлення більше 600 грн, доставка - безкоштовна 👍😍')

			elif call.data == 'ymova_dost':
				bot.send_message(call.message.chat.id, "Доставка здійснюється до вашої двері нашими кур'єрами")

			elif call.data == 'adres':
				bot.send_message(call.message.chat.id, "Дніпро, вул. О.М. Макарова, 27\nМагазин спортивного харчування:")
				bot.send_location(call.message.chat.id, 48.42902651043336, 34.99814183606439)

			elif call.data == 'back':
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				send_photo = 0
				IDSubtypeClient=(globalIDSubtypeClient)
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				
				#cur.execute("SELECT Product.Name_Product, Product.ID_Product FROM Product, Subtype_Product Where Product.Status = 1 and Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = ?;", (IDSubtypeClient,))
				#key1 = cur.fetchall()

				#kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
				#globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")



#АДМИНИСТРАТОР выбор товара и его подтипа
#
#
#
#АДМИНИСТРАТОР выбор товара и его подтипа
#ПОДТИПЫ ПРОТЕИНА
			elif call.data == 'prot_add':#добавление товара администратором протеин
				markup3 = types.InlineKeyboardMarkup(row_width=6)

				lline1 = types.InlineKeyboardButton("Cироватковий концентрат", callback_data='1prot_1')
				lline2 = types.InlineKeyboardButton("Cироватковий ізолят", callback_data='1prot_2')
				lline3 = types.InlineKeyboardButton("Cироватковий гідролізат", callback_data='1prot_3')
				lline4 = types.InlineKeyboardButton("Комплексний протеїн", callback_data='1prot_4')
				lline5 = types.InlineKeyboardButton("Kазеїн", callback_data='1prot_5')
				lline6 = types.InlineKeyboardButton("Суміш протеїнів рослинного походження", callback_data='1prot_6')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5, lline6)

				# remove inline buttons
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть тип протеїну:",reply_markup=markup3)

			elif call.data == '1prot_1':
				globalIDSubtype = 0 #подтип товара
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
		
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				
				id = int(globalIDClien)
				
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				bot.send_message(call.message.chat.id, "Додавання Cироватковий концентрат")

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1prot_2':
				#global globalIDSubtype
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 1 #подтип товара
				bot.send_message(call.message.chat.id, "Додавання Cироватковий ізолят")

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1prot_3':
				#global globalIDSubtype
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 2 #подтип товара
				bot.send_message(call.message.chat.id, "Додавання Cироватковий гідролізат")

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1prot_4':
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				#global globalIDSubtype
				globalIDSubtype = 3 #подтип товара
				bot.send_message(call.message.chat.id, "Додавання Комплексний протеїн")

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1prot_5':
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				#global globalIDSubtype
				globalIDSubtype = 4 #подтип товара
				bot.send_message(call.message.chat.id, "Додавання Kазеїн")

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1prot_6':
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				#global globalIDSubtype
				globalIDSubtype = 5 #подтип товара
				bot.send_message(call.message.chat.id, "Додавання Суміш протеїнів рослинного походження")

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

#АДМИНИСТРАТОР выбор товара и его подтипа
#ПОДТИПЫ БЦА			
			elif call.data == 'bca_add':#добавление товара администратором бца
				markup3 = types.InlineKeyboardMarkup(row_width=7)

				lline1 = types.InlineKeyboardButton("12:1:1", callback_data='1bca_1')
				lline2 = types.InlineKeyboardButton("20:1:1", callback_data='1bca_2')
				lline3 = types.InlineKeyboardButton("2:1:1", callback_data='1bca_3')
				lline4 = types.InlineKeyboardButton("3:1:2", callback_data='1bca_4')
				lline5 = types.InlineKeyboardButton("3:2:1", callback_data='1bca_5')
				lline6 = types.InlineKeyboardButton("4:1:1", callback_data='1bca_6')
				lline7 = types.InlineKeyboardButton("8:1:1", callback_data='1bca_7')
				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5, lline6)
				markup3.add(lline7)

				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Співвідношення амінокислот:",reply_markup=markup3)

			elif call.data == '1bca_1':#добавление товара администратором бца
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 6 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1bca_2':#добавление товара администратором бца
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 7 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1bca_3':#добавление товара администратором бца
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 8 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1bca_4':#добавление товара администратором бца
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 9 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1bca_5':#добавление товара администратором бца
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 10 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1bca_6':#добавление товара администратором бца
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 11 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1bca_7':#добавление товара администратором бца
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 12 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

#АДМИНИСТРАТОР выбор товара и его подтипа
#ПОДТИПЫ ГЕЙНЕРА
			elif call.data == 'geaner_add':#добавление товара администратором гейнер
				markup3 = types.InlineKeyboardMarkup(row_width=6)

				lline1 = types.InlineKeyboardButton("Амінокислоти", callback_data='1geaner_1')
				lline2 = types.InlineKeyboardButton("Вітаміни", callback_data='1geaner_2')
				lline3 = types.InlineKeyboardButton("Креатин", callback_data='1geaner_3')
				lline4 = types.InlineKeyboardButton("Таурин", callback_data='1geaner_4')
				lline5 = types.InlineKeyboardButton("Трибулус", callback_data='1geaner_5')
				lline6 = types.InlineKeyboardButton("Ферменти", callback_data='1geaner_6')
				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5, lline6)

				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Містить добавки:",reply_markup=markup3)

			elif call.data == '1geaner_1':#добавление товара администратором гейнер
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 13 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1geaner_2':#добавление товара администратором гейнер
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 14 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1geaner_3':#добавление товара администратором гейнер
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 15 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1geaner_4':#добавление товара администратором гейнер
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 16 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1geaner_5':#добавление товара администратором гейнер
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 17 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1geaner_6':#добавление товара администратором гейнер
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 18 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()
#АДМИНИСТРАТОР выбор товара и его подтипа
#ПОДТИПЫ АМИНОКИСОТ
			elif call.data == 'ami_add':#добавление товара администратором аминокислоты
				markup3 = types.InlineKeyboardMarkup(row_width=9)

				lline1 = types.InlineKeyboardButton("BCA", callback_data='1ami_1')
				lline2 = types.InlineKeyboardButton("Аргінін", callback_data='1ami_2')
				lline3 = types.InlineKeyboardButton("Бета-аланін", callback_data='1ami_3')
				lline4 = types.InlineKeyboardButton("Вітаміни", callback_data='1ami_4')
				lline5 = types.InlineKeyboardButton("Глютамін", callback_data='1ami_5')
				lline6 = types.InlineKeyboardButton("Кофеїн", callback_data='1ami_6')
				lline7 = types.InlineKeyboardButton("Мелатонін", callback_data='1ami_7')
				lline8 = types.InlineKeyboardButton("Таурин", callback_data='1ami_8')
				lline9 = types.InlineKeyboardButton("Цитруллін", callback_data='1ami_9')
				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5, lline6)
				markup3.add(lline7, lline8)
				markup3.add(lline9)

				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Містить добавки:",reply_markup=markup3)

			elif call.data == '1ami_1':#добавление товара администратором аминокислоты
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 19 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1ami_2':#добавление товара администратором аминокислоты
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 20 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1ami_3':#добавление товара администратором аминокислоты
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 21 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1ami_4':#добавление товара администратором аминокислоты
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 22 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1ami_5':#добавление товара администратором аминокислоты
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 23 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1ami_6':#добавление товара администратором аминокислоты
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 24 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1ami_7':#добавление товара администратором аминокислоты
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 25 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1ami_8':#добавление товара администратором аминокислоты
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 26 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1ami_9':#добавление товара администратором аминокислоты
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 27 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

#АДМИНИСТРАТОР выбор товара и его подтипа
#ПОДТИПЫ КРЕАТИНА
			elif call.data == 'kreat_add':#добавление товара администратором креатин
				markup3 = types.InlineKeyboardMarkup(row_width=4)

				lline1 = types.InlineKeyboardButton("Моногідрат", callback_data='1kreat_1')
				lline2 = types.InlineKeyboardButton("Суміш креатинів", callback_data='1kreat_2')
				lline3 = types.InlineKeyboardButton("Креатин гідрохлорид", callback_data='1kreat_3')
				lline4 = types.InlineKeyboardButton("Три креатин малат", callback_data='1kreat_4')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)

				# remove inline buttons
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть тип креатину:",reply_markup=markup3)

			elif call.data == '1kreat_1':#добавление товара администратором креатин
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 28 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1kreat_2':#добавление товара администратором креатин
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 29 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1kreat_3':#добавление товара администратором креатин
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 30 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1kreat_4':#добавление товара администратором креатин
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 31 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

#АДМИНИСТРАТОР выбор товара и его подтипа
#ПОДТИПЫ Л-КАРНИТИНА
			elif call.data == 'l_kor_add':#добавление товара администратором л-корнитин
				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("CARNIPURE", callback_data='1l_kor_1')
				lline2 = types.InlineKeyboardButton("L-Карнетин без добавок", callback_data='1l_kor_2')
				lline3 = types.InlineKeyboardButton("L-Карнетин з добавками", callback_data='1l_kor_3')
				lline4 = types.InlineKeyboardButton("Ацетил L-Карнетин", callback_data='1l_kor_4')
				lline5 = types.InlineKeyboardButton("Суміш Карнетинів", callback_data='1l_kor_5')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть тип L-Карнетину:",reply_markup=markup3)

			elif call.data == '1l_kor_1':#добавление товара администратором л-корнитин
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 32 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1l_kor_2':#добавление товара администратором л-корнитин
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 33 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()
				
			elif call.data == '1l_kor_3':#добавление товара администратором л-корнитин
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 34 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1l_kor_4':#добавление товара администратором л-корнитин
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 35 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1l_kor_5':#добавление товара администратором л-корнитин
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 36 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

#АДМИНИСТРАТОР выбор товара и его подтипа
#ПОДТИПЫ ЖИРОСЖИГАТЕЛЕЙ	
			elif call.data == 'jir_add':#добавление товара администратором жиросжигатель
				markup3 = types.InlineKeyboardMarkup(row_width=7)

				lline1 = types.InlineKeyboardButton("CLA", callback_data='1jir_1')
				lline2 = types.InlineKeyboardButton("Зовнішні жироспалювачі", callback_data='1jir_2')
				lline3 = types.InlineKeyboardButton("Зелений чай", callback_data='1jir_3')
				lline4 = types.InlineKeyboardButton("Ліпотропні жироспалювачі", callback_data='1jir_4')
				lline5 = types.InlineKeyboardButton("Оптимізатори щитовидної залози", callback_data='1jir_5')
				lline6 = types.InlineKeyboardButton("Термогенні жироспалювачі", callback_data='1jir_6')
				lline7 = types.InlineKeyboardButton("Універсальні жироспалювачі", callback_data='1jir_7')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5, lline6)
				markup3.add(lline7)

				# remove inline buttons
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть тип Жироспалювача:",reply_markup=markup3)

			elif call.data == '1jir_1':#добавление товара администратором жиросжигатель
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 37 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1jir_2':#добавление товара администратором жиросжигатель
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 38 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1jir_3':#добавление товара администратором жиросжигатель
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 39 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1jir_4':#добавление товара администратором жиросжигатель
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 40 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1jir_5':#добавление товара администратором жиросжигатель
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 41 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1jir_6':#добавление товара администратором жиросжигатель
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 42 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1jir_7':#добавление товара администратором жиросжигатель
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 43 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()


#АДМИНИСТРАТОР выбор товара и его подтипа
#ПОДТИПЫ ВИТАМИНОВ-МИНИРАЛОВ		
			elif call.data == 'vit_add':#добавление товара администратором витамины
				markup3 = types.InlineKeyboardMarkup(row_width=2)

				lline1 = types.InlineKeyboardButton("Для жінок", callback_data='1vit_1')
				lline2 = types.InlineKeyboardButton("Для Чоловіків", callback_data='1vit_2')

				markup3.add(lline1, lline2)

				# remove inline buttons
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть для кого:",reply_markup=markup3)

			elif call.data == '1vit_1':#добавление товара администратором витамины
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 44 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == '1vit_2':#добавление товара администратором витамины
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalRedag = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				globalIDSubtype = 45 #подтип товара

				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				markup3.add(lline5)

				# remove inline buttons
				globalMessengID =bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

####
##
#
#Удаление товара админом 

####
#Кнопки которые вызывают Функции Добавления названия, цены, описания и фото товара
#
#
#
			elif call.data == 'name':

				#bot.send_message(message.chat.id, "Добро пожалувати, {0.first_name}!\nЯ - <b>{1.first_name}</b>, створений що б допомогти обрати спортивне харчування.".format(message.from_user, bot.get_me()),parse_mode='html', reply_markup=markup)
				markup3 = types.InlineKeyboardMarkup(row_width=4)

				lline1 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline2 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline3 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline4 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)

				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()

				globalMessengID = bot.send_message(call.message.chat.id, "Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()
				msg = bot.send_message(call.message.chat.id, "Введіть назву товару")
				bot.register_next_step_handler(msg, process_name_step)
				#bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				#photoTovar(call.message.chat.id,Subtype)

			elif call.data == 'price':
				#photoTovar(call.message.chat.id)
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				#bot.send_message(call.message.chat.id, "Введенна ціна товару "+ globalPrice)
				markup3 = types.InlineKeyboardMarkup(row_width=4)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline3 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline4 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)
				# remove inline buttons
				#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
				globalMessengID =bot.send_message(call.message.chat.id, "Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()
				msg = bot.send_message(call.message.chat.id, "Введіть ціну товару")
				bot.register_next_step_handler(msg, process_price_step)
				#bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
				#photoTovar(call.message.chat.id,Subtype)

			elif call.data == 'description':
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				#bot.send_message(call.message.chat.id, "Введенний опис товару "+ globaldescription)
				markup3 = types.InlineKeyboardMarkup(row_width=4)

				lline1 = types.InlineKeyboardButton("Ввести назва товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline3 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
				lline4 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)

				# remove inline buttons
				#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
				globalMessengID =bot.send_message(call.message.chat.id, "Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()
				msg = bot.send_message(call.message.chat.id, "Введіть опис товару")
				bot.register_next_step_handler(msg, process_description_step)
				#bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)

			elif call.data == 'photo':
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 0 
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('0', globalIDClien))
				con.commit()
				
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				markup3 = types.InlineKeyboardMarkup(row_width=4)

				lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
				lline2 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
				lline3 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
				lline4 = types.InlineKeyboardButton("Зберігти", callback_data='save')

				markup3.add(lline1, lline2)
				markup3.add(lline3, lline4)

				# remove inline buttons
				#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
				globalMessengID =bot.send_message(call.message.chat.id, "Оберіть пункт додавання товару:",reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()
				bot.send_message(call.message.chat.id, "Оберіть фото товару")
				#bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Оберіть пункт додавання товару:",reply_markup=markup3)
			
			elif call.data == 'save':

				if globalPhoto != '0' and globaldescription != '0' and globalName !='0' and globalPrice != 0:
					con = sqlite3.connect('example.db')
					cur = con.cursor()
					tovar=(globalName, globalIDSubtype, globalPrice, globaldescription, globalPhoto)
					cur.execute("INSERT INTO Product (Name_Product, ID_Subtype, Price, Description, Photo) Values (?,?,?,?,?);", tovar)
					con.commit()
					globalPhoto = '0'
					globaldescription = '0' 
					globalName = '0' 
					globalPrice = 0
					bot.send_message(call.message.chat.id, "Товар додано!")
				else: 
					markup3 = types.InlineKeyboardMarkup(row_width=5)

					lline1 = types.InlineKeyboardButton("Ввести назву товару", callback_data='name')
					lline2 = types.InlineKeyboardButton("Ввести ціну товару", callback_data='price')
					lline3 = types.InlineKeyboardButton("Ввести опис товару", callback_data='description')
					lline4 = types.InlineKeyboardButton("Завантажити фото товару", callback_data='photo')
					lline5 = types.InlineKeyboardButton("Зберігти", callback_data='save')

					markup3.add(lline1, lline2)
					markup3.add(lline3, lline4)
					markup3.add(lline5)

					# remove inline buttons
					bot.send_message(call.message.chat.id, "Оберіть пункт додавання товару:",reply_markup=markup3)
					bot.send_message(call.message.chat.id, "Заповніть будь-ласка усе")

			elif call.data == 'addTOzakaz':
				con = sqlite3.connect('example.db')
				cur = con.cursor()

				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()

				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				Client=(globalIDClien)


				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()

				#bot.send_message(call.message.chat.id, 'Клиент'+ globalIDClient)
				cur.execute("SELECT [Order].ID_Order FROM [Order], Client  WHERE [Order].ID_Client = Client.ID_Client  and [Order].Status = 0 and Client.ID_Client  = ?;", (Client,))
				IDOrder = cur.fetchall()


				ordr = " ".join([str(_) for _ in IDOrder])
				IDOrder = re.sub("['|(|)|,]","",ordr)

				#bot.send_message(call.message.chat.id, 'Найденный заказ '+ IDOrder)
				#bot.send_message(call.message.chat.id, 'id product  '+ str(globalIDProduct))
				
				cur.execute("SELECT Client_ID_Product.ID_Product  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				#bot.send_message(call.message.chat.id,str(ke))

				St = " ".join([str(_) for _ in ke])
				ke=re.sub("['|(|)|,]","",St)

				TypeProduct=(ke)

				HaveProduct = (int(IDOrder),ke)

				cur.execute("SELECT Order_Product.ID_Product, Order_Product.Count FROM [Order], Order_Product  WHERE [Order].ID_Order = Order_Product.ID_Order and Order_Product.ID_Order  = ? and Order_Product.ID_Product = ? ;", (HaveProduct))
				ProductHaveAndCount = cur.fetchall()

				ProductHave = " ".join([str(_) for _ in ProductHaveAndCount])
				ProductHaveAndCount = re.sub("['|(|)|,]","",ProductHave)

				##сделать проверку на то что есть ли в этом заказе какой-то товар, что бы понять мне делать INSERT нового товара или UPDATE
				if ProductHaveAndCount == "":
					user = (int(IDOrder), ke, 1)
					cur.execute("INSERT INTO Order_Product VALUES(?, ?, ?);", user)
					con.commit()
					#bot.send_message(call.message.chat.id, 'нету товаров в корзине')	
				else:
					user = (int(IDOrder), ke)
					cur.execute("UPDATE Order_Product SET Count = Count + 1 WHERE Order_Product.ID_Order = ? and Order_Product.ID_Product = ? ;", (user))
					con.commit()
					#bot.send_message(call.message.chat.id, 'есть товари в корзине ' + str(ProductHaveAndCount))

				#cur.execute("UPDATE Client_ID_Producr SET ID_Product = ? WHERE ID_Client = ?",(globalIDProduct, globalIDClient))

				
		
				cur.execute("SELECT Product.Name_Product FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
				key2 = cur.fetchall()
				cur.execute("SELECT Product.Price  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
				key3 = cur.fetchall()
				cur.execute("SELECT Product.Photo  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
				key4 = cur.fetchall()
				cur.execute("SELECT Product.Description  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
				key6 = cur.fetchall()

				StrA = " ".join([str(_) for _ in key2])
				s1=re.sub("['|(|)|,]","",StrA)

				StrB = " ".join([str(_) for _ in key3])
				s2=re.sub("['|(|)|,]","",StrB)

				StrV = " ".join([str(_) for _ in key6])
				s3=re.sub("['|(|)|,]","",StrV)

				StrC = " ".join([str(_) for _ in key4])
				s4=re.sub("['|(|)|,]","",StrC)
 				#f'{text}\n{img}'
				markup3 = types.InlineKeyboardMarkup(row_width=3)

				lline1 = types.InlineKeyboardButton("✅" + s2 + "грн " + s1, callback_data='addTOzakaz')

				id = int(globalIDClien)
				cur.execute("SELECT Order_Product.* FROM [Order], Order_Product, Client Where [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 0 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ?;", (id,))
				korzina = cur.fetchall()
				#bot.send_message(call.message.chat.id, korzina)
				Str = " ".join([str(_) for _ in korzina])
				proverka = re.sub("['|(|)|,]","",Str)
				if proverka == "":
					#bot.send_message(call.message.chat.id, proverka) 
					lline2 = types.InlineKeyboardButton("🛍", callback_data='korzina')
				else:
					cur.execute("SELECT Product.Price, Order_Product.Count FROM Product, Order_Product, [Order], Client  WHERE Product.ID_Product = Order_Product.ID_Product and Order_Product.ID_Order = [Order].ID_Order and [Order].Status = 0 and Client.ID_Client = [Order].ID_Client and Client.ID_Client = ?;", (id,))
					cinaANDcount = cur.fetchall()
					Str = " ".join([str(_) for _ in cinaANDcount])
					cinaANDcount = re.sub("['|(|)|,]","",Str)
					allPrice = 0
					#bot.send_message(call.message.chat.id, cinaANDcount)
					mas = cinaANDcount.split(' ')
					mas2 = []
					mas2 = list(map(float, mas))

					for i in range(len(mas2)):
						if (i+1) % 2 == 0:
							#bot.send_message(call.message.chat.id, mas2[i-1] * mas2[i])
							allPrice += mas2[i-1] * mas2[i]
					lline2 = types.InlineKeyboardButton(str(allPrice) +"🛍", callback_data='korzina')

				lline3 = types.InlineKeyboardButton("Назад", callback_data='back')

				markup3.add(lline1, lline2)
				markup3.add(lline3)
				globalMessengID = bot.send_photo(call.message.chat.id, open(s4, 'rb'), caption= s1 +"\nЦіна: "+ s2 + "\nОпис: "+s3, parse_mode='Markdown', reply_markup=markup3)
				
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()
				#bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = 'аа', reply_markup=markup3)

			elif call.data == 'korzina':
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				cur.execute("SELECT Product.Name_Product FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 0 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ?;", (id,))
				tovar = cur.fetchall()


				Str = " ".join([str(_) for _ in tovar])
				tovar = re.sub("['|(|)|,]","",Str)
				if tovar == '':
					bot.send_message(call.message.chat.id,"Кошик порожній")
				else:
					#bot.send_message(call.message.chat.id,tovar)
					spisok_tovar = tovar.split('. ')
					#bot.send_message(call.message.chat.id, len(spisok_tovar))
					#for i in range(len(spisok_tovar)):
						#bot.send_message(call.message.chat.id, spisok_tovar[i])
					cur.execute("SELECT Product.Price, Order_Product.Count FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 0 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ?;", (id,))
					korzina = cur.fetchall()
					
					Str = " ".join([str(_) for _ in korzina])
					korzina = re.sub("['|(|)|,]","",Str)

					mas = korzina.split(' ')
					mas2 = []
					mas2 = list(map(float, mas))
					allPrice = 0 
					indexMassum = 0
					
					massum = [] 

					#otv = [] 
					for i in range(len(mas2)):
						if (i+1) % 2 == 0:
							massum.append(mas2[i-1] * mas2[i])
							#bot.send_message(call.message.chat.id,massum[indexMassum])
							allPrice += mas2[i-1] * mas2[i]
							if indexMassum + 1 != (len(mas2) / 2):
								indexMassum += 1

					cur.execute("SELECT Product.Name_Product , Order_Product.Count ,Product.Price, Order_Product.Count * Product.Price  FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 0 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ?;", (id,))
					korzina = cur.fetchall()
					#bot.send_message(call.message.chat.id, str(korzina))

					#####2 вариант вывода корзины
					Str = " ".join([str(_) for _ in korzina])
					korzina = re.sub("[|']","",Str)
					start = -1
					index = []
					i = 0

					while True:
						start = korzina.find(") (", start + 1)
						if start == -1:
							#bot.send_message(call.message.chat.id, "Не нашел")
							break
						else:
							index.append(start+2)
							#bot.send_message(call.message.chat.id, index[i])
							i += 1

					for x in range(len(index)):
						korzina = korzina[:index[x]-1] + "\n\n" + korzina[index[x]+1:]
					#bot.send_message(call.message.chat.id, korzina)
					start1 = -1
					index1 = []
					t = 0

					while True:
						start1 = korzina.find(".), ", start1 + 1)
						if start1 == -1:
							#bot.send_message(call.message.chat.id, "Не нашел")
							break
						else:
							index1.append(start1+2)
							#bot.send_message(call.message.chat.id, index1[t])
							t += 1

					for x in range(len(index1)):
						korzina = korzina[:index1[x]] + " " + korzina[index1[x]+1:]
					##bot.send_message(call.message.chat.id, korzina)
									
					start2 = -1
					index2 = []
					indexRavno = []
					r = 0

					while True:
						start2 = korzina.find(", ", start2 + 1)
						if start2 == -1:
							#bot.send_message(call.message.chat.id, "Не нашел")
							break
						else:
							if (r + 1) % 2 != 0:
								index2.append(start2)
								#bot.send_message(call.message.chat.id, index2[r])
								r += 1
							else: 
								indexRavno.append(start2)
								r += 1

					for x in range(len(index2)):
						korzina = korzina[:index2[x]] + "X " + korzina[index2[x]+2:]
					##bot.send_message(call.message.chat.id, korzina)

					for x in range(len(indexRavno)):
						korzina = korzina[:indexRavno[x]] + " =" + korzina[indexRavno[x]+2:]

					start3 = -1
					index3 = []
					g = 0

					while True:
						start3 = korzina.find(".)", start3 + 1)
						if start3 == -1:
							#bot.send_message(call.message.chat.id, "Не нашел")
							break
						else:
								index3.append(start3+2)
								g += 1

					for x in range(len(index3)):
						korzina = korzina[:index3[x]] + "\n" + korzina[index3[x]+1:]

					Str = re.sub("[(|)]","",korzina)

					##
					##ВЫВЕСТИ КНОПКИ ДЛЯ УДАЛЕНИЯ КОРЗИНЫ, РЕДАКТИРОВАНИЕ, ОФОРМЛЕНИЯ ЗАКАЗА
					##
					markup3 = types.InlineKeyboardMarkup(row_width=3)

					lline1 = types.InlineKeyboardButton("✏ Редагувати", callback_data='edit')
					lline2 = types.InlineKeyboardButton("❌ Видалити кошик", callback_data='deleteKorzina')
					lline3 = types.InlineKeyboardButton("✅ Оформити замовлення", callback_data='registration')
					markup3.add(lline1, lline2)
					markup3.add(lline3)

					# remove inline buttons
					globalMessengID = bot.send_message(call.message.chat.id,"Кошик\n-----\nНазва, кількість, грн\n\n" + str(Str) +'\n\nЗагалом: ' + str(allPrice)+"грн\n-----",reply_markup=markup3)
					cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
					con.commit()
					cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
					con.commit()
			##
			##РЕДАКТИРОВАНИЕ КОРЗИНЫ
			##
			elif call.data == 'edit':
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalEditIndex = 0 WHERE ID_Client = ?",(globalIDClien,))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalCountEditProduct = 0 WHERE ID_Client = ?",(globalIDClien,))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalEditProductID = 0 WHERE ID_Client = ?",(globalIDClien,))
				con.commit()
				
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				#bot.send_message(call.message.chat.id,str(id))


				cur.execute("SELECT Product.ID_Product  FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 0 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ?;", (id,))
				korzina = cur.fetchall()

				strCount = len(korzina)

				Str = " ".join([str(_) for _ in korzina[0]])
				korzinaIndex=re.sub("['|(|)|,]","",Str)
				##АЙДИ текущего товара в корзине
				globalEditProduct = int(Str)
				cur.execute("UPDATE Client_ID_Product SET globalEditProductID = ? WHERE ID_Client = ?",(globalEditProduct,id,))
				con.commit()
				cur.execute("SELECT Client_ID_Product.globalEditProductID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				ke = re.sub("['|(|)|,]","",St)
				#bot.send_message(call.message.chat.id, globalEditProductID)

				TypeProduct = (int(ke))
				#Str = " ".join([str(_) for _ in korzina])
				#korzina=re.sub("['|(|)|,]","",Str)
				#bot.send_message(call.message.chat.id,str(korzina))
				#bot.send_message(call.message.chat.id,korzina)
				#Str = korzina.replace(" ", " ")
				#Str = korzina.replace('.0', ' x')
				

				##индекс текущего товара в корзине
				#globalEditIndex = 0
				##АЙДИ текущего товара в корзине
				#globalEditProductID = Str[0]
				##Количество товаров в корзине
				#globalCountEditProduct = strCount
				cur.execute("UPDATE Client_ID_Product SET globalCountEditProduct = ? WHERE ID_Client = ?",(strCount,id,))
				con.commit()

				#TypeProduct = (str(Str[0]))
				
				cur.execute("SELECT Product.Name_Product FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
				key2 = cur.fetchall()
				#bot.send_message(call.message.chat.id,str(key2))
				cur.execute("SELECT Product.Price  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
				key3 = cur.fetchall()
				#bot.send_message(call.message.chat.id,str(key3))
				cur.execute("SELECT Product.Photo  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
				key4 = cur.fetchall()
				#bot.send_message(call.message.chat.id,str(key4))
				cur.execute("SELECT Product.Description  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
				key6 = cur.fetchall()
				#bot.send_message(call.message.chat.id,str(key6))

				Count = (id, ke)
				cur.execute("SELECT Order_Product.Count  FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 0 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ? and Product.ID_Product = ?;", (Count))
				count = cur.fetchall()
				#bot.send_message(call.message.chat.id,str(count))

				StrA = " ".join([str(_) for _ in count])
				count=re.sub("['|(|)|,]","",StrA)
				#bot.send_message(call.message.chat.id,count)
				

				StrA = " ".join([str(_) for _ in key2])
				s1=re.sub("['|(|)|,]","",StrA)

				StrB = " ".join([str(_) for _ in key3])
				s2=re.sub("['|(|)|,]","",StrB)

				StrV = " ".join([str(_) for _ in key6])
				s3=re.sub("['|(|)|,]","",StrV)

				StrC = " ".join([str(_) for _ in key4])
				s4=re.sub("['|(|)|,]","",StrC)

				cur.execute("SELECT Client_ID_Product.globalEditIndex  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				EditIndex = cur.fetchall()
				St = " ".join([str(_) for _ in EditIndex])
				EditIndex = re.sub("['|(|)|,]","",St)


				cur.execute("SELECT Client_ID_Product.globalCountEditProduct  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				CountEditProduct = cur.fetchall()
				St = " ".join([str(_) for _ in CountEditProduct])
				CountEditProduct = re.sub("['|(|)|,]","",St)
				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline3 = types.InlineKeyboardButton(" +1", callback_data='plus1')
				lline2 = types.InlineKeyboardButton(str(count) + " шт.", callback_data='e') 
				lline1 = types.InlineKeyboardButton("-1", callback_data='minus1') 
				lline4 = types.InlineKeyboardButton("⬅ ", callback_data='editBack')
				lline5 = types.InlineKeyboardButton(str(int(EditIndex)+1) +"/" + str(CountEditProduct), callback_data='e')
				lline6 = types.InlineKeyboardButton("➡ ", callback_data='editFront')
				lline7 = types.InlineKeyboardButton("✅ Завершити редагування", callback_data='editEnd')
				#bot.send_message(call.message.chat.id,korzina[0])
				#bot.send_message(call.message.chat.id,korzina[1])
				#bot.send_message(call.message.chat.id,str(korzina))
				markup3.add(lline1, lline2, lline3)
				markup3.add(lline4, lline5, lline6)
				markup3.add(lline7)
				globalMessengID = bot.send_photo(call.message.chat.id, open(s4, 'rb'), caption= s1 +"\nЦіна: "+ s2 + "\nОпис: "+s3, parse_mode='Markdown', reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == 'editBack':
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
			


				cur.execute("SELECT Product.ID_Product  FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 0 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ?;", (id,))
				korzina = cur.fetchall()
				##индекс текущего товара в корзине
				cur.execute("SELECT Client_ID_Product.globalEditIndex  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				EditIndex = cur.fetchall()
				St = " ".join([str(_) for _ in EditIndex])
				EditIndex = re.sub("['|(|)|,]","",St)
				
				EditIndex = int(EditIndex) - 1

				cur.execute("UPDATE Client_ID_Product SET globalEditIndex = ? WHERE ID_Client = ?",(EditIndex,id,))
				con.commit()
				
				cur.execute("SELECT Client_ID_Product.globalEditIndex  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				EditIndex = cur.fetchall()
				St = " ".join([str(_) for _ in EditIndex])
				EditIndex = re.sub("['|(|)|,]","",St)
				#bot.send_message(call.message.chat.id,globalEditIndex)
				if int(EditIndex) == -1:
					cur.execute("SELECT Client_ID_Product.globalCountEditProduct  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					CountEditProduct = cur.fetchall()
					St = " ".join([str(_) for _ in CountEditProduct])
					CountEditProduct = re.sub("['|(|)|,]","",St)
					EditIndex =  int(CountEditProduct) - 1
					cur.execute("UPDATE Client_ID_Product SET globalEditIndex = ? WHERE ID_Client = ?",(EditIndex,id,))
					con.commit()
					#bot.send_message(call.message.chat.id, globalEditIndex)

				cur.execute("SELECT Client_ID_Product.globalEditIndex  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				EditIndex = cur.fetchall()
				St = " ".join([str(_) for _ in EditIndex])
				EditIndex = re.sub("['|(|)|,]","",St)
				Str = " ".join([str(_) for _ in korzina[int(EditIndex)]])
				korzinaIndex=re.sub("['|(|)|,]","",Str)
				##АЙДИ текущего товара в корзине

				cur.execute("SELECT Product.ID_Product  FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 0 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ?;", (id,))
				korzina = cur.fetchall()

				strCount = len(korzina)

				Str = " ".join([str(_) for _ in korzina[int(EditIndex)]])
				korzinaIndex=re.sub("['|(|)|,]","",Str)
				##АЙДИ текущего товара в корзине

				cur.execute("UPDATE Client_ID_Product SET globalEditProductID = ? WHERE ID_Client = ?",(korzinaIndex,id,))
				con.commit()
				cur.execute("SELECT Client_ID_Product.globalEditProductID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				EditProductID = re.sub("['|(|)|,]","",St)
				#bot.send_message(call.message.chat.id, globalEditProductID)

				TypeProduct = (int(EditProductID))
				
				cur.execute("SELECT Product.Name_Product FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
				key2 = cur.fetchall()
				#bot.send_message(call.message.chat.id,str(key2))
				cur.execute("SELECT Product.Price  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
				key3 = cur.fetchall()
				#bot.send_message(call.message.chat.id,str(key3))
				cur.execute("SELECT Product.Photo  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
				key4 = cur.fetchall()
				#bot.send_message(call.message.chat.id,str(key4))
				cur.execute("SELECT Product.Description  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
				key6 = cur.fetchall()
				#bot.send_message(call.message.chat.id,str(key6))

				Count = (id, int(EditProductID))
				cur.execute("SELECT Order_Product.Count  FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 0 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ? and Product.ID_Product = ?;", (Count))
				count = cur.fetchall()
				#bot.send_message(call.message.chat.id,str(count))

				StrA = " ".join([str(_) for _ in count])
				count=re.sub("['|(|)|,]","",StrA)
				#bot.send_message(call.message.chat.id,count)
				

				StrA = " ".join([str(_) for _ in key2])
				s1=re.sub("['|(|)|,]","",StrA)

				StrB = " ".join([str(_) for _ in key3])
				s2=re.sub("['|(|)|,]","",StrB)

				StrV = " ".join([str(_) for _ in key6])
				s3=re.sub("['|(|)|,]","",StrV)

				StrC = " ".join([str(_) for _ in key4])
				s4=re.sub("['|(|)|,]","",StrC)
				cur.execute("SELECT Client_ID_Product.globalEditIndex  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				EditIndex = cur.fetchall()
				St = " ".join([str(_) for _ in EditIndex])
				EditIndex = re.sub("['|(|)|,]","",St)


				cur.execute("SELECT Client_ID_Product.globalCountEditProduct  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				CountEditProduct = cur.fetchall()
				St = " ".join([str(_) for _ in CountEditProduct])
				CountEditProduct = re.sub("['|(|)|,]","",St)
				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline3 = types.InlineKeyboardButton(" +1", callback_data='plus1')
				lline2 = types.InlineKeyboardButton(str(count) + " шт.", callback_data='e') 
				lline1 = types.InlineKeyboardButton("-1", callback_data='minus1') 
				lline4 = types.InlineKeyboardButton("⬅ ", callback_data='editBack')
				lline5 = types.InlineKeyboardButton(str(int(EditIndex)+1) +"/" + str(CountEditProduct), callback_data='e')
				lline6 = types.InlineKeyboardButton("➡ ", callback_data='editFront')
				lline7 = types.InlineKeyboardButton("✅ Завершити редагування", callback_data='editEnd')
				#bot.send_message(call.message.chat.id,korzina[0])
				#bot.send_message(call.message.chat.id,korzina[1])
				#bot.send_message(call.message.chat.id,str(korzina))
				markup3.add(lline1, lline2, lline3)
				markup3.add(lline4, lline5, lline6)
				markup3.add(lline7)
				globalMessengID = bot.send_photo(call.message.chat.id, open(s4, 'rb'), caption= s1 +"\nЦіна: "+ s2 + "\nОпис: "+s3, parse_mode='Markdown', reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == 'editFront':
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
			
				cur.execute("SELECT Product.ID_Product  FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 0 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ?;", (id,))
				korzina = cur.fetchall()
				##индекс текущего товара в корзине
				cur.execute("SELECT Client_ID_Product.globalEditIndex  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				EditIndex = cur.fetchall()
				St = " ".join([str(_) for _ in EditIndex])
				EditIndex = re.sub("['|(|)|,]","",St)
				
				EditIndex = int(EditIndex) + 1

				cur.execute("UPDATE Client_ID_Product SET globalEditIndex = ? WHERE ID_Client = ?",(EditIndex,id,))
				con.commit()
				
				cur.execute("SELECT Client_ID_Product.globalEditIndex  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				EditIndex = cur.fetchall()
				St = " ".join([str(_) for _ in EditIndex])
				EditIndex = re.sub("['|(|)|,]","",St)
				#bot.send_message(call.message.chat.id,globalEditIndex)
				#globalCountEditProduct:
					#globalEditIndex = 0
				cur.execute("SELECT Client_ID_Product.globalCountEditProduct  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				CountEditProduct = cur.fetchall()
				St = " ".join([str(_) for _ in CountEditProduct])
				CountEditProduct = re.sub("['|(|)|,]","",St)
				if int(EditIndex) >= int(CountEditProduct):
					EditIndex =  '0'
					cur.execute("UPDATE Client_ID_Product SET globalEditIndex = ? WHERE ID_Client = ?",(EditIndex,id,))
					con.commit()
					#bot.send_message(call.message.chat.id, globalEditIndex)

				cur.execute("SELECT Client_ID_Product.globalEditIndex  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				EditIndex = cur.fetchall()
				St = " ".join([str(_) for _ in EditIndex])
				EditIndex = re.sub("['|(|)|,]","",St)
				Str = " ".join([str(_) for _ in korzina[int(EditIndex)]])
				korzinaIndex=re.sub("['|(|)|,]","",Str)
				##АЙДИ текущего товара в корзине

				cur.execute("SELECT Product.ID_Product  FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 0 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ?;", (id,))
				korzina = cur.fetchall()

				strCount = len(korzina)

				Str = " ".join([str(_) for _ in korzina[int(EditIndex)]])
				korzinaIndex=re.sub("['|(|)|,]","",Str)
				##АЙДИ текущего товара в корзине

				cur.execute("UPDATE Client_ID_Product SET globalEditProductID = ? WHERE ID_Client = ?",(korzinaIndex,id,))
				con.commit()
				cur.execute("SELECT Client_ID_Product.globalEditProductID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				EditProductID = re.sub("['|(|)|,]","",St)
				#bot.send_message(call.message.chat.id, globalEditProductID)

				TypeProduct = (int(EditProductID))
				
				cur.execute("SELECT Product.Name_Product FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
				key2 = cur.fetchall()
				#bot.send_message(call.message.chat.id,str(key2))
				cur.execute("SELECT Product.Price  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
				key3 = cur.fetchall()
				#bot.send_message(call.message.chat.id,str(key3))
				cur.execute("SELECT Product.Photo  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
				key4 = cur.fetchall()
				#bot.send_message(call.message.chat.id,str(key4))
				cur.execute("SELECT Product.Description  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
				key6 = cur.fetchall()
				#bot.send_message(call.message.chat.id,str(key6))

				Count = (id, int(EditProductID))
				cur.execute("SELECT Order_Product.Count  FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 0 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ? and Product.ID_Product = ?;", (Count))
				count = cur.fetchall()
				#bot.send_message(call.message.chat.id,str(count))

				StrA = " ".join([str(_) for _ in count])
				count=re.sub("['|(|)|,]","",StrA)
				#bot.send_message(call.message.chat.id,count)
				

				StrA = " ".join([str(_) for _ in key2])
				s1=re.sub("['|(|)|,]","",StrA)

				StrB = " ".join([str(_) for _ in key3])
				s2=re.sub("['|(|)|,]","",StrB)

				StrV = " ".join([str(_) for _ in key6])
				s3=re.sub("['|(|)|,]","",StrV)

				StrC = " ".join([str(_) for _ in key4])
				s4=re.sub("['|(|)|,]","",StrC)
				cur.execute("SELECT Client_ID_Product.globalEditIndex  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				EditIndex = cur.fetchall()
				St = " ".join([str(_) for _ in EditIndex])
				EditIndex = re.sub("['|(|)|,]","",St)


				cur.execute("SELECT Client_ID_Product.globalCountEditProduct  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				CountEditProduct = cur.fetchall()
				St = " ".join([str(_) for _ in CountEditProduct])
				CountEditProduct = re.sub("['|(|)|,]","",St)
				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline3 = types.InlineKeyboardButton(" +1", callback_data='plus1')
				lline2 = types.InlineKeyboardButton(str(count) + " шт.", callback_data='e') 
				lline1 = types.InlineKeyboardButton("-1", callback_data='minus1') 
				lline4 = types.InlineKeyboardButton("⬅ ", callback_data='editBack')
				lline5 = types.InlineKeyboardButton(str(int(EditIndex)+1) +"/" + str(CountEditProduct), callback_data='e')
				lline6 = types.InlineKeyboardButton("➡ ", callback_data='editFront')
				lline7 = types.InlineKeyboardButton("✅ Завершити редагування", callback_data='editEnd')
				#bot.send_message(call.message.chat.id,korzina[0])
				#bot.send_message(call.message.chat.id,korzina[1])
				#bot.send_message(call.message.chat.id,str(korzina))
				markup3.add(lline1, lline2, lline3)
				markup3.add(lline4, lline5, lline6)
				markup3.add(lline7)
				globalMessengID = bot.send_photo(call.message.chat.id, open(s4, 'rb'), caption= s1 +"\nЦіна: "+ s2 + "\nОпис: "+s3, parse_mode='Markdown', reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()
				
			elif call.data == 'minus1':
				con = sqlite3.connect('example.db')
				cur = con.cursor()

				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				#bot.send_message(call.message.chat.id, globalIDClient)

				cur.execute("SELECT [Order].ID_Order FROM [Order], Client  WHERE [Order].ID_Client = Client.ID_Client  and [Order].Status = 0 and Client.ID_Client  = ?;", (id,))
				IDOrder = cur.fetchall()

				ordr = " ".join([str(_) for _ in IDOrder])
				IDOrder = re.sub("['|(|)|,]","",ordr)

				#bot.send_message(call.message.chat.id, IDOrder)
				cur.execute("SELECT Client_ID_Product.globalEditProductID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				EditProductID = re.sub("['|(|)|,]","",St)
				Count = (id, int(EditProductID))

				cur.execute("SELECT Order_Product.Count  FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 0 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ? and Product.ID_Product = ?;", (Count))
				count = cur.fetchall()
				#bot.send_message(call.message.chat.id,str(count))

				StrA = " ".join([str(_) for _ in count])
				count=re.sub("['|(|)|,]","",StrA)

				#bot.send_message(call.message.chat.id, count)

				if int(count) <= 0:
					count = 0
				else:
					user = (int(IDOrder), int(EditProductID))
					cur.execute("UPDATE Order_Product SET Count = Count - 1 WHERE Order_Product.ID_Order = ? and Order_Product.ID_Product = ? ;", (user))
					con.commit()

				Count = (id, int(EditProductID))
				cur.execute("SELECT Order_Product.Count  FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 0 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ? and Product.ID_Product = ?;", (Count))
				count = cur.fetchall()
				#bot.send_message(call.message.chat.id,str(count))

				StrA = " ".join([str(_) for _ in count])
				count=re.sub("['|(|)|,]","",StrA)

				#bot.send_message(call.message.chat.id, globalEditProductID)

				TypeProduct = (int(EditProductID))
				
				cur.execute("SELECT Product.Name_Product FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
				key2 = cur.fetchall()
				#bot.send_message(call.message.chat.id,str(key2))
				cur.execute("SELECT Product.Price  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
				key3 = cur.fetchall()
				#bot.send_message(call.message.chat.id,str(key3))
				cur.execute("SELECT Product.Photo  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
				key4 = cur.fetchall()
				#bot.send_message(call.message.chat.id,str(key4))
				cur.execute("SELECT Product.Description  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
				key6 = cur.fetchall()
				#bot.send_message(call.message.chat.id,str(key6))
			
				StrA = " ".join([str(_) for _ in key2])
				s1=re.sub("['|(|)|,]","",StrA)

				StrB = " ".join([str(_) for _ in key3])
				s2=re.sub("['|(|)|,]","",StrB)

				StrV = " ".join([str(_) for _ in key6])
				s3=re.sub("['|(|)|,]","",StrV)

				StrC = " ".join([str(_) for _ in key4])
				s4=re.sub("['|(|)|,]","",StrC)
				##Количество товаров в корзине
				#globalCountEditProduct = strCount
				#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
				cur.execute("SELECT Client_ID_Product.globalEditIndex  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				EditIndex = cur.fetchall()
				St = " ".join([str(_) for _ in EditIndex])
				EditIndex = re.sub("['|(|)|,]","",St)


				cur.execute("SELECT Client_ID_Product.globalCountEditProduct  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				CountEditProduct = cur.fetchall()
				St = " ".join([str(_) for _ in CountEditProduct])
				CountEditProduct = re.sub("['|(|)|,]","",St)
				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline3 = types.InlineKeyboardButton(" +1", callback_data='plus1')
				lline2 = types.InlineKeyboardButton(str(count) + " шт.", callback_data='e') 
				lline1 = types.InlineKeyboardButton("-1", callback_data='minus1') 
				lline4 = types.InlineKeyboardButton("⬅ ", callback_data='editBack')
				lline5 = types.InlineKeyboardButton(str(int(EditIndex)+1) +"/" + str(CountEditProduct), callback_data='e')
				lline6 = types.InlineKeyboardButton("➡ ", callback_data='editFront')
				lline7 = types.InlineKeyboardButton("✅ Завершити редагування", callback_data='editEnd')
				#bot.send_message(call.message.chat.id,korzina[0])
				#bot.send_message(call.message.chat.id,korzina[1])
				#bot.send_message(call.message.chat.id,str(korzina))
				markup3.add(lline1, lline2, lline3)
				markup3.add(lline4, lline5, lline6)
				markup3.add(lline7)
				globalMessengID = bot.send_photo(call.message.chat.id, open(s4, 'rb'), caption= s1 +"\nЦіна: "+ s2 + "\nОпис: "+s3, parse_mode='Markdown', reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()

			elif call.data == 'plus1':
				con = sqlite3.connect('example.db')
				cur = con.cursor()

				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				#bot.send_message(call.message.chat.id, globalIDClient)

				cur.execute("SELECT [Order].ID_Order FROM [Order], Client  WHERE [Order].ID_Client = Client.ID_Client  and [Order].Status = 0 and Client.ID_Client  = ?;", (id,))
				IDOrder = cur.fetchall()

				ordr = " ".join([str(_) for _ in IDOrder])
				IDOrder = re.sub("['|(|)|,]","",ordr)

				#bot.send_message(call.message.chat.id, IDOrder)
				cur.execute("SELECT Client_ID_Product.globalEditProductID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				EditProductID = re.sub("['|(|)|,]","",St)
				user = (int(IDOrder), int(EditProductID))
				cur.execute("UPDATE Order_Product SET Count = Count + 1 WHERE Order_Product.ID_Order = ? and Order_Product.ID_Product = ? ;", (user))
				con.commit()
				#bot.send_message(call.message.chat.id, globalEditProductID)

				TypeProduct = (int(EditProductID))
				
				cur.execute("SELECT Product.Name_Product FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
				key2 = cur.fetchall()
				#bot.send_message(call.message.chat.id,str(key2))
				cur.execute("SELECT Product.Price  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
				key3 = cur.fetchall()
				#bot.send_message(call.message.chat.id,str(key3))
				cur.execute("SELECT Product.Photo  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
				key4 = cur.fetchall()
				#bot.send_message(call.message.chat.id,str(key4))
				cur.execute("SELECT Product.Description  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
				key6 = cur.fetchall()
				#bot.send_message(call.message.chat.id,str(key6))

				Count = (id, int(EditProductID))
				cur.execute("SELECT Order_Product.Count  FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 0 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ? and Product.ID_Product = ?;", (Count))
				count = cur.fetchall()
				#bot.send_message(call.message.chat.id,str(count))

				StrA = " ".join([str(_) for _ in count])
				count=re.sub("['|(|)|,]","",StrA)
				#bot.send_message(call.message.chat.id,count)
				

				StrA = " ".join([str(_) for _ in key2])
				s1=re.sub("['|(|)|,]","",StrA)

				StrB = " ".join([str(_) for _ in key3])
				s2=re.sub("['|(|)|,]","",StrB)

				StrV = " ".join([str(_) for _ in key6])
				s3=re.sub("['|(|)|,]","",StrV)

				StrC = " ".join([str(_) for _ in key4])
				s4=re.sub("['|(|)|,]","",StrC)
				##Количество товаров в корзине
				#globalCountEditProduct = strCount
				#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
				cur.execute("SELECT Client_ID_Product.globalEditIndex  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				EditIndex = cur.fetchall()
				St = " ".join([str(_) for _ in EditIndex])
				EditIndex = re.sub("['|(|)|,]","",St)


				cur.execute("SELECT Client_ID_Product.globalCountEditProduct  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				CountEditProduct = cur.fetchall()
				St = " ".join([str(_) for _ in CountEditProduct])
				CountEditProduct = re.sub("['|(|)|,]","",St)
				markup3 = types.InlineKeyboardMarkup(row_width=5)

				lline3 = types.InlineKeyboardButton(" +1", callback_data='plus1')
				lline2 = types.InlineKeyboardButton(str(count) + " шт.", callback_data='e') 
				lline1 = types.InlineKeyboardButton("-1", callback_data='minus1') 
				lline4 = types.InlineKeyboardButton("⬅ ", callback_data='editBack')
				lline5 = types.InlineKeyboardButton(str(int(EditIndex)+1) +"/" + str(CountEditProduct), callback_data='e')
				lline6 = types.InlineKeyboardButton("➡ ", callback_data='editFront')
				lline7 = types.InlineKeyboardButton("✅ Завершити редагування", callback_data='editEnd')
				#bot.send_message(call.message.chat.id,korzina[0])
				#bot.send_message(call.message.chat.id,korzina[1])
				#bot.send_message(call.message.chat.id,str(korzina))
				markup3.add(lline1, lline2, lline3)
				markup3.add(lline4, lline5, lline6)
				markup3.add(lline7)
				globalMessengID = bot.send_photo(call.message.chat.id, open(s4, 'rb'), caption= s1 +"\nЦіна: "+ s2 + "\nОпис: "+s3, parse_mode='Markdown', reply_markup=markup3)
				cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
				con.commit()


			elif call.data == 'editEnd':
				con = sqlite3.connect('example.db')
				cur = con.cursor()

				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalEditIndex = 0 WHERE ID_Client = ?",(globalIDClien,))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalCountEditProduct = 0 WHERE ID_Client = ?",(globalIDClien,))
				con.commit()
				cur.execute("UPDATE Client_ID_Product SET globalEditProductID = 0 WHERE ID_Client = ?",(globalIDClien,))
				con.commit()
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()

				cur.execute("SELECT [Order].ID_Order FROM [Order], Client  WHERE [Order].ID_Client = Client.ID_Client  and [Order].Status = 0 and Client.ID_Client  = ?;", (id,))
				IDOrder = cur.fetchall()

				ordr = " ".join([str(_) for _ in IDOrder])
				IDOrder = re.sub("['|(|)|,]","",ordr)

				#####ИЩЕМ ТОВАРЫ В КОРЗИНЕ С КОЛИЧЕСТВОМ 0 И УДАЛЯЕМ ИЗ КОРЗИНЫ ЕГО
				cur.execute("SELECT Product.ID_Product  FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 0 and [Order].ID_Client = Client.ID_Client and Order_Product.Count = 0  and [Order].ID_Client = ?;", (id,))
				IDProductFromCount0 = cur.fetchall()
				#bot.send_message(call.message.chat.id,str(IDProductFromCount0))

				#Str = " ".join([str(_) for _ in IDProductFromCount0])
				#IDProductFromCount0=re.sub("['|(|)|,]","",Str)

				#cur.execute("SELECT Order_Product.ID_Order FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 0 and [Order].ID_Client = Client.ID_Client and Order_Product.Count = 0  and [Order].ID_Client = ?;", (id,))
				#IDOrderFromCount0 = cur.fetchall()
				#bot.send_message(call.message.chat.id,str(IDOrderFromCount0))
				#Str = " ".join([str(_) for _ in IDProductFromCount0])
				#IDProductFromCount0=re.sub("['|(|)|,]","",Str)

				if str(IDProductFromCount0) != "[]":
					##ЗДЕСЬ Я УДАЛЯЮ ТОВАР ИЗ КОРЗИНЫ ПО ЛИСТУ С НАЙДЕННЫМИ ИНДЕКСАМИ
					for i in IDProductFromCount0:
						StrA = " ".join([str(_) for _ in i])
						i=re.sub("['|(|)|,]","",StrA)
						#bot.send_message(call.message.chat.id,str(i))
						#bot.send_message(call.message.chat.id,i)
						user = (int(i), int(IDOrder))
						cur.execute("DELETE FROM Order_Product WHERE Order_Product.ID_Product = ? and Order_Product.ID_Order = ?;", (user))
						con.commit()


					#bot.send_message(call.message.chat.id,str(IDProductFromCount0))
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)

				#else: 
					#bot.send_message(call.message.chat.id,'Равно нулу вроде как')
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)

				cur.execute("SELECT Product.Name_Product FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 0 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ?;", (id,))
				tovar = cur.fetchall()

				Str = " ".join([str(_) for _ in tovar])
				tovar = re.sub("['|(|)|,]","",Str)
				if tovar == '':
					bot.send_message(call.message.chat.id,"Кошик порожній")
				else:
					#bot.send_message(call.message.chat.id,tovar)
					spisok_tovar = tovar.split('. ')
					#bot.send_message(call.message.chat.id, len(spisok_tovar))
					#for i in range(len(spisok_tovar)):
						#bot.send_message(call.message.chat.id, spisok_tovar[i])
					cur.execute("SELECT Product.Price, Order_Product.Count FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 0 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ?;", (id,))
					korzina = cur.fetchall()
					
					Str = " ".join([str(_) for _ in korzina])
					korzina = re.sub("['|(|)|,]","",Str)

					mas = korzina.split(' ')
					mas2 = []
					mas2 = list(map(float, mas))
					allPrice = 0 
					indexMassum = 0
					
					massum = [] 

					#otv = [] 
					for i in range(len(mas2)):
						if (i+1) % 2 == 0:
							massum.append(mas2[i-1] * mas2[i])
							#bot.send_message(call.message.chat.id,massum[indexMassum])
							allPrice += mas2[i-1] * mas2[i]
							if indexMassum + 1 != (len(mas2) / 2):
								indexMassum += 1

					cur.execute("SELECT Product.Name_Product , Order_Product.Count ,Product.Price, Order_Product.Count * Product.Price  FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 0 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ?;", (id,))
					korzina = cur.fetchall()
					#bot.send_message(call.message.chat.id, str(korzina))

					#####2 вариант вывода корзины
					Str = " ".join([str(_) for _ in korzina])
					korzina = re.sub("[|']","",Str)
					start = -1
					index = []
					i = 0

					while True:
						start = korzina.find(") (", start + 1)
						if start == -1:
							#bot.send_message(call.message.chat.id, "Не нашел")
							break
						else:
							index.append(start+2)
							#bot.send_message(call.message.chat.id, index[i])
							i += 1

					for x in range(len(index)):
						korzina = korzina[:index[x]-1] + "\n\n" + korzina[index[x]+1:]
					#bot.send_message(call.message.chat.id, korzina)
					start1 = -1
					index1 = []
					t = 0

					while True:
						start1 = korzina.find(".), ", start1 + 1)
						if start1 == -1:
							#bot.send_message(call.message.chat.id, "Не нашел")
							break
						else:
							index1.append(start1+2)
							#bot.send_message(call.message.chat.id, index1[t])
							t += 1

					for x in range(len(index1)):
						korzina = korzina[:index1[x]] + " " + korzina[index1[x]+1:]
					##bot.send_message(call.message.chat.id, korzina)
									
					start2 = -1
					index2 = []
					indexRavno = []
					r = 0

					while True:
						start2 = korzina.find(", ", start2 + 1)
						if start2 == -1:
							#bot.send_message(call.message.chat.id, "Не нашел")
							break
						else:
							if (r + 1) % 2 != 0:
								index2.append(start2)
								#bot.send_message(call.message.chat.id, index2[r])
								r += 1
							else: 
								indexRavno.append(start2)
								r += 1

					for x in range(len(index2)):
						korzina = korzina[:index2[x]] + "X " + korzina[index2[x]+2:]
					##bot.send_message(call.message.chat.id, korzina)

					for x in range(len(indexRavno)):
						korzina = korzina[:indexRavno[x]] + " =" + korzina[indexRavno[x]+2:]

					start3 = -1
					index3 = []
					g = 0

					while True:
						start3 = korzina.find(".)", start3 + 1)
						if start3 == -1:
							#bot.send_message(call.message.chat.id, "Не нашел")
							break
						else:
								index3.append(start3+2)
								g += 1

					for x in range(len(index3)):
						korzina = korzina[:index3[x]] + "\n" + korzina[index3[x]+1:]

					Str = re.sub("[(|)]","",korzina)

					##
					##ВЫВЕСТИ КНОПКИ ДЛЯ УДАЛЕНИЯ КОРЗИНЫ, РЕДАКТИРОВАНИЕ, ОФОРМЛЕНИЯ ЗАКАЗА
					##
					markup3 = types.InlineKeyboardMarkup(row_width=3)

					lline1 = types.InlineKeyboardButton("✏ Редагувати", callback_data='edit')
					lline2 = types.InlineKeyboardButton("❌ Видалити кошик", callback_data='deleteKorzina')
					lline3 = types.InlineKeyboardButton("✅ Оформити замовлення", callback_data='registration')
					markup3.add(lline1, lline2)
					markup3.add(lline3)

					# remove inline buttons
					globalMessengID = bot.send_message(call.message.chat.id,"Кошик\n-----\nНазва, кількість, грн\n\n" + str(Str) +'\n\nЗагалом: ' + str(allPrice)+"грн\n-----",reply_markup=markup3)
					cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
					con.commit()
					cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
					con.commit()
			##
			##УДАЛЕНИЕ КОРЗИНЫ(товаров в корзине)
			##
			elif call.data == 'deleteKorzina':
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()
				#bot.send_message(call.message.chat.id, globalIDClient)

				cur.execute("SELECT [Order].ID_Order FROM [Order], Client  WHERE [Order].ID_Client = Client.ID_Client  and [Order].Status = 0 and Client.ID_Client  = ?;", (id,))
				IDOrder = cur.fetchall()

				ordr = " ".join([str(_) for _ in IDOrder])
				IDOrder = re.sub("['|(|)|,]","",ordr)

				user = (IDOrder)

				cur.execute("DELETE FROM Order_Product WHERE Order_Product.ID_Order = ?;", (user,))
				con.commit()

				cur.execute("SELECT Product.Name_Product FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 0 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ?;", (id,))
				tovar = cur.fetchall()

				Str = " ".join([str(_) for _ in tovar])
				tovar = re.sub("['|(|)|,]","",Str)
				if tovar == '':
					bot.send_message(call.message.chat.id,"Кошик порожній")

				#bot.send_message(call.message.chat.id,'sd')
			##
			##ПОДТВЕРЖДЕНИЕ ЗАКАЗА(ОФОРМЛЕНИЕ)
			##
			elif call.data == 'registration':
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				
				cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				ke = cur.fetchall()
				St = " ".join([str(_) for _ in ke])
				send_photo=re.sub("['|(|)|,]","",St)
				if int(send_photo) == 1:
					cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					ke=re.sub("['|(|)|,]","",St)
					bot.delete_message(call.message.chat.id, ke)
					cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
					con.commit()

				cur.execute("SELECT [Order].ID_Order FROM [Order], Client  WHERE [Order].ID_Client = Client.ID_Client  and [Order].Status = 0 and Client.ID_Client  = ?;", (id,))
				IDOrder = cur.fetchall()

				ordr = " ".join([str(_) for _ in IDOrder])
				IDOrder = re.sub("['|(|)|,]","",ordr)

				cur.execute("SELECT Product.ID_Product  FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 0 and [Order].ID_Client = Client.ID_Client and Order_Product.Count = 0  and [Order].ID_Client = ?;", (globalIDClien,))
				IDProductFromCount0 = cur.fetchall()
				
				if str(IDProductFromCount0) != "[]":
					##ЗДЕСЬ Я УДАЛЯЮ ТОВАР ИЗ КОРЗИНЫ ПО ЛИСТУ С НАЙДЕННЫМИ ИНДЕКСАМИ
					for i in IDProductFromCount0:
						StrA = " ".join([str(_) for _ in i])
						i=re.sub("['|(|)|,]","",StrA)
						#bot.send_message(call.message.chat.id,str(i))
						#bot.send_message(call.message.chat.id,i)
						user = (int(i), int(IDOrder))
						cur.execute("DELETE FROM Order_Product WHERE Order_Product.ID_Product = ? and Order_Product.ID_Order = ?;", (user))
						con.commit()
				cur.execute("SELECT Product.Name_Product FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 0 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ?;", (id,))
				tovar = cur.fetchall()


				Str = " ".join([str(_) for _ in tovar])
				tovar = re.sub("['|(|)|,]","",Str)
				if tovar == '':
					bot.send_message(call.message.chat.id,"Кошик порожній")
				else:
					user = (IDOrder)
					cur.execute("UPDATE [Order] SET Status = 1, Date_Order = DATE('now') Where [Order].ID_Order = ?;", (user,))
					con.commit()

					order=(id, 0, "2021-05-02")
					cur.execute("INSERT INTO [Order] (ID_Client, Status, Date_Order) Values (?,?,?);", order)
					con.commit()

					
					cur.execute("SELECT Client.Address FROM Client WHERE Client.ID_Client = ?;", (id,))
					adress = cur.fetchall()
					strr = " ".join([str(_) for _ in adress])
					adress = re.sub("['|(|)|,]","",strr)
					#bot.send_message(call.message.chat.id,adress)

					cur.execute("SELECT Client.Number_Phone FROM Client WHERE Client.ID_Client = ?;", (id,))
					phone = cur.fetchall()
					strr = " ".join([str(_) for _ in phone])
					phone = re.sub("['|(|)|,]","",strr)

					bot.send_message(call.message.chat.id,'Ваше замовлення буде доставленно через два дні на дану адресу:\n '+ adress + '\nвам зателефонують на цей номер телефону:\n '+ phone + '\nОплата налічними при отриманні замовлення або на картку:\n4000 0012 3456 7899\nГарного дня😚 ')

			elif call.data == 'search1':
				msg = bot.send_message(call.message.chat.id, "Введіть назву шуканого товар")
				bot.register_next_step_handler(msg, process_search1_step)
			

			elif call.data == 'search2':
				msg = bot.send_message(call.message.chat.id, "Введіть шуканий тип товару")
				bot.register_next_step_handler(msg, process_search2_step)
			
			elif call.data == 'ZakazOfDate':
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 1
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('1', globalIDClien))
				con.commit()

				cur.execute("SELECT Product.Name_Product FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client;")
				tovar = cur.fetchall()

				Str = " ".join([str(_) for _ in tovar])
				tovar = re.sub("['|(|)|,]","",Str)
				if tovar == '':
					bot.send_message(call.message.chat.id,"Замовлень немає")
				else:
					cur.execute('SELECT DISTINCT [Order].Date_Order FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client ORDER BY [Order].Date_Order;')
					key1 = cur.fetchall()

					kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
					bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Усі замовлення за датами \nОберіть дату:")
			
			elif call.data == 'ZakazOfFIO':
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('1', globalIDClien))
				con.commit()
				globalAllZakaz = 1

				#bot.send_message(call.message.chat.id, "Усі замовлення на цю дату: "+call.data)
				cur.execute("SELECT Product.Name_Product FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client;")
				tovar = cur.fetchall()

				Str = " ".join([str(_) for _ in tovar])
				tovar = re.sub("['|(|)|,]","",Str)
				if tovar == '':
					bot.send_message(call.message.chat.id,"Замовлень немає")
				else:
					cur.execute('SELECT DISTINCT Client.FIO, Client.ID_Client FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client ORDER BY Client.FIO;')
					key1 = cur.fetchall()

					kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
					bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Усі клієнти що робили замовлення\nОберіть клиєнта:")
			
			
			elif call.data == 'ZakazOfFIOSearch':
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				globalAllZakaz = 1
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('1', globalIDClien))
				con.commit()
				#bot.send_message(call.message.chat.id, "Усі замовлення на цю дату: "+call.data)
				cur.execute("SELECT Product.Name_Product FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client;")
				tovar = cur.fetchall()

				Str = " ".join([str(_) for _ in tovar])
				tovar = re.sub("['|(|)|,]","",Str)
				if tovar == '':
					bot.send_message(call.message.chat.id,"Замовлень немає")
				else:
					msg = bot.send_message(call.message.chat.id, "Введіть Прізвище Ім'я клієнта")
					bot.register_next_step_handler(msg, process_searchFIO_step)
				
			
			elif validate(call.data) == True: #Вывод заказов по дате у клиента
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				
				cur.execute("SELECT Client_ID_Product.globalAllZakaz  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				AllZakaz = cur.fetchall()
				St = " ".join([str(_) for _ in AllZakaz])
				AllZakaz=re.sub("['|(|)|,]","",St)
				if int(AllZakaz) == 0:
					bot.send_message(call.message.chat.id, "Усі замовлення на цю дату: "+call.data)
					con = sqlite3.connect('example.db')
					cur = con.cursor()

					cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
					idclient = cur.fetchall()

					#bot.send_message(user_id, idclient)
					#global globalIDClient
					StrA = " ".join([str(_) for _ in idclient])
					globalIDClient=re.sub("['|(|)|,]","",StrA)
					id = int(globalIDClient)

					cur.execute("SELECT Product.Name_Product FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ? and [Order].Date_Order = ?;", (id, call.data))
					tovar = cur.fetchall()

					Str = " ".join([str(_) for _ in tovar])
					tovar = re.sub("['|(|)|,]","",Str)
					if tovar == '':
						bot.send_message(call.message.chat.id,"Зробіть замовлення, щоб побачити його тут!")
					else:
						cur.execute("SELECT DISTINCT [Order].ID_Order FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ? and [Order].Date_Order = ?;", (id, call.data))
						IDOrder = cur.fetchall()

						for j in IDOrder:

							Str = " ".join([str(_) for _ in j])
							j = re.sub("['|(|)|,]","",Str)

							cur.execute("SELECT Product.Price, Order_Product.Count FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ? and [Order].ID_Order = ?;", (id,j))
							korzina = cur.fetchall()
							
							Str = " ".join([str(_) for _ in korzina])
							korzina = re.sub("['|(|)|,]","",Str)

							mas = korzina.split(' ')
							mas2 = []
							mas2 = list(map(float, mas))
							allPrice = 0 
							indexMassum = 0
							
							massum = [] 

							#otv = [] 
							for i in range(len(mas2)):
								if (i+1) % 2 == 0:
									massum.append(mas2[i-1] * mas2[i])
									#bot.send_message(call.message.chat.id,massum[indexMassum])
									allPrice += mas2[i-1] * mas2[i]
									if indexMassum + 1 != (len(mas2) / 2):
										indexMassum += 1

							cur.execute("SELECT Product.Name_Product , Order_Product.Count ,Product.Price, Order_Product.Count * Product.Price  FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ? and [Order].ID_Order = ?;", (id,j))
							korzina = cur.fetchall()
							#bot.send_message(call.message.chat.id, str(korzina))

							#####2 вариант вывода корзины
							Str = " ".join([str(_) for _ in korzina])
							korzina = re.sub("[|']","",Str)
							start = -1
							index = []
							i = 0

							while True:
								start = korzina.find(") (", start + 1)
								if start == -1:
									#bot.send_message(call.message.chat.id, "Не нашел")
									break
								else:
									index.append(start+2)
									#bot.send_message(call.message.chat.id, index[i])
									i += 1

							for x in range(len(index)):
								korzina = korzina[:index[x]-1] + "\n\n" + korzina[index[x]+1:]
							#bot.send_message(call.message.chat.id, korzina)
							start1 = -1
							index1 = []
							t = 0

							while True:
								start1 = korzina.find(".), ", start1 + 1)
								if start1 == -1:
									#bot.send_message(call.message.chat.id, "Не нашел")
									break
								else:
									index1.append(start1+2)
									#bot.send_message(call.message.chat.id, index1[t])
									t += 1

							for x in range(len(index1)):
								korzina = korzina[:index1[x]] + " " + korzina[index1[x]+1:]
							##bot.send_message(call.message.chat.id, korzina)
											
							start2 = -1
							index2 = []
							indexRavno = []
							r = 0

							while True:
								start2 = korzina.find(", ", start2 + 1)
								if start2 == -1:
									#bot.send_message(call.message.chat.id, "Не нашел")
									break
								else:
									if (r + 1) % 2 != 0:
										index2.append(start2)
										#bot.send_message(call.message.chat.id, index2[r])
										r += 1
									else: 
										indexRavno.append(start2)
										r += 1

							for x in range(len(index2)):
								korzina = korzina[:index2[x]] + "X " + korzina[index2[x]+2:]
							##bot.send_message(call.message.chat.id, korzina)

							for x in range(len(indexRavno)):
								korzina = korzina[:indexRavno[x]] + " =" + korzina[indexRavno[x]+2:]

							start3 = -1
							index3 = []
							g = 0

							while True:
								start3 = korzina.find(".)", start3 + 1)
								if start3 == -1:
									#bot.send_message(call.message.chat.id, "Не нашел")
									break
								else:
										index3.append(start3+2)
										g += 1

							for x in range(len(index3)):
								korzina = korzina[:index3[x]] + "\n" + korzina[index3[x]+1:]
							##bot.send_message(call.message.chat.id, korzina)

							Str = re.sub("[(|)]","",korzina)

							cur.execute("SELECT DISTINCT [Order].ID_Order FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ? and [Order].ID_Order = ?;", (id,j))
							number = cur.fetchall()

							Str1 = " ".join([str(_) for _ in number])
							number = re.sub("['|(|)|,]","",Str1)

							cur.execute("SELECT DISTINCT [Order].Date_Order FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ? and [Order].ID_Order = ?;", (id,j))
							date = cur.fetchall()

							Str2 = " ".join([str(_) for _ in date])
							date = re.sub("['|(|)|,]","",Str2)
							

							cur.execute("SELECT DISTINCT Client.FIO FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client and [Order].ID_Order = ?;", (j,))
							fio = cur.fetchall()

							Str2 = " ".join([str(_) for _ in fio])
							fio = re.sub("['|(|)|,]","",Str2)

							cur.execute("SELECT DISTINCT Client.Number_Phone FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client and [Order].ID_Order = ?;", (j,))
							phone = cur.fetchall()

							Str2 = " ".join([str(_) for _ in phone])
							phone = re.sub("['|(|)|,]","",Str2)

							cur.execute("SELECT DISTINCT Client.Address FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client and [Order].ID_Order = ?;", (j,))
							adrress = cur.fetchall()

							Str2 = " ".join([str(_) for _ in adrress])
							adrress = re.sub("['|(|)|,]","",Str2)
							#bot.send_message(call.message.chat.id, "Кошик\n-----\nНазва, кількість, грн")
							#bot.send_message(call.message.chat.id,"Кошик\n-----\nНазва, кількість, грн\n\n" + str(Str) +'\n\nЗагалом: ' + str(allPrice)+"грн\n-----")
							##
							##ВЫВЕСТИ КНОПКИ ДЛЯ УДАЛЕНИЯ КОРЗИНЫ, РЕДАКТИРОВАНИЕ, ОФОРМЛЕНИЯ ЗАКАЗА

							# remove inline buttons
							bot.send_message(call.message.chat.id,"Зомовлення №" + number +"\nКлієнт: "+fio+"\nДата: " + date+"\nНомер телефону: "+phone+"\nАдреса: "+adrress +"\n-----\n" + str(Str) +'\n\nЗагалом: ' + str(allPrice)+"грн\n-----")
				elif int(AllZakaz) == 1:
					bot.send_message(call.message.chat.id, "Усі замовлення на цю дату: "+ call.data)

					con = sqlite3.connect('example.db')
					cur = con.cursor()


					cur.execute("SELECT Product.Name_Product FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client and [Order].Date_Order = ?;", (call.data,))
					tovar = cur.fetchall()

					Str = " ".join([str(_) for _ in tovar])
					tovar = re.sub("['|(|)|,]","",Str)
					if tovar == '':
						bot.send_message(call.message.chat.id,"Зробіть замовлення, щоб побачити його тут!")
					else:
						cur.execute("SELECT DISTINCT [Order].ID_Order FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client and [Order].Date_Order = ?;", (call.data,))
						IDOrder = cur.fetchall()

						for j in IDOrder:

							Str = " ".join([str(_) for _ in j])
							j = re.sub("['|(|)|,]","",Str)

							cur.execute("SELECT Product.Price, Order_Product.Count FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client and [Order].ID_Order = ?;", (j,))
							korzina = cur.fetchall()
							
							Str = " ".join([str(_) for _ in korzina])
							korzina = re.sub("['|(|)|,]","",Str)

							mas = korzina.split(' ')
							mas2 = []
							mas2 = list(map(float, mas))
							allPrice = 0 
							indexMassum = 0
							
							massum = [] 

							#otv = [] 
							for i in range(len(mas2)):
								if (i+1) % 2 == 0:
									massum.append(mas2[i-1] * mas2[i])
									#bot.send_message(call.message.chat.id,massum[indexMassum])
									allPrice += mas2[i-1] * mas2[i]
									if indexMassum + 1 != (len(mas2) / 2):
										indexMassum += 1

							cur.execute("SELECT Product.Name_Product , Order_Product.Count ,Product.Price, Order_Product.Count * Product.Price  FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client and [Order].ID_Order = ?;", (j,))
							korzina = cur.fetchall()
							#bot.send_message(call.message.chat.id, str(korzina))

							#####2 вариант вывода корзины
							Str = " ".join([str(_) for _ in korzina])
							korzina = re.sub("[|']","",Str)
							start = -1
							index = []
							i = 0

							while True:
								start = korzina.find(") (", start + 1)
								if start == -1:
									#bot.send_message(call.message.chat.id, "Не нашел")
									break
								else:
									index.append(start+2)
									#bot.send_message(call.message.chat.id, index[i])
									i += 1

							for x in range(len(index)):
								korzina = korzina[:index[x]-1] + "\n\n" + korzina[index[x]+1:]
							#bot.send_message(call.message.chat.id, korzina)
							start1 = -1
							index1 = []
							t = 0

							while True:
								start1 = korzina.find(".), ", start1 + 1)
								if start1 == -1:
									#bot.send_message(call.message.chat.id, "Не нашел")
									break
								else:
									index1.append(start1+2)
									#bot.send_message(call.message.chat.id, index1[t])
									t += 1

							for x in range(len(index1)):
								korzina = korzina[:index1[x]] + " " + korzina[index1[x]+1:]
							##bot.send_message(call.message.chat.id, korzina)
											
							start2 = -1
							index2 = []
							indexRavno = []
							r = 0

							while True:
								start2 = korzina.find(", ", start2 + 1)
								if start2 == -1:
									#bot.send_message(call.message.chat.id, "Не нашел")
									break
								else:
									if (r + 1) % 2 != 0:
										index2.append(start2)
										#bot.send_message(call.message.chat.id, index2[r])
										r += 1
									else: 
										indexRavno.append(start2)
										r += 1

							for x in range(len(index2)):
								korzina = korzina[:index2[x]] + "X " + korzina[index2[x]+2:]
							##bot.send_message(call.message.chat.id, korzina)

							for x in range(len(indexRavno)):
								korzina = korzina[:indexRavno[x]] + " =" + korzina[indexRavno[x]+2:]

							start3 = -1
							index3 = []
							g = 0

							while True:
								start3 = korzina.find(".)", start3 + 1)
								if start3 == -1:
									#bot.send_message(call.message.chat.id, "Не нашел")
									break
								else:
										index3.append(start3+2)
										g += 1

							for x in range(len(index3)):
								korzina = korzina[:index3[x]] + "\n" + korzina[index3[x]+1:]
							##bot.send_message(call.message.chat.id, korzina)

							Str = re.sub("[(|)]","",korzina)

							cur.execute("SELECT DISTINCT [Order].ID_Order FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client and [Order].ID_Order = ?;", (j,))
							number = cur.fetchall()

							Str1 = " ".join([str(_) for _ in number])
							number = re.sub("['|(|)|,]","",Str1)

							cur.execute("SELECT DISTINCT [Order].Date_Order FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client and [Order].ID_Order = ?;", (j,))
							date = cur.fetchall()

							Str2 = " ".join([str(_) for _ in date])
							date = re.sub("['|(|)|,]","",Str2)

							cur.execute("SELECT DISTINCT Client.ID_Client FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client and [Order].ID_Order = ?;", (j,))
							idclient = cur.fetchall()

							Str2 = " ".join([str(_) for _ in idclient])
							idclient = re.sub("['|(|)|,]","",Str2)

							cur.execute("SELECT DISTINCT Client.FIO FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client and [Order].ID_Order = ?;", (j,))
							fio = cur.fetchall()

							Str2 = " ".join([str(_) for _ in fio])
							fio = re.sub("['|(|)|,]","",Str2)

							cur.execute("SELECT DISTINCT Client.Number_Phone FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client and [Order].ID_Order = ?;", (j,))
							phone = cur.fetchall()

							Str2 = " ".join([str(_) for _ in phone])
							phone = re.sub("['|(|)|,]","",Str2)

							cur.execute("SELECT DISTINCT Client.Address FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client and [Order].ID_Order = ?;", (j,))
							adrress = cur.fetchall()

							Str2 = " ".join([str(_) for _ in adrress])
							adrress = re.sub("['|(|)|,]","",Str2)

							#bot.send_message(call.message.chat.id, "Кошик\n-----\nНазва, кількість, грн")
							#bot.send_message(call.message.chat.id,"Кошик\n-----\nНазва, кількість, грн\n\n" + str(Str) +'\n\nЗагалом: ' + str(allPrice)+"грн\n-----")
							##
							##ВЫВЕСТИ КНОПКИ ДЛЯ УДАЛЕНИЯ КОРЗИНЫ, РЕДАКТИРОВАНИЕ, ОФОРМЛЕНИЯ ЗАКАЗА

							# remove inline buttons
							bot.send_message(call.message.chat.id,"Зомовлення №" + number +"\nКлієнт: "+fio+"\nДата: " + date+"\nНомер телефону: "+phone+"\nАдреса: "+adrress +"\n-----\n" + str(Str) +'\n\nЗагалом: ' + str(allPrice)+"грн\n-----")

				elif int(AllZakaz) == 3:
					bot.send_message(call.message.chat.id, "Усі замовлення на цю дату: ")
					con = sqlite3.connect('example.db')
					cur = con.cursor()

					
					id = int(globalAllZakazFIOID)

					cur.execute("SELECT Product.Name_Product FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ? and [Order].Date_Order = ?;", (id, call.data))
					tovar = cur.fetchall()

					Str = " ".join([str(_) for _ in tovar])
					tovar = re.sub("['|(|)|,]","",Str)
					if tovar == '':
						bot.send_message(call.message.chat.id,"Зробіть замовлення, щоб побачити його тут!")
					else:
						cur.execute("SELECT DISTINCT [Order].ID_Order FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ? and [Order].Date_Order = ?;", (id, call.data))
						IDOrder = cur.fetchall()

						for j in IDOrder:

							Str = " ".join([str(_) for _ in j])
							j = re.sub("['|(|)|,]","",Str)

							cur.execute("SELECT Product.Price, Order_Product.Count FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ? and [Order].ID_Order = ?;", (id,j))
							korzina = cur.fetchall()
							
							Str = " ".join([str(_) for _ in korzina])
							korzina = re.sub("['|(|)|,]","",Str)

							mas = korzina.split(' ')
							mas2 = []
							mas2 = list(map(float, mas))
							allPrice = 0 
							indexMassum = 0
							
							massum = [] 

							#otv = [] 
							for i in range(len(mas2)):
								if (i+1) % 2 == 0:
									massum.append(mas2[i-1] * mas2[i])
									#bot.send_message(call.message.chat.id,massum[indexMassum])
									allPrice += mas2[i-1] * mas2[i]
									if indexMassum + 1 != (len(mas2) / 2):
										indexMassum += 1

							cur.execute("SELECT Product.Name_Product , Order_Product.Count ,Product.Price, Order_Product.Count * Product.Price  FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ? and [Order].ID_Order = ?;", (id,j))
							korzina = cur.fetchall()
							#bot.send_message(call.message.chat.id, str(korzina))

							#####2 вариант вывода корзины
							Str = " ".join([str(_) for _ in korzina])
							korzina = re.sub("[|']","",Str)
							start = -1
							index = []
							i = 0

							while True:
								start = korzina.find(") (", start + 1)
								if start == -1:
									#bot.send_message(call.message.chat.id, "Не нашел")
									break
								else:
									index.append(start+2)
									#bot.send_message(call.message.chat.id, index[i])
									i += 1

							for x in range(len(index)):
								korzina = korzina[:index[x]-1] + "\n\n" + korzina[index[x]+1:]
							#bot.send_message(call.message.chat.id, korzina)
							start1 = -1
							index1 = []
							t = 0

							while True:
								start1 = korzina.find(".), ", start1 + 1)
								if start1 == -1:
									#bot.send_message(call.message.chat.id, "Не нашел")
									break
								else:
									index1.append(start1+2)
									#bot.send_message(call.message.chat.id, index1[t])
									t += 1

							for x in range(len(index1)):
								korzina = korzina[:index1[x]] + " " + korzina[index1[x]+1:]
							##bot.send_message(call.message.chat.id, korzina)
											
							start2 = -1
							index2 = []
							indexRavno = []
							r = 0

							while True:
								start2 = korzina.find(", ", start2 + 1)
								if start2 == -1:
									#bot.send_message(call.message.chat.id, "Не нашел")
									break
								else:
									if (r + 1) % 2 != 0:
										index2.append(start2)
										#bot.send_message(call.message.chat.id, index2[r])
										r += 1
									else: 
										indexRavno.append(start2)
										r += 1

							for x in range(len(index2)):
								korzina = korzina[:index2[x]] + "X " + korzina[index2[x]+2:]
							##bot.send_message(call.message.chat.id, korzina)

							for x in range(len(indexRavno)):
								korzina = korzina[:indexRavno[x]] + " =" + korzina[indexRavno[x]+2:]

							start3 = -1
							index3 = []
							g = 0

							while True:
								start3 = korzina.find(".)", start3 + 1)
								if start3 == -1:
									#bot.send_message(call.message.chat.id, "Не нашел")
									break
								else:
										index3.append(start3+2)
										g += 1

							for x in range(len(index3)):
								korzina = korzina[:index3[x]] + "\n" + korzina[index3[x]+1:]
							##bot.send_message(call.message.chat.id, korzina)

							Str = re.sub("[(|)]","",korzina)

							cur.execute("SELECT DISTINCT [Order].ID_Order FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ? and [Order].ID_Order = ?;", (id,j))
							number = cur.fetchall()

							Str1 = " ".join([str(_) for _ in number])
							number = re.sub("['|(|)|,]","",Str1)

							cur.execute("SELECT DISTINCT [Order].Date_Order FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ? and [Order].ID_Order = ?;", (id,j))
							date = cur.fetchall()

							Str2 = " ".join([str(_) for _ in date])
							date = re.sub("['|(|)|,]","",Str2)

							cur.execute("SELECT DISTINCT Client.ID_Client FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client and [Order].ID_Client = ? and [Order].ID_Order = ?;", (id,j))
							idclient = cur.fetchall()

							Str2 = " ".join([str(_) for _ in idclient])
							idclient = re.sub("['|(|)|,]","",Str2)

							cur.execute("SELECT DISTINCT Client.FIO FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client and [Order].ID_Client = ? and [Order].ID_Order = ?;", (id,j))
							fio = cur.fetchall()

							Str2 = " ".join([str(_) for _ in fio])
							fio = re.sub("['|(|)|,]","",Str2)

							cur.execute("SELECT DISTINCT Client.Number_Phone FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client and [Order].ID_Order = ?;", (j,))
							phone = cur.fetchall()

							Str2 = " ".join([str(_) for _ in phone])
							phone = re.sub("['|(|)|,]","",Str2)

							cur.execute("SELECT DISTINCT Client.Address FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client and [Order].ID_Order = ?;", (j,))
							adrress = cur.fetchall()

							Str2 = " ".join([str(_) for _ in adrress])
							adrress = re.sub("['|(|)|,]","",Str2)

							#bot.send_message(call.message.chat.id, "Кошик\n-----\nНазва, кількість, грн")
							#bot.send_message(call.message.chat.id,"Кошик\n-----\nНазва, кількість, грн\n\n" + str(Str) +'\n\nЗагалом: ' + str(allPrice)+"грн\n-----")
							##
							##ВЫВЕСТИ КНОПКИ ДЛЯ УДАЛЕНИЯ КОРЗИНЫ, РЕДАКТИРОВАНИЕ, ОФОРМЛЕНИЯ ЗАКАЗА

							# remove inline buttons
							bot.send_message(call.message.chat.id,"Зомовлення №" + number +"\nКлієнт: "+fio+"\nДата: " + date+"\nНомер телефону: "+phone+"\nАдреса: "+adrress +"\n-----\n" + str(Str) +'\n\nЗагалом: ' + str(allPrice)+"грн\n-----")


			elif call.data == 'back1':
				send_photo = 0
				#bot.send_message(call.message.chat.id, serc+"1-2")
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				
				cur.execute("SELECT Client_ID_Product.globalsearch  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				serc = cur.fetchall()
				St = " ".join([str(_) for _ in serc])
				serc=re.sub("['|(|)|,]","",St)
				
				if int(serc) == 1:
					con = sqlite3.connect('example.db')
					cur = con.cursor()
					cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
					idclient = cur.fetchall()
					StrA = " ".join([str(_) for _ in idclient])
					globalIDClien=re.sub("['|(|)|,]","",StrA)
					id = int(globalIDClien)
					
					
					cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					send_photo=re.sub("['|(|)|,]","",St)
					if int(send_photo) == 1:
						cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
						ke = cur.fetchall()
						St = " ".join([str(_) for _ in ke])
						ke=re.sub("['|(|)|,]","",St)
						bot.delete_message(call.message.chat.id, ke)
						cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
						con.commit()
					name = str.capitalize(globalsearchName)
					#bot.send_message(call.message.chat.id, serc+"1")
					#cur.execute('SELECT Product.Name_Product, Product.ID_Product FROM Product Where Product.Name_Product LIKE ?;', ('%{}%'.format(name),))
					#key1 = cur.fetchall()

					#kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
					#globalMessengID =bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

				if int(serc) == 2:
			
					#bot.delete_message(call.message.chat.id, globalMessengID.message_id)
					con = sqlite3.connect('example.db')
					cur = con.cursor()
					cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
					idclient = cur.fetchall()
					StrA = " ".join([str(_) for _ in idclient])
					globalIDClien=re.sub("['|(|)|,]","",StrA)
					id = int(globalIDClien)
					
					
					cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					send_photo=re.sub("['|(|)|,]","",St)
					if int(send_photo) == 1:
						cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
						ke = cur.fetchall()
						St = " ".join([str(_) for _ in ke])
						ke=re.sub("['|(|)|,]","",St)
						bot.delete_message(call.message.chat.id, ke)
						cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
						con.commit()
					name = str.capitalize(globalsearchName)
					#bot.send_message(call.message.chat.id, serc+"2")
					#cur.execute('SELECT Product.Name_Product, Product.ID_Product FROM Product, Type_product, Subtype_product Where Product.ID_Subtype = Subtype_product.ID_Subtype and Subtype_product.ID_Type = Type_product.ID_Type and Type_product.Name_Type LIKE ?;', ('%{}%'.format(name),))
					#key1 = cur.fetchall()

					#kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
					#bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Оберіть товар:")

			elif call.data == 'dell':
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()

				StrA = " ".join([str(_) for _ in idclient])
				globalIDClient=re.sub("['|(|)|,]","",StrA)
				Client=(globalIDClient)
				cur.execute("SELECT Client_ID_Product.ID_Product  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClient,))
				ke = cur.fetchall()
				#bot.send_message(call.message.chat.id,str(ke))

				St = " ".join([str(_) for _ in ke])
				ke=re.sub("['|(|)|,]","",St)

				send_photo = 0
				bot.send_message(call.message.chat.id, "Товар видалено")
				TypeProduct=(ke)
				cur.execute("UPDATE Product SET Status = 0 WHERE ID_Product = ?", (TypeProduct,))
				con.commit()
				cur.execute('SELECT [Order].ID_Order FROM Product, [Order], Order_Product Where [Order].ID_Order = Order_Product.ID_Order and Order_Product.ID_Product = Product.ID_Product and Product.Status = 0;')
				key1 = cur.fetchall()
				for x in range(len(key1)):
					Str1 = " ".join([str(_) for _ in key1[x]])
					key = re.sub("['|(|)|,]","",Str1)
					pr = (ke,key)
					cur.execute("DELETE FROM Order_Product WHERE Order_Product.ID_Product = ? and Order_Product.ID_Order = ? ", (ke,key))
					con.commit()
				Str1 = " ".join([str(_) for _ in key1])
				key1 = re.sub("['|(|)|,]","",Str1)
				#bot.send_message(call.message.chat.id, key1)
				
			

			elif call.data == 'fio':#Редактирование ФИО
				msg = bot.send_message(call.message.chat.id, "Введіть Прізвище Ім'я")
				bot.register_next_step_handler(msg, process_EditFIO_step)

			elif call.data == 'address':#Редактирование адресса
				msg = bot.send_message(call.message.chat.id, "Введіть Адресу")
				bot.register_next_step_handler(msg, process_EditAdress_step)

			elif call.data == 'numberPhone':#Редактирование номера телефона
				msg = bot.send_message(call.message.chat.id, "Введіть Номер телефону у форматі:\n+38(***)*******")
				bot.register_next_step_handler(msg, process_EditNumber_step)

			elif call.data == 'redakNameProduct':
				
				msg = bot.send_message(call.message.chat.id, "Введіть нову назву")
				bot.register_next_step_handler(msg, process_NameProduct_step)

			elif call.data == 'redakPriceProduct':
				msg = bot.send_message(call.message.chat.id, "Введіть нову ціну")
				bot.register_next_step_handler(msg, process_PriceProduct_step)

			elif call.data == 'redakDescProduct':

				msg = bot.send_message(call.message.chat.id, "Введіть новий опис")
				bot.register_next_step_handler(msg, process_DescProduct_step)

			elif call.data == 'redakPhotoProduct':
				bot.send_message(call.message.chat.id, "Оберіть зображення")

#
#ВЫВОДИМ ТОВАР ПО IDТОВАРА
#
			elif int(call.data) >= 0:
				con = sqlite3.connect('example.db')
				cur = con.cursor()
				cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
				idclient = cur.fetchall()
				StrA = " ".join([str(_) for _ in idclient])
				globalIDClien=re.sub("['|(|)|,]","",StrA)
				id = int(globalIDClien)
				
				cur.execute("SELECT Client_ID_Product.globalAllZakaz  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
				AllZakaz = cur.fetchall()
				St = " ".join([str(_) for _ in AllZakaz])
				AllZakaz=re.sub("['|(|)|,]","",St)
				if int(AllZakaz) == 0:
					con = sqlite3.connect('example.db')
					cur = con.cursor()

					cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
					idclient = cur.fetchall()
					StrA = " ".join([str(_) for _ in idclient])
					globalIDClien=re.sub("['|(|)|,]","",StrA)
					id = int(globalIDClien)
					
					cur.execute("SELECT Client_ID_Product.send_photo  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					ke = cur.fetchall()
					St = " ".join([str(_) for _ in ke])
					send_photo=re.sub("['|(|)|,]","",St)
					if int(send_photo) == 1:
						cur.execute("SELECT Client_ID_Product.globalMessengID  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
						ke = cur.fetchall()
						St = " ".join([str(_) for _ in ke])
						ke=re.sub("['|(|)|,]","",St)
						bot.delete_message(call.message.chat.id, ke)
						cur.execute("UPDATE Client_ID_Product SET send_photo = 0 WHERE ID_Client = ?",(globalIDClien,))
						con.commit()
					globalIDProduct=int(call.data)
					TypeProduct=(globalIDProduct)
					
					cur.execute("SELECT Product.Name_Product FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
					key2 = cur.fetchall()
					cur.execute("SELECT Product.Price  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
					key3 = cur.fetchall()
					cur.execute("SELECT Product.Photo  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
					key4 = cur.fetchall()
					cur.execute("SELECT Product.Description  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
					key6 = cur.fetchall()
					cur.execute("SELECT Product.Name_Product,Product.Price, Product.Photo  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = ?;", (TypeProduct,))
					key5 = cur.fetchall()

					#bot.send_message(call.message.chat.id, key5.format(n), parse_mode='Markdown')
					#``'Всего:\n{}'.
					StrA = " ".join([str(_) for _ in key2])
					s1=re.sub("['|(|)|,]","",StrA)

					StrB = " ".join([str(_) for _ in key3])
					s2=re.sub("['|(|)|,]","",StrB)

					StrV = " ".join([str(_) for _ in key6])
					s3=re.sub("['|(|)|,]","",StrV)

					StrC = " ".join([str(_) for _ in key4])
					s4=re.sub("['|(|)|,]","",StrC)
	 				#f'{text}\n{img}'
					markup3 = types.InlineKeyboardMarkup(row_width=8)

					lline1 = types.InlineKeyboardButton("✅" + str(s2) + "грн " + str(s1), callback_data='addTOzakaz')

					cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
					idclient = cur.fetchall()

					#bot.send_message(user_id, idclient)
					Str1 = " ".join([str(_) for _ in idclient])
					globalIDClient=re.sub("['|(|)|,]","",Str1)
					id = int(globalIDClient)
					cur.execute("UPDATE Client_ID_Product SET ID_Product = ? WHERE ID_Client = ?",(globalIDProduct, id))
					con.commit()

					cur.execute("SELECT Order_Product.* FROM [Order], Order_Product, Client Where [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 0 and [Order].ID_Client = Client.ID_Client  and [Order].ID_Client = ?;", (id,))
					korzina = cur.fetchall()
					#bot.send_message(call.message.chat.id, korzina)
					Str = " ".join([str(_) for _ in korzina])
					proverka = re.sub("['|(|)|,]","",Str)
					if proverka == "":
						#bot.send_message(call.message.chat.id, proverka) 
						lline2 = types.InlineKeyboardButton("🛍", callback_data='korzina')
					else:
						cur.execute("SELECT Product.Price, Order_Product.Count FROM Product, Order_Product, [Order], Client  WHERE Product.ID_Product = Order_Product.ID_Product and Order_Product.ID_Order = [Order].ID_Order and [Order].Status = 0 and Client.ID_Client = [Order].ID_Client and Client.ID_Client = ?;", (id,))
						cinaANDcount = cur.fetchall()
						Str = " ".join([str(_) for _ in cinaANDcount])
						cinaANDcount = re.sub("['|(|)|,]","",Str)
						allPrice = 0
						#bot.send_message(call.message.chat.id, cinaANDcount)
						mas = cinaANDcount.split(' ')
						mas2 = []
						mas2 = list(map(float, mas))
						#bot.send_message(call.message.chat.id, mas2[0])
						#bot.send_message(call.message.chat.id, mas2[1])
						#bot.send_message(call.message.chat.id, mas2[2])
						#bot.send_message(call.message.chat.id, mas2[3])
						#bot.send_message(call.message.chat.id, len(mas2))
						for i in range(len(mas2)):
							if (i+1) % 2 == 0:
								#bot.send_message(call.message.chat.id, mas2[i-1] * mas2[i])
								allPrice += mas2[i-1] * mas2[i]
						lline2 = types.InlineKeyboardButton(str(allPrice) +"🛍", callback_data='korzina')

					lline3 = types.InlineKeyboardButton("Назад", callback_data='back')
					lline5 = types.InlineKeyboardButton("Назад", callback_data='back1')
					lline4 = types.InlineKeyboardButton("Редагувати назву", callback_data='redakNameProduct')
					lline7 = types.InlineKeyboardButton("Редагувати ціну", callback_data='redakPriceProduct')
					lline8 = types.InlineKeyboardButton("Редагувати опис", callback_data='redakDescProduct')
					lline9 = types.InlineKeyboardButton("Редагувати зображення", callback_data='redakPhotoProduct')
					lline6 = types.InlineKeyboardButton("Удалить", callback_data='dell')
					cur.execute("SELECT Client_ID_Product.globalsearch  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					slsearch = cur.fetchall()
					St = " ".join([str(_) for _ in slsearch])
					slsearch=re.sub("['|(|)|,]","",St)

					cur.execute("SELECT Client_ID_Product.globalDell  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					delle = cur.fetchall()
					St = " ".join([str(_) for _ in delle])
					delle=re.sub("['|(|)|,]","",St)

					cur.execute("SELECT Client_ID_Product.globalRedag  FROM Client_ID_Product, Client Where Client_ID_Product.ID_Client = Client.ID_Client and Client.ID_Client = ?;", (globalIDClien,))
					Redag = cur.fetchall()
					St = " ".join([str(_) for _ in Redag])
					Redag=re.sub("['|(|)|,]","",St)
					if int(slsearch) != 0:
						markup3.add(lline1, lline2)
						markup3.add(lline5)
					elif int(delle) != 0:#удаляєм
						markup3.add(lline6)
						markup3.add(lline3)
					elif int(Redag) != 0:#редактируем
						markup3.add(lline4,lline7)
						markup3.add(lline8,lline9)
						markup3.add(lline3)
					else:
						markup3.add(lline1, lline2)
						markup3.add(lline3)
						send_photo = 1
					globalMessengID = bot.send_photo(call.message.chat.id, open(s4, 'rb'), caption= s1 +"\nЦіна: "+ s2 + "\nОпис: "+s3, parse_mode='Markdown', reply_markup=markup3)
					cur.execute("UPDATE Client_ID_Product SET globalMessengID = ? WHERE ID_Client = ?",(globalMessengID.message_id, id))
					con.commit()
					cur.execute("UPDATE Client_ID_Product SET Send_photo = 1 WHERE ID_Client = ?",(id,))
					con.commit()
				else:
					con = sqlite3.connect('example.db')
					cur = con.cursor()
					globalAllZakaz = 3
					cur.execute('SELECT ID_Client FROM Client WHERE user_id = ?;', (call.message.chat.id,))
					idclient = cur.fetchall()
					StrA = " ".join([str(_) for _ in idclient])
					globalIDClien=re.sub("['|(|)|,]","",StrA)
					id = int(globalIDClien)
					cur.execute("UPDATE Client_ID_Product SET globalAllZakaz = ? WHERE ID_Client = ?",('3', globalIDClien))
					con.commit()
					globalAllZakazFIOID = call.data

					cur.execute("SELECT Product.Name_Product FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client and [Order].ID_Client = ?;",(globalAllZakazFIOID,))
					tovar = cur.fetchall()

					Str = " ".join([str(_) for _ in tovar])
					tovar = re.sub("['|(|)|,]","",Str)
					if tovar == '':
						bot.send_message(call.message.chat.id,"Замовлень немає")
					else:
						cur.execute('SELECT DISTINCT [Order].Date_Order FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client and [Order].ID_Client = ? ORDER BY [Order].Date_Order;',(globalAllZakazFIOID,))
						key1 = cur.fetchall()

						kb_product = Keyboa(items=key1, copy_text_to_callback=True).keyboard
						bot.send_message(chat_id=call.message.chat.id, reply_markup=kb_product, text="Усі замовлення за датами \nОберіть дату:")
				


					#bot.send_message(call.message.chat.id, "Усі замовлення цього клієнта: ")

					#con = sqlite3.connect('example.db')
					#cur = con.cursor()


					#cur.execute("SELECT Product.Name_Product FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client and Client.ID_Client = ?;", (call.data,))
					#tovar = cur.fetchall()

					#Str = " ".join([str(_) for _ in tovar])
					#tovar = re.sub("['|(|)|,]","",Str)
					#if tovar == '':
					#	bot.send_message(call.message.chat.id,"Зробіть замовлення, щоб побачити його тут!")
					#else:
					#	cur.execute("SELECT DISTINCT [Order].ID_Order FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client and Client.ID_Client = ?;", (call.data,))
					#	IDOrder = cur.fetchall()

					#	for j in IDOrder:

					#		Str = " ".join([str(_) for _ in j])
					#		j = re.sub("['|(|)|,]","",Str)

					#		cur.execute("SELECT Product.Price, Order_Product.Count FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client and [Order].ID_Order = ?;", (j,))
					#		korzina = cur.fetchall()
					#		
					#		Str = " ".join([str(_) for _ in korzina])
					#		korzina = re.sub("['|(|)|,]","",Str)

					#		mas = korzina.split(' ')
					#		mas2 = []
					#		mas2 = list(map(float, mas))
					#		allPrice = 0 
					#		indexMassum = 0
							
					##		massum = [] 

					#		#otv = [] 
					#		for i in range(len(mas2)):
					###			if (i+1) % 2 == 0:
					#				massum.append(mas2[i-1] * mas2[i])
					#				#bot.send_message(call.message.chat.id,massum[indexMassum])
					#				allPrice += mas2[i-1] * mas2[i]
					#				if indexMassum + 1 != (len(mas2) / 2):
					#					indexMassum += 1
#
					##		cur.execute("SELECT Product.Name_Product , Order_Product.Count ,Product.Price, Order_Product.Count * Product.Price  FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client and [Order].ID_Order = ?;", (j,))
					##		korzina = cur.fetchall()
					##		#bot.send_message(call.message.chat.id, str(korzina))
##
					##		#####2 вариант вывода корзины
					##		Str = " ".join([str(_) for _ in korzina])
					##		korzina = re.sub("[|']","",Str)
					##		start = -1
					##		index = []
					##		i = 0
##
					##		while True:
					##			start = korzina.find(") (", start + 1)
					##			if start == -1:
									#bot.send_message(call.message.chat.id, "Не нашел")
					##				break
					##			else:
					#				index.append(start+2)
									#bot.send_message(call.message.chat.id, index[i])
					#				i += 1

					#		for x in range(len(index)):
					#			korzina = korzina[:index[x]-1] + "\n\n" + korzina[index[x]+1:]
					#		#bot.send_message(call.message.chat.id, korzina)
					#		start1 = -1
					#		index1 = []
					#		t = 0
#
					#		while True:
					#			start1 = korzina.find(".), ", start1 + 1)
					#			if start1 == -1:
									#bot.send_message(call.message.chat.id, "Не нашел")
					#				break
					#			else:
					#				index1.append(start1+2)
									#bot.send_message(call.message.chat.id, index1[t])
					#				t += 1

						#	for x in range(len(index1)):
						#		korzina = korzina[:index1[x]] + " " + korzina[index1[x]+1:]
							##bot.send_message(call.message.chat.id, korzina)
											
						#	start2 = -1
						#	index2 = []
						#	indexRavno = []
						#	r = 0

							#while True:
							#	start2 = korzina.find(", ", start2 + 1)
							#	if start2 == -1:
									#bot.send_message(call.message.chat.id, "Не нашел")
							#		break
							#	else:
							#		if (r + 1) % 2 != 0:
								#		index2.append(start2)
										#bot.send_message(call.message.chat.id, index2[r])
									#	r += 1
								#	else: 
								#		indexRavno.append(start2)
								#		r += 1

							#for x in range(len(index2)):
							#	korzina = korzina[:index2[x]] + "X " + korzina[index2[x]+2:]
							##bot.send_message(call.message.chat.id, korzina)

							#for x in range(len(indexRavno)):
							#	korzina = korzina[:indexRavno[x]] + " =" + korzina[indexRavno[x]+2:]
#
							#start3 = -1
							#index3 = []
							#g = 0

							#while True:
							#	start3 = korzina.find(".)", start3 + 1)
							#	if start3 == -1:
							#		#bot.send_message(call.message.chat.id, "Не нашел")
							#		break
							#	else:
							#			index3.append(start3+2)
							#			g += 1

							#for x in range(len(index3)):
							#	korzina = korzina[:index3[x]] + "\n" + korzina[index3[x]+1:]
							##bot.send_message(call.message.chat.id, korzina)

							#Str = re.sub("[(|)]","",korzina)

							#cur.execute("SELECT DISTINCT [Order].ID_Order FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client and [Order].ID_Order = ?;", (j,))
							#number = cur.fetchall()

							#Str1 = " ".join([str(_) for _ in number])
							#number = re.sub("['|(|)|,]","",Str1)
#
							#cur.execute("SELECT DISTINCT [Order].Date_Order FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client and [Order].ID_Order = ?;", (j,))
							#date = cur.fetchall()

							#Str2 = " ".join([str(_) for _ in date])
							#date = re.sub("['|(|)|,]","",Str2)

							#cur.execute("SELECT DISTINCT Client.ID_Client FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client and [Order].ID_Order = ?;", (j,))
							###idclient = cur.fetchall()

							##Str2 = " ".join([str(_) for _ in idclient])
							##idclient = re.sub("['|(|)|,]","",Str2)

							##cur.execute("SELECT DISTINCT Client.FIO FROM Product, [Order], Order_Product, Client Where Product.ID_Product = Order_Product.ID_Product and [Order].ID_Order =  Order_Product.ID_Order and [Order].Status = 1 and [Order].ID_Client = Client.ID_Client and [Order].ID_Order = ?;", (j,))
							##fio = cur.fetchall()

							##Str2 = " ".join([str(_) for _ in fio])
							##fio = re.sub("['|(|)|,]","",Str2)

							#bot.send_message(call.message.chat.id, "Кошик\n-----\nНазва, кількість, грн")
							#bot.send_message(call.message.chat.id,"Кошик\n-----\nНазва, кількість, грн\n\n" + str(Str) +'\n\nЗагалом: ' + str(allPrice)+"грн\n-----")
							##
							##ВЫВЕСТИ КНОПКИ ДЛЯ УДАЛЕНИЯ КОРЗИНЫ, РЕДАКТИРОВАНИЕ, ОФОРМЛЕНИЯ ЗАКАЗА

							# remove inline buttons
							#bot.send_message(call.message.chat.id,"Клієнт №"+idclient+" "+fio+"\nЗомовлення №" + number +"  "+ date +"\n-----\n" + str(Str) +'\n\nЗагалом: ' + str(allPrice)+"грн\n-----")




				# remove inline buttons
				#bot.send_message(chat_id=call.message.chat.id, reply_markup=markup3, text="" )

            # show alert
            #bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
               # text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")
		else: bot.send_message(call.message.chat.id, 'Ошибка')			
 
	except Exception as e:
		print(repr(e))

bot.polling(none_stop=True)




#def photoTovar(messageID, Subtype):
#	global globalIDSubtype
#	globalIDSubtype = Subtype
	#bot.send_message(messageID, 'Оберіть фото товару')

#def askAge(message):
#	chat_id = message.chat.id
#	text = message.text
#	msg = bot.send_message(chat_id, 'Спасибо, я запомнил ' + text )	

#def start_handler(message):
#	global globalIDName
#	#msg = bot.send_message(call.message.from_user.id, 'Для создания нового объявления отправь название компании_вакансия\n Например:\n\n Рога и копыта_грузчик')
#	#bot.register_next_step_handler(msg, name_ad(msg))
#	#bot.send_message(call.message.chat.id, msg)
#	chat_id = message.chat.id
#	text = message.text
#	msg = bot.send_message(chat_id, 'Введіть назву товару')
#	bot.register_next_step_handler(msg, askAge)
#	bot.send_message(message.chat.id, msg)
#	globalIDName = msg
#	bot.send_message(message.chat.id, globalIDName)
#def add_pr(message):
#	try:
#		chat_id = message.chat.id
#		global globalIDName
#		#globalIDSubtype
#		globalIDName[chat_id] = LI#ST(message.text)
#		#markup = types.ReplyKeyboardRemove(selective=False)
#		if message.text != 'Отмена':
#			bot.send_message(chat_id, f'Условно добавил {message.text}\n/list')
#			bot.send_message(chat_id, globalIDName)
#		else:
#			bot.send_message(chat_id, 'Отмена!')
#	except Exception as e:
#		print(str(e))
#def hello(message):
#	open('problem.txt', 'w').write(message.chat.id + ' | ' + message.text + '||')
#	bot.send_message(message.chat.id, 'Thank you!')
#	bot.send_message(ADMIN_ID, message.chat.id + ' | ' + message.text)
#call.message.text = 'Назва товару'
#call_message = call.message
#sent = bot.send_message(call.message.chat.id, 'Введіть назву товару')
#bot.register_next_step_handler(sent, hello)
#start_handler()
#bot.register_next_step_handler()
#msg = bot.send_message(call.message.chat.id, f'Введите название продукта')
#msg = '0'
#globalIDName = bot.register_next_step_handler(msg, call.message.text)
#bot.send_message(message.chat.id, call.message.text)
#bot.send_message(message.chat.id, globalIDName)
#bot.send_message(message.chat.id, "Введіть назву товару")
#globalIDName = input('Введіть назву товару')
#bot.send_message(message.chat.id, globalIDName)
#globalIDName = str(message.chet.id)
#bot.send_message(message.chat.id, globalIDName)
#savedata = {}
#globalIDName = 0 #подтип товара
#savedata[str(message.chet.id) + 'name'] = 'wait'
#f = open('data.txt', 'a')
#f.write(message.chat.id + 'name' = savedata[str(message.chet.id) + 'name'])
#f.close()
#bot.send_message(message.chat.id, 'Хорошо, запомнил')
				#cur.execute("SELECT * FROM Client WHERE user_id = 0;")
				
				#cur.execute("SELECT COUNT(*) FROM Product where ID_Subtype = 0;")
				#cur.execute("SELECT Product.ID_Product FROM Product, Subtype_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 0;")
				#count = cur.fetchall()
				#int(count)
				#key1 = {} 
				#key2 = {} 
				#key3 = {}
				#product = ()

				#for i in range(3):
					#cur.execute("SELECT Product.Name_Product FROM Product, Subtype_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 0;")
					#key1[i] = cur.fetchall()
					#cur.execute("SELECT Product.ID_Product FROM Product, Subtype_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 0;")
					#key2[i] = cur.fetchall()
					#bot.send_message(call.message.chat.id, key)


				#cur.execute("SELECT Product.Name_Product FROM Product, Subtype_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 0;")
				#key2 = cur.fetchall()
				#cur.execute("SELECT Product.Price FROM Product, Subtype_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 0;")
				#key3 = cur.fetchall()
				#cur.execute("SELECT Product.Photo FROM Product, Subtype_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 0;")
				#key4 = cur.fetchall()
				
				#cur.execute("SELECT Product.Price FROM Product, Subtype_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 0;")
				#key3 = cur.fetchall()
				#cur.execute("SELECT Product.ID_Product FROM Product, Subtype_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 0;")
				#key2 = cur.fetchall()
				#callback_data='prot_1'				
				#if len(data) > 4096:
					#for x in range(0, len(report), 4096):
						#bot.send_message(call.message.chat.id, '{}'.format(report[x:x + 4096]))
				#else:
				#bot.send_message(call.message.chat.id, '{}'.format(key2), '{}'.format(key3), '{}'.format(key4))




				#product = key1 + key2
				#bot.send_message(call.message.chat.id, product)
				#tuple(product)
				#bot.send_message(call.message.chat.id, product)
				#bot.send_message(call.message.chat.id, key1[0])
				#bot.send_message(call.message.chat.id, key2[0])
				#bot.send_message(call.message.chat.id, key1[1])
				#bot.send_message(call.message.chat.id, key2[1])
				#bot.send_message(call.message.chat.id, product)
				#sum(itertools.chain.from_iterable(count))
				#sum(map(sum, count))

				#for i in range(2):
					#if i % 2 == 0:
						#list.extend(key1[i-1],key1[i])
						#list.remove(key1[i])

				#bot.send_message(call.message.chat.id, key1[0:2])
				#bot.send_message(call.message.chat.id, key2[0:2])
				#bot.send_message(call.message.chat.id, product[2])
				#bot.send_message(call.message.chat.id, product['2'])
				#bot.send_message(call.message.chat.id, product['0'])
				#bot.send_message(call.message.chat.id, product['1'])
				#bot.send_message(call.message.chat.id, key1[0])
				#bot.send_message(call.message.chat.id, key2[0])
				#bot.send_message(call.message.chat.id, key3[0])
				#bot.send_message(call.message.chat.id, product)
 
				
				#cur.execute("SELECT * FROM PRODUCT JOIN SUBTYPE_PRODUCT ON ID_SUBTYPE.PRODUCT = ID_TYPE.SUBTYPE_PRODUCT WHERE ID_SUBTYPE.SUBTYPE_PRODUC = " i ";")
				
				#print(count)
				#bot.send_message(call.message.chat.id, key[1]) 
				#product = [{"banana": '101'}, {"coconut": "102"}, 
				#{"orange": "103"},{"peach": "104"}, {"apricot": "105"}, 
				#{"apple": "106"}, {"pineapple": "107"}, {"avocado": "108"}, {"melon": "109"},]



				#user_data[zapros_name_product] = zapros_id
				

				#kb_cities = Keyboa(
				#items=["Moscow", "London", "Tokyo", ],
				#front_marker="&city=",
				#back_marker="$"
				#).keyboard
				#bot.send_message(call.message.chat.id, product) 
				#bot.send_message(call.message.chat.id, s1 +"\nЦіна: "+ s2 + "\nОпис: "+s3 + "\nФото: "+ s4, parse_mode='Markdown')
				#bot.send_photo(call.message.chat.id, open(s4, 'rb'))
				#bot.send_message(call.message.chat.id,'{}'.format(key3), parse_mode='Markdown')
				#bot.send_message(call.message.chat.id,'{}'.format(key4), parse_mode='Markdown')
				#bot.send_message(call.message.chat.id,'{}'.format(key3), parse_mode='Markdown')
				#bot.send_message(call.message.chat.id, '{}'.format(key4), parse_mode='Markdown')
				#bot.send_message(call.message.chat.id, "юху1")

#SELECT * FROM Client WHERE user_id = 0
#elif call.data == '11':
				#con = sqlite3.connect('example.db')
				#cur = con.cursor()
				#cur.execute("SELECT Product.Name_Product FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = 11;")
				#key2 = cur.fetchall()
				#cur.execute("SELECT Product.Price  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = 11;")
				#key3 = cur.fetchall()
				#cur.execute("SELECT Product.Photo  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = 11;")
				#key4 = cur.fetchall()
				#cur.execute("SELECT Product.Description  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = 11;")
				#key6 = cur.fetchall()
				#cur.execute("SELECT Product.Name_Product,Product.Price, Product.Photo  FROM Product, Subtype_Product, Type_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Type = Type_Product.ID_Type and Product.ID_Product = 11;")
				#key5 = cur.fetchall()

				#bot.send_message(call.message.chat.id, key5.format(n), parse_mode='Markdown')
				#``'Всего:\n{}'.
				#StrA = " ".join([str(_) for _ in key2])
				#s1=re.sub("['|(|)|,]","",StrA)

				#StrB = " ".join([str(_) for _ in key3])
				#s2=re.sub("['|(|)|,]","",StrB)

				#StrV = " ".join([str(_) for _ in key6])
				#s3=re.sub("['|(|)|,]","",StrV)

				#StrC = " ".join([str(_) for _ in key4])
				#s4=re.sub("['|(|)|,]","",StrC)
 				#f'{text}\n{img}'
				#bot.send_photo(call.message.chat.id, open(s4, 'rb'), caption= s1 +"\nЦіна: "+ s2 + "\nОпис: "+s3, parse_mode='Markdown')

			#bot.send_message(message.chat.id, 'Введіть назву товару')
			#name = message.chat.id.text
			#bot.send_message(message.chat.id, message.chat.id.text)

			#con = sqlite3.connect('example.db')
			#cur = con.cursor()
			#tovar=('Протеїн', globalIDSubtype, '1500', 'Крутой очень', src)
			#cur.execute("INSERT INTO Product (Name_Product, ID_Subtype, Price, Description, Photo) Values (?,?,?,?,?);", tovar)
			#con.commit()

				#cur.execute("SELECT Product.ID_Product FROM Product, Subtype_Product Where Product.ID_Subtype = Subtype_Product.ID_Subtype and Subtype_Product.ID_Subtype = 0;")
				#key2 = cur.fetchall()
				#StrA = " ".join([str(_) for _ in key2])
				#globalIDProduct=re.sub("['|(|)|,]","",StrA)

#####1 вариант вывода корзины
				#Str = " ".join([str(_) for _ in korzina])
				#korzina = re.sub("['|(|)|,]","",Str)
				#start = -1
				#index = []
				#i = 0

				#while True:
					#start = korzina.find(".0", start+1)
					#if start == -1:
						#break
					#else:
						#index.append(start+2)
						
						#i += 1

				#korzinaIzm = korzina
				
				#for x in range(len(index)):
					#korzina = korzina[:index[x]-1] + "\n\n" + korzina[index[x]+1:]
				#bot.send_message(call.message.chat.id, "Кошик\n-----\nНазва, кількість, грн")
				#bot.send_message(call.message.chat.id,"Кошик\n-----\nНазва, кількість, грн\n" + str(korzina) +'\nЗагалом: ' + str(allPrice)+"грн\n-----")


					#bot.send_message(call.message.chat.id, index[i])
					#Str = " ".join([str(_) for _ in korzina])
					#word[:position - 1] + '.' + word[position:]
					#bot.send_message(call.message.chat.id,index[x])
					
					#korzina = korzina[:index[x]] + "\n\n"
					#korzinaIzm = korzina[:index + 'X' + korzina[index:]
				#bot.send_message(call.message.chat.id,len(index))	
				#bot.send_message(call.message.chat.id,korzinaIzm)
				#Str = korzina.replace('.0', ' x')
				#korzina = Str.replace(' ', ' -')
				#bot.send_message(call.message.chat.id,korzina)
								#for i in range(indexMassum):
					#bot.send_message(call.message.chat.id, str(spisok_tovar[i])+"  "+ mas[i] +"  " +str(massum[i]))
			

				#mas = Str.split('-')
