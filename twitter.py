import tweepy
import keys


# X (Twitter) Authentication
print("Authenticating to Twitter...")
auth = tweepy.OAuth1UserHandler(
    keys.API_KEY, keys.API_SECRET, keys.ACCESS_TOKEN, keys.ACCESS_TOKEN_SECRET
)
api = tweepy.API(auth)
clientx = tweepy.Client(
    keys.BEARER_TOKEN,
    keys.API_KEY,
    keys.API_SECRET,
    keys.ACCESS_TOKEN,
    keys.ACCESS_TOKEN_SECRET,
)


def post_reply(latest_tweet_id, source_url):
    print("Sending reply to the latest tweet...")
    clientx.create_tweet(
        text=f"Source: {source_url}",
        in_reply_to_tweet_id=latest_tweet_id,
    )


def post_image(response_title, response_desc, image_bytes, source_url):
    print("\nCreating a tweet with image...")
    # Uploading the image to the Twitter API
    image_bytes.seek(0)
    media = api.media_upload(filename=f"{response_title}-apod.jpg", file=image_bytes)

    # Adding alt text in Twitter
    alt_text_limit_twitter = 1000
    media_metadata = api.create_media_metadata(
        media_id=media.media_id,
        alt_text=prune_description(alt_text_limit_twitter, response_desc),
    )

    # Creating the tweet along with the image
    response = clientx.create_tweet(text=response_title, media_ids=[media.media_id])
    latest_tweet_id = response.data["id"]

    post_reply(latest_tweet_id, source_url)


def post_video(response_title, media_url, source_url):
    print("\nCreating a tweet with video URL...")
    response = clientx.create_tweet(text=f"{response_title}\nURL: {media_url}")
    latest_tweet_id = response.data["id"]

    post_reply(latest_tweet_id, source_url)
