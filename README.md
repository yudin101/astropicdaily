> [!NOTE]
> This bot is currently not available on Instagram because Instagram blocks PythonAnywhere's free account's IP.

# astropicdaily

Bot that uploads the Astronomy Picture of the Day.

Follow astropicdaily on:

- [X (Twitter)](https://x.com/astropicdaily)
- [Bluesky](https://bsky.app/profile/astropicdaily.bsky.social)
- [Instagram](https://www.instagram.com/astro.pic.daily/)

## Run Locally

**Clone the project**

```bash
git clone https://github.com/yudin101/astropicdaily.git
```

**Go to the project directory**

```bash
cd astropicdaily
```

**Install dependencies**

```bash
pip install -r requirements.txt
```

**Setup variables**

```bash
echo "BEARER_TOKEN = 'your_bearer_token_here'" > keys.py
echo "API_KEY = 'your_api_key_here'" >> keys.py
echo "API_SECRET = 'your_api_secret_here'" >> keys.py
echo "ACCESS_TOKEN = 'your_access_token_here'" >> keys.py
echo "ACCESS_TOKEN_SECRET = 'your_access_token_secret_here'" >> keys.py
echo "APOD_KEY = 'your_apod_key_here'" >> keys.py
echo "BSKY_USERNAME = 'your_bluesky_username'" >> keys.py
echo "BSKY_PASSWORD = 'your_bluesky_password'" >> keys.py
echo "INSTA_USERNAME = 'your_instagram_password'" >> keys.py
echo "INSTA_PASSWORD = 'your_instagram_password'" >> keys.py
```

_X (Twitter) related keys can be generated from [X Developer Portal](https://developer.x.com/en). APOD_KEY can be created from [NASA Open APIs](https://api.nasa.gov/)._

**Run the script**

```bash
python3 main.py
```

## Contributing

Contributions are always welcome!

If you’d like to contribute to this project, you can:

- **Create an Issue**: Report bugs or suggest features by [creating an issue](https://github.com/Yudin101/astropicdaily/issues/new).
- **Open a Pull Request**: Submit code changes or improvements by [opening a pull request](https://github.com/Yudin101/astropicdaily/pulls).

Thank you for your interest in contributing!

## License

This project is licensed under the [MIT License](https://github.com/yudin101/astropicdaily/blob/main/LICENSE).
