from instagrapi import Client
import tempfile
import keys

cl = Client()
cl.login(keys.INSTA_USERNAME, keys.INSTA_PASSWORD)


def post_image(response_title, image_bytes, response_desc, source_url):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        temp_file.write(image_bytes.getvalue())
        temp_file_path = temp_file.name

        media = cl.photo_upload(
            temp_file_path,
            f"{response_title}\n\n#astronomy #astrophotography #apod",
        )

    media_id = media.dict()["id"]
    print(media_id)
    post_comment(media_id, source_url, response_desc)


def post_comment(media_id, source_url):
    cl.media_comment(media_id, f"{response_desc}\n\nSource: {source_url}")
