import requests
import tweepy
import io
import atproto

import keys


# X (Twitter) Authentication
auth = tweepy.OAuth1UserHandler(keys.API_KEY, keys.API_SECRET, keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)
clientx = tweepy.Client(keys.BEARER_TOKEN, keys.API_KEY, keys.API_SECRET, keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET)


# Bluesky Authentication
clientb = atproto.Client()
clientb.login(keys.BSKY_USERNAME, keys.BSKY_PASSWORD)


# APOD API Fetch
url = f"https://api.nasa.gov/planetary/apod?api_key={keys.APOD_KEY}"
response = requests.get(url)
data = response.json()

image_date = data['date']
image_title = data['title']
learn_more_text = "Source: apod.nasa.gov/apod/astropix.html"


try:
    img_response = requests.get(data['url'])

    if img_response.status_code == 200:
        image_bytes = io.BytesIO(img_response.content)

        
        # Post on X

        # Uploading the image to API
        media = api.media_upload(filename=f"{image_date}-apod.jpg", file=image_bytes)
        
        # Creating the tweet along with the image
        response = clientx.create_tweet(text=image_title, media_ids=[media.media_id])
        latest_tweet_id = response.data["id"]

        # Replying to the last tweet
        response = clientx.create_tweet(
            text = learn_more_text,
            in_reply_to_tweet_id = latest_tweet_id
        )
        

        # Post on Bluesky

        # Creating the post and also setting a reference
        root_post_ref = atproto.models.create_strong_ref(
            clientb.send_image(
                text = image_title,
                image = image_bytes,
                image_alt = f"Astronomy Picture of the Day: {image_title}",
            )
        )

        # Replying to the last post
        clientb.send_post(
            text = learn_more_text,
            reply_to = atproto.models.AppBskyFeedPost.ReplyRef(parent = root_post_ref, root = root_post_ref)
        )

    else:
        print(f"Failed to fetch image. Status code: {img_response.status_code}")

    print("APOD posted successfully!")
except Exception as e:
    print(f"Error occurred: {e}")
