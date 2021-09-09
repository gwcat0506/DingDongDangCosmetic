import pymysql
import sys
import chatBotModel
import requests
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater
import json
import threading
import time
import requests

token = "1969083875:AAGAuhWR-pdHYVvAmFbLPnYuyVP3fusWdrk"

priceDB = pymysql.connect(
    user='root', 
    passwd='3840', 
    host='127.0.0.1', 
    db='oliveDB', 
    charset='utf8',
    autocommit=True
)

cursor = priceDB.cursor(pymysql.cursors.DictCursor)
cursor.execute("set names utf8")

def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

def check_set(bot, args):
	chatID = str(bot.message.chat.id)
	itemID = args.args[0]

	sql = "select * from sales where sales_id=\'" + itemID +"\';"
	cursor.execute(sql)
	result = cursor.fetchall()

	try:
		sql = "update notifications set item=\'" + itemID + "\', curr_price="+ str(result[0]['sales_price']) + " where sub_id = \'" + chatID + "\';"	
		cursor.execute(sql)	
	
	except:
		sql = "insert into notifications (sub_id, item, curr_price) values (\'" + chatID + "\', \'" + itemID + "\', " + str(result[0]['sales_price']) + ");"
		cursor.execute(sql)

	priceDB.commit()

	sql = "select * from items where id=\'" + itemID +"\';"
	cursor.execute(sql)
	result = cursor.fetchall()

	pricingBot.sendMessage(bot.message.chat.id, "상품 " + result[0]['text'] + "의 알림 등록이 완료 되었습니다.")

def check_start(bot, args):
	chatID = str(bot.message.chat.id)
	
	temp = args.args[0].split("_")
	itemID = temp[0]
	print(itemID)
	# itemID = args.args[0]

	sql = "select * from sales where sales_id=\'" + itemID +"\';"
	cursor.execute(sql)
	result = cursor.fetchall()
	try:
		sql = "insert into notifications (sub_id, item, curr_price) values (\'" + chatID + "\', \'" + itemID + "\', " + str(result[0]['sales_price']) + ");"
		cursor.execute(sql)	
	
	except:
		sql = "update notifications set item=\'" + itemID + "\', curr_price="+ str(result[0]['sales_price']) + " where sub_id = \'" + chatID + "\';"	
		cursor.execute(sql)
	priceDB.commit()

	sql = "select * from items where id=\'" + itemID +"\';"
	cursor.execute(sql)
	result = cursor.fetchall()

	pricingBot.sendMessage(bot.message.chat.id, "상품 " + result[0]['text'] + "의 알림 등록이 완료 되었습니다.")

	t = threading.Thread(target=watch, args=(bot.message.chat.id,))
	t.start()


def check_sales_change(item_id):
	try:
		sql = "select * from sales where sales_id=\'" + item_id +"\';"

		cursor.execute(sql)
		notification_request_item = cursor.fetchall()[0]
		print(notification_request_item)
		return notification_request_item['sales_price']
	except:
		print("check_sales_change")

def watch(id):
	while True: 
		sql = "select * from notifications where sub_id=\'" + str(id) +"\';"
		cursor.execute(sql)
		userData = cursor.fetchall()[0]
		notification_request_item = userData['item']

		current_sales_price = check_sales_change(notification_request_item)

		if ( userData['curr_price'] > current_sales_price ):
			sql = "update notifications set curr_price="+ str(current_sales_price) + " where sub_id = \'" + str(id) + "\';"	
			print(sql)
			cursor.execute(sql)
			priceDB.commit()

			sql = "select * from items where id=\'" + notification_request_item +"\';"
			cursor.execute(sql)
			getText = cursor.fetchall()[0]['text']

			pricingBot.sendMessage(id, "설정해둔 상품인 [" + getText + "] 이(가) 현재 " + str(current_sales_price) + "원으로 할인을 시작하였습니다.")
		elif (userData['curr_price'] < current_sales_price):
			sql = "update notifications set curr_price="+ str(current_sales_price) + " where sub_id = \'" + str(id) + "\';"	
			print(sql)
			cursor.execute(sql)
			priceDB.commit()

		time.sleep(1)





def callback_get(bot, update):
    if bot.callback_query.data=="yes":
        manager_order(bot.callback_query.message.chat.id)
    elif bot.callback_query.data=="no":
        pricingBot.sendMessage(bot.callback_query.message.chat.id, "다음 기회에..")







def manager_order(id):
    try:
        comment = "주문 정보는 다음과 같습니다.\n어쩌구저쩌구.."
        pricingBot.sendMessage(id, comment)

    except:
        print("error from manager_order")

def text(bot, update):
    if bot.message.reply_to_message is not None:
        complete_order(bot.message.chat.id, bot.message.reply_to_message.text, bot.message.text)
    else:
        pricingBot.sendMessage(bot.message.chat.id, "환영합니다")

def complete_order(id, reply_text, text):
    try:
        comment = "reply_text와 text를 사용해서 보내고 싶은 메세지를 보내주세요."        
        pricingBot.sendMessage(id, comment)

    except:
        print("error from complete_order")

def error(bot, update):
    """Log Errors caused by Updates."""
    # logger.warning('Update "%s" caused error "%s"', bot, update.error)

def hi(bot, args):
	pricingBot.sendMessage(bot.message.chat.id, "hi")


if __name__ == '__main__':
	pricingBot = chatBotModel.pricingBot()

	pricingBot.add_handler('hi', hi)
	pricingBot.add_handler('set', check_set)
	pricingBot.add_handler('start', check_start)
	pricingBot.add_query_handler(callback_get)
	pricingBot.add_message_handler(text)
	pricingBot.add_error_handler(error)
	pricingBot.start()
