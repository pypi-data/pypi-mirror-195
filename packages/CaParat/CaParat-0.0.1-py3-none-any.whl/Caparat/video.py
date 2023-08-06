from wget import download
from .requests import GetVideo

class Video:
	def __init__(self, video_id:str):
		data = GetVideo(video_id)
		self.title = data["title"]
		self.int_id = data["id"]
		self.id = video_id
		self.poster = data["big_poster"]
		self.upload_at = data["create_date"]
		self.upload_at_fa = data["sdate"]
		self.tags = data["tags"]
		self.tag_str = data["tag_str"]
		self.cat_name = data["cat_name"]
		self.cat_name_en = data["cat_name_en"]
		self.like_cnt = data["like_cnt"]
		self.data = data


	def download(self, path:str="./"):
		download(self.data, path)

	def __str__(self):
		return self.title + " - " + self.id