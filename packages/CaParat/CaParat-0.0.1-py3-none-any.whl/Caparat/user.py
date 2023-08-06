from .requests import GetUser

class User:
	def __init__(self, userid:str):
		data = GetUser(userid)
		self.profile_url = data["pic_b"]
		self.name = data["name"]
		self.video_cnt = int(data["video_cnt"])
		self.following_cnt = int(data["follower_cnt"])
		self.followed_cnt = int(data["followed_cnt"])
		self.facebook = data["facebook"]
		self.twitter = data["twitter"]
		self.cloob = data["cloob"]
		has_live = False
		if data["has_live"] == "yes":
			has_live = True
		self.has_live = has_live

	def __str__(self):
		return self.name