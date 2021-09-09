import asyncio
import websockets
import csv
import pymysql
import json

from time import sleep

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

# async def accept(websocket, path):
# 	i = 0
# 	while ( i < len(data) ):
# 		# await websocket.send(str(data[i][0]) + " / " + str(data[i][1]) + " / " + str(data[i][2]))
# 		await websocket.send(str(data[i]))
# 		i += 1
# 		await asyncio.sleep(1)

async def accept(websocket, path):
	while True:
		print("serverf running")
		# 클라이언트로부터 메시지를 대기한다.
		try:
			data = await websocket.recv()
			if (data != ""):

				print("receive :" + data + ":")
				# select p.id, p.text, p.price, p.link, s.sales_price from items as p join sales as son s.sales_id = p.id;
				# sql = "select * from items where text regexp \'" + data +"\';"
				sql = "select p.id, p.text, p.price, p.link, s.sales_price from (select * from items where text regexp \'" + data +"\') as p left join sales as s on s.sales_id = p.id;"
				print(sql)

				cursor.execute(sql)
				result = cursor.fetchall()
				toSend = ""

				for x in result:
					toSend += str(x).replace("None", "0") + "\n"

				print(toSend)

				await websocket.send(toSend)

		except Exception as e:
			print(e)
			break

start_server = websockets.serve(accept, "localhost", 9998)
print("hello?")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()


