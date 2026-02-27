from pathlib import Path

from guster import GusterWebApp, ImageUrlRepository, NicknameRepository, WikimediaImageRepository


def main():
    base_dir = Path(__file__).resolve().parent
    remote_image_urls = WikimediaImageRepository().load()
    local_image_urls = ImageUrlRepository(base_dir / "data" / "image_urls.txt").load()
    image_urls = remote_image_urls + [url for url in local_image_urls if url not in remote_image_urls]
    nicknames = NicknameRepository(base_dir / "data" / "nicknames.txt").load()
    app = GusterWebApp(image_urls=image_urls, nicknames=nicknames, host="localhost")
    app.run()


if __name__ == "__main__":
    main()
