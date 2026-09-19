import os
import tempfile

from instagrapi import Client

import keys

SESSION_FILE = "insta_session.json"


def get_client():
    print("Authenticating to Instagram...")
    cl = Client()
    if os.path.exists(SESSION_FILE):
        cl.load_settings(SESSION_FILE)
    cl.login(keys.INSTA_USERNAME, keys.INSTA_PASSWORD)
    cl.dump_settings(SESSION_FILE)
    return cl


def post_comment(cl, media_id, source_url, response_desc):
    print("Instagram: Replying to the latest post...")
    cl.media_comment(media_id, f"{response_desc}\n\nSource: {source_url}")


def post_image(response_title, image_bytes, response_desc, source_url):
    cl = get_client()
    print("\nInstagram: Creating a post with image...")
    # A temporary file had to be created because I could only enter the file path

    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        temp_file.write(image_bytes.getvalue())
        temp_file_path = temp_file.name

        try:
            media = cl.photo_upload(
                temp_file_path,
                f"{response_title}\n\n#astronomy #astrophotography #apod",
            )

            media_id = media.dict()["id"]
            post_comment(cl, media_id, source_url, response_desc)
        finally:
            os.remove(temp_file_path)
