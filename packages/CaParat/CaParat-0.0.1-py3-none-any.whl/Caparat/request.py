import requests as req
import json

def GetUser(username:str):
	url = "https://www.aparat.com/etc/api/profile/username/"+username

	with req.get(url) as res:
		data = json.loads(str(res.text))

	return data["profile"]

def GetVideo(id:str):
	url = "https://www.aparat.com/etc/api/video/videohash/"+id

	with req.get(url) as res:
		data = json.loads(str(res.text))

	return data["video"]