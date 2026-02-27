from pathlib import Path

from guster import GusterWebApp, ImageUrlRepository, NicknameRepository


def main():
    base_dir = Path(__file__).resolve().parent
    image_urls = ImageUrlRepository(base_dir / "data" / "image_urls.txt").load()
    nicknames = NicknameRepository(base_dir / "data" / "nicknames.txt").load()
    app = GusterWebApp(image_urls=image_urls, nicknames=nicknames, host="localhost")
    app.run()


if __name__ == "__main__":
    main()
