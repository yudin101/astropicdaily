import requests
import tweepy
import io
import keys

auth = tweepy.OAuth1UserHandler(keys.API_KEY, keys.API_SECRET, keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

client = tweepy.Client(keys.BEARER_TOKEN, keys.API_KEY, keys.API_SECRET, keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET)

url = f"https://api.nasa.gov/planetary/apod?api_key={keys.APOD_KEY}"
response = requests.get(url)
data = response.json()

try:
	img_response = requests.get(data['hdurl'])

	if img_response.status_code == 200:
		image_bytes = io.BytesIO(img_response.content)
		media = api.media_upload(filename=f"{data['date']}-apod.jpg", file=image_bytes)

		response = client.create_tweet(text=data['title'], media_ids=[media.media_id])
		latest_tweet_id = response.data["id"]

		response = client.create_tweet(
			text="Learn more at: https://apod.nasa.gov/apod/astropix.html",
			in_reply_to_tweet_id=latest_tweet_id
		)
		latest_tweet_id = response.data["id"]
	else:
		print(f"Failed to fetch image. Status code: {img_response.status_code}")

	print("Thread posted successfully!")
except Exception as e:
	print(f"Error occurred: {e}")