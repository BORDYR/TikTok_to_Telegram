'''Scraptic video downloader'''
import requests
import urllib
import os
import json

def download_last_liked(logger):
	sec_uid = os.environ['TTaccSecUid']
	RapidAPI_key = os.environ['ScrapticApiKey']
		# api-endpoint
	URL = 'https://scraptik.p.rapidapi.com/user-likes'

	# defining a params dict for the parameters to be sent to the API
	PARAMS = {
	    'user_id': sec_uid,
	    'count': '50',
	    'max_time': '0'
	  }
	HEADERS = {
	    'X-RapidAPI-Key': RapidAPI_key,
	    'X-RapidAPI-Host': 'scraptik.p.rapidapi.com'
	  }
	 

	with open('config.json', 'r', encoding='utf-8') as f:
		config = json.load(f)
	last_video_id = config['last_video_id']

	TTaccSecUid = os.environ['TTaccSecUid']
	i=0
	try:
		r = requests.get(url = URL, params = PARAMS, headers=HEADERS)
		response = r.json()
		#updated_last_video_id = response['aweme_list'][0]['aweme_id']
		updated_last_video_id = last_video_id
		config['last_video_id'] = updated_last_video_id

		with open('config.json', 'w', encoding='utf-8') as f:
			json.dump(config, f, ensure_ascii=False, indent=4)

		os.environ['last_video_id'] = str(updated_last_video_id)


		#print("Getting next items ", cursor)
		logger.info(f"Last videoID is {last_video_id}")

		for item in response['aweme_list']:
			#print(item.get('video').get('downloadAddr'))
			if not 'image_post_info' in item.keys():

				download_addr = item['video']['download_addr']['url_list'][2]
				videoId = item['aweme_id']
				videoId_int = int(videoId)
				if int(videoId_int) != int(last_video_id):
				#if videoId_int > last_video_id:
					#my_tt_videos.append(item.get('video').get('downloadAddr'))
					i+=1
					print(f'i = {i}')
					print(f'Downloadind video {videoId_int}')

					try:
						urllib.request.urlretrieve(download_addr, f'videos/video_{videoId}.mp4')
						updated_last_video_id = videoId
					except Exception as e:
						print(f'Failed to download video {videoId}')
					#last_video_id = videoId_int
				else:
					logger.info(f'{i} videos downloaded; updated_last_video_id={updated_last_video_id}')
					break

		config['last_video_id'] = updated_last_video_id
		with open('config.json', 'w', encoding='utf-8') as f:
			json.dump(config, f, ensure_ascii=False, indent=4)

	except Exception as e:
		logger.error(e)
		#print(e, e.field)


