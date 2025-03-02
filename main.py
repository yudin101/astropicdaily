import requests
import io

import keys

import twitter
import bluesky


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


# APOD API Fetch
url = f"https://api.nasa.gov/planetary/apod?api_key={keys.APOD_KEY}"
response = requests.get(url)
data = response.json()

response_date = data["date"]
response_title = data["title"]
response_desc = data["explanation"]
media_type = data["media_type"]
media_url = data["url"]
source_url = date_extract(response_date)


if media_type == "video":
    twitter.post_video(response_title, media_url, source_url)
    bluesky.post_video(response_title, media_url, source_url)

elif media_type == "image":
    img_response = requests.get(media_url)

    if img_response.status_code == 200:
        image_bytes = io.BytesIO(img_response.content)

        twitter.post_image(response_title, response_desc, image_bytes, source_url)
        bluesky.post_image(response_title, response_desc, image_bytes, source_url)

    else:
        print(f"Failed to fetch image. Status code: {img_response.status_code}")
