import requests
import tweepy
import io
import atproto

import keys


# X (Twitter) Authentication
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


# Bluesky Authentication
clientb = atproto.Client()
clientb.login(keys.BSKY_USERNAME, keys.BSKY_PASSWORD)


# APOD API Fetch
url = f"https://api.nasa.gov/planetary/apod?api_key={keys.APOD_KEY}"
response = requests.get(url)
data = response.json()


def prune_description(limit, alt_text):
    additional_text = "[MORE ON THE WEBSITE]"
    max_len = limit - len(additional_text) - 1

    if len(alt_text) > max_len:
        return alt_text[:max_len].rstrip() + " " + additional_text
    else:
        return alt_text


def date_extract(date):
    extract = date[2:4] + date[5:7] + date[8:]
    return f"apod.nasa.gov/apod/ap{extract}.html"


response_date = data["date"]
response_title = data["title"]
response_desc = data["explanation"]
media_type = data["media_type"]
media_url = data["url"]
source_url = date_extract(response_date)


try:
    if media_type == "video":
        # Creating a tweet (Twitter)
        response = clientx.create_tweet(text=f"{response_title}\nURL: {media_url}")
        latest_tweet_id = response.data["id"]

        # Crreating a post (Bluesky)
        root_post_ref = atproto.models.create_strong_ref(
            clientb.send_post(
                text=atproto.client_utils.TextBuilder()
                .text(f"{response_title}\nURL: ")
                .link(media_url, media_url),
            )
        )

    elif media_type == "image":
        img_response = requests.get(media_url)

        if img_response.status_code == 200:
            twitter_image_bytes = io.BytesIO(img_response.content)
            bsky_image_bytes = io.BytesIO(img_response.content)

            # Uploading the image to the Twitter API
            twitter_image_bytes.seek(0)
            media = api.media_upload(
                filename=f"{response_date}-apod.jpg", file=twitter_image_bytes
            )

            # Adding alt text in Twitter
            alt_text_limit_twitter = 1000
            media_metadata = api.create_media_metadata(
                media_id=media.media_id,
                alt_text=prune_description(alt_text_limit_twitter, response_desc),
            )

            # Creating the tweet along with the image
            response = clientx.create_tweet(
                text=response_title, media_ids=[media.media_id]
            )
            latest_tweet_id = response.data["id"]

            # Uploading the post along with the image (Bluesky)
            alt_text_limit_bsky = 2000
            bsky_image_bytes.seek(0)
            root_post_ref = atproto.models.create_strong_ref(
                clientb.send_image(
                    text=response_title,
                    image=bsky_image_bytes.read(),
                    image_alt=prune_description(alt_text_limit_bsky, response_desc),
                )
            )
        else:
            print(f"Failed to fetch image. Status code: {img_response.status_code}")

    # Replying to the last tweet (Twitter)
    response = clientx.create_tweet(
        text=f"Source: {source_url}",
        in_reply_to_tweet_id=latest_tweet_id,
    )

    # Replying to the last post (Bluesky)
    clientb.send_post(
        text=atproto.client_utils.TextBuilder()
        .text("Source: ")
        .link(
            f"{source_url}",
            f"https://{source_url}",
        ),
        reply_to=atproto.models.AppBskyFeedPost.ReplyRef(
            parent=root_post_ref, root=root_post_ref
        ),
    )

    print("APOD posted successfully!")
except Exception as e:
    print(f"Error occurred: {e}")
