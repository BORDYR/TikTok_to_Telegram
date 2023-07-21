#!/usr/bin/python3

# TTtoTG saver tool for automatic upload your liked TikToks to the telegram channel
"""
* You need to create and specify your Tikapi token, tg_bot_api token, your tg_channel name
	and your Tiktok account secUid in the .env file with corresponding format:
	 token = "<token>"
	 channel = "<channel>"
	 TikApiKey = "<TikApiKey>"
	 TTaccSecUid = "<TTaccSecUid>"
* For now you also wholud specify the Video_id for the latest video to download
"""

import os
from os import listdir
from os.path import isfile, join
import shutil
import urllib.request
import requests
import time
import json
import logging
from dotenv import load_dotenv

import telegram

from tqdm import tqdm

from logger_config import LOGGING_CONFIG

from scraptik_downloader import download_last_liked

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('TTtoTG_logger')


class MyBot():
	def __init__(self, bot_token, channel_name):
		self.token=bot_token
		self.base = 'https://api.telegram.org'
		self.channel_name = channel_name
		self.bot = telegram.Bot(bot_token)
		self.videos_path = 'videos'

	def getME(self):
		return requests.get(self.base+'/bot'+self.token+'/getME').text

	def get_downloaded_videos_list(self):
		return sorted(listdir('videos/'))

	def uploadVideo(self, filepath):
		self.bot.send_video(self.channel_name, open(filepath, 'rb'))

	def uploadVideoList(self,):
		"""
		Telegram API restrict for not more than 20 uploads per minute
		"""
		start = time.time()
		upload_counter = 0

		if len(self.get_downloaded_videos_list()) == 0:
			logger.info("No video to upload")
			return False

		for video in tqdm(self.get_downloaded_videos_list()):

			self.uploadVideo(os.path.join(self.videos_path, video))

			#last_upload_time = time.time()
			upload_counter += 1
			if upload_counter >= 15 :
				batch_time = time.time() - start
				time.sleep(max(0, 60 - batch_time + 1)) # waiting if needed
				start = time.time()
				upload_counter = 0
		logger.info(f"{len(self.get_downloaded_videos_list())} videos has been uploaded")

		return True


	def clear_videos_dir(self, folder):
		for filename in os.listdir(folder):
			file_path = os.path.join(folder, filename)
			try:
				if os.path.isfile(file_path) or os.path.islink(file_path):
					os.unlink(file_path)
				elif os.path.isdir(file_path):
					shutil.rmtree(file_path)
			except Exception as e:
				logger.error('Failed to delete %s. Reason: %s' % (file_path, e))


	def run(self,):
		self.uploadVideoList()
		self.clear_videos_dir(self.videos_path)


def run():
	load_dotenv()

	#TikApiKey = os.environ['TikApiKey']
	#API = TikAPI(str(TikApiKey))
	download_last_liked(logger)

	token = os.environ.get("token")
	print(token)
	channel_name = os.environ.get("channel")
	print(channel_name)
	BOT = MyBot(token, channel_name)
	BOT.run()


if __name__ == "__main__":
	run()