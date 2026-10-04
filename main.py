import io

import requests

# import twitter
import bluesky
import keys


def prune_description(limit, alt_text):
    additional_text = "[MORE ON THE WEBSITE]"
    max_len = limit - len(additional_text) - 1

    if len(alt_text) > max_len:
        return alt_text[:max_len].rstrip() + " " + additional_text
    else:
        return alt_text


# APOD API Fetch
# OLD URL (DEPRECATED)
# url = f"https://api.nasa.gov/planetary/apod?api_key={keys.APOD_KEY}"

url = f"https://science.nasa.gov/wp-json/wp/v2/apod-basic?api_key={keys.APOD_KEY}"

try:
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    # The API currently seems to ignore the query parameters to
    # fetch only today's information and due to that, we have to
    # fetch multiple dictionaries inside the list and use only the
    # first element.
    data_for_today = data[0]
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
    print(f"Response content: {response.text}")
    exit(1)
except requests.exceptions.JSONDecodeError:
    print("Failed to decode JSON. The API returned non-JSON data.")
    print(f"Raw response: {response.text}")
    exit(1)

response_date = data_for_today["date"]
source_url = data_for_today["url"]

response_title = data_for_today["title"]
media_type = data_for_today["media_type"]

if media_type == "video" or media_type == "image":
    media_url = data_for_today["hdurl"]


if media_type == "video":
    # twitter.post_video(response_title, media_url, source_url)
    bluesky.post_video(response_title, media_url, source_url)

elif media_type == "image":
    response_desc = data_for_today["alt"]
    # alt_text_twitter = prune_description(1000, response_desc)
    alt_text_bluesky = prune_description(2000, response_desc)

    img_response = requests.get(media_url)

    if img_response.status_code == 200:
        image_bytes = io.BytesIO(img_response.content)

        # twitter.post_image(
        #     response_title, image_bytes, source_url, alt_text_twitter
        # )
        bluesky.post_image(response_title, image_bytes, source_url, alt_text_bluesky)

    else:
        print(f"Failed to fetch image. Status code: {img_response.status_code}")

elif media_type == "other":
    # twitter.post_tweet(source_url)
    bluesky.post_text(source_url)
