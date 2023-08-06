from .user import User
from .video import Video

class Aparat:
	def get_user(self, user_id:str):
		return User(user_id)

	def get_video(self, video_id:str):
		return Video(video_id)