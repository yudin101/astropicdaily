import atproto
import keys


# Bluesky Authentication
print("Authenticating to Bluesky...")
clientb = atproto.Client()
clientb.login(keys.BSKY_USERNAME, keys.BSKY_PASSWORD)


def post_reply(source_url, root_post_ref):
    print("Sending reply to the latest post...")
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


def post_image(
    response_title, response_desc, image_bytes, source_url, alt_text_bluesky
):
    print("\nCreating a post with image...")
    alt_text_limit_bsky = 2000
    image_bytes.seek(0)
    root_post_ref = atproto.models.create_strong_ref(
        clientb.send_image(
            text=response_title,
            image=image_bytes.read(),
            image_alt=alt_text_bluesky,
        )
    )

    post_reply(source_url, root_post_ref)


def post_video(response_title, media_url, source_url):
    print("\nCreating a post with video URL...")
    root_post_ref = atproto.models.create_strong_ref(
        clientb.send_post(
            text=atproto.client_utils.TextBuilder()
            .text(f"{response_title}\nURL: ")
            .link(media_url, media_url),
        )
    )

    post_reply(source_url, root_post_ref)
