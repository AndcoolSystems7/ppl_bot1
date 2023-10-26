from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS, cross_origin
import random
from threading import Thread
import numpy as np
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import pickle
import os
import asyncio
from aiogram.types import UserProfilePhotos
from PIL import Image
import base64
from io import BytesIO
import emoji

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

app = Flask(__name__)
api = Api(app)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
notAlowed = {
	"status": "error",
	"message": "The method is not allowed for the requested URL."
    }
    
global bot
global loop


def findBadge(list, id1):
    for num, i in enumerate(list):
        if int(i[0]) == int(id1):
            return num
    return -1


async def load(id_):
	global bot
	user_profile_photo: UserProfilePhotos = await bot.get_user_profile_photos(id_)
	member = await bot.get_chat_member(int(id_), int(id_))
	first = (
        str(member.user.first_name)
        if member.user.first_name != None
		else ""
		)
	kast_a = " " if first != "" else ""
	last = (
			(kast_a + str(member.user.last_name))
			if member.user.last_name != None
			else ""
	)
	name = first + last
	new_name = "".join(char for char in name if not emoji.is_emoji(char))
	new_name = new_name if new_name[-1] != " " else new_name[:-1]

	if len(user_profile_photo.photos) > 0:
		file = await bot.get_file(user_profile_photo.photos[0][0].file_id)
		await bot.download_file(file.file_path, f'api/{id_}.png')
		usr_img = Image.open(f'api/{id_}.png').convert("RGBA")
		new_image = usr_img.resize((100, 100))
		os.remove(f'api/{id_}.png')
		
		buffered = BytesIO()
		new_image.save(buffered, format="PNG")
		img_str = base64.b64encode(buffered.getvalue())

		
		return img_str, new_name, member.user.username
	else:
		return None, new_name, member.user.username
	
class Quote(Resource):
	@limiter.limit("10/second")
	def get(self, id="0", method=None):
		if method == None: return "Welcome to pplbandagebot api", 200

		if method == "logout": 
			if id != "0": 
				if os.path.isfile("data/sessions.sess"):
					with open('data/sessions.sess', 'rb') as fp:
						dict = pickle.load(fp)
				else: dict = {}
				for x in dict:
					if dict[x] == id:
						dict.pop(x)
						with open('data/sessions.sess', 'wb') as fp:
							pickle.dump(dict, fp)
						return {"status": "success"}, 200
				return {"status": "error", "message": "User not found"}, 404
			

			else: return notAlowed, 405
		return notAlowed, 405


	def post(self, id="0", method=None):
		if method == "login":
			if id != "0": return notAlowed, 405

			parser = reqparse.RequestParser()
			parser.add_argument("oauth-token")
			params = parser.parse_args()


			if os.path.isfile("data/sessions.sess"):
				with open('data/sessions.sess', 'rb') as fp:
					dict = pickle.load(fp)
			else: dict = {}

			for x in dict:
				if str(dict[x]) == str(params["oauth-token"]):
					return {"status": "success", "token": dict[x]}, 200
			return {"status": "error", "message": "User not found"}, 404
		
		if method == "load": 
			parser = reqparse.RequestParser()
			parser.add_argument("oauth-token")
			params = parser.parse_args()
			
			if os.path.isfile("data/sessions.sess"):
				with open('data/sessions.sess', 'rb') as fp:
					dict = pickle.load(fp)
			else: dict = {}
			for x in dict:
				if str(dict[x]) == str(params["oauth-token"]):
					global loop
					future = asyncio.run_coroutine_threadsafe(load(x), loop)
					photo = str(future.result()[0].decode("utf-8") if future.result()[0] != None else None)

					donateList_npy = np.load("data/donations.npy")
					dlist = donateList_npy.tolist()
					balance = 0
						
					for xx in range(len(dlist)):
						if int(dlist[xx][2]) == int(x):
							name = dlist[xx][0]
							balance = dlist[xx][1]
							balance_max = dlist[xx][3]
							break

					badgesListn = np.load("data/badges.npy")
					badgesList = badgesListn.tolist()

					badgeId = findBadge(badgesList, int(x))
					emoji1 = badgesList[badgeId][1] if badgeId != -1 else ""
								
					return {"status": "success",
	      					"balance": balance,
							"badge": emoji1,
	      					"name": str(future.result()[1]),
						    "username": str(future.result()[2]),
							"data": photo}, 200
			return {"status": "error", "message": "User not found"}, 404
		return notAlowed, 405

    
api.add_resource(Quote, 
                 "/", 
                 "/<string:method>", 
                 "/<string:method>/", 
                 "/<string:method>/<string:id>")

def run():
  app.run(host='0.0.0.0', port=8080)

def keep_alive(bot_, loop_):
    global bot
    global loop
    bot = bot_
    loop = loop_
    t = Thread(target=run)
    t.start()

