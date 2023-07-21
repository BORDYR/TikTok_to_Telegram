
def download_last_liked(api):

	with open('config.json', 'r', encoding='utf-8') as f:
		config = json.load(f)
	last_video_id = config['last_video_id']

	TTaccSecUid = os.environ['TTaccSecUid']
	i=0
	try:
		response = api.public.likes(
			secUid = TTaccSecUid)

		updated_last_video_id = response.json().get('itemList')[0].get('video').get('id')
		config['last_video_id'] = updated_last_video_id

		with open('config.json', 'w', encoding='utf-8') as f:
			json.dump(config, f, ensure_ascii=False, indent=4)

		os.environ['last_video_id'] = str(updated_last_video_id)

		while response:
			cursor = response.json().get('cursor')
			#print("Getting next items ", cursor)
			logger.info(f"Last videoID is {last_video_id}")

			for item in response.json().get('itemList'):
				#print(item.get('video').get('downloadAddr'))
				download_addr = item.get('video').get('downloadAddr')
				videoId = item.get('video').get('id')
				videoId_int = int(videoId)
				if int(videoId_int) != int(last_video_id):
				#if videoId_int > last_video_id:
					#my_tt_videos.append(item.get('video').get('downloadAddr'))
					i+=1
					print(f'i = {i}')
					print(f'Downloadind video {videoId_int}')
					print(f'by addr {download_addr}')

					try:
						urllib.request.urlretrieve(download_addr, f'videos/video_{videoId}.mp4')
					except ResponseException as e:
						print('mdaa')
					#last_video_id = videoId_int
				else:
					logger.info(f'{i} videos downloaded; updated_last_video_id={updated_last_video_id}')
					return updated_last_video_id

			response = response.next_items()

	except ValidationException as e:
		logger.error(e)
		#print(e, e.field)

	except ResponseException as e:
		logger.error(e)
		#print(e, e.response.status_code)
