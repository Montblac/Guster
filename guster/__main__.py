from pathlib import Path

from guster import GusterApp, WikimediaImageRepository, load_text_file, run_server


def main():
    base_dir = Path(__file__).resolve().parent.parent
    remote_urls = WikimediaImageRepository().load()
    local_urls = load_text_file(base_dir / "data" / "image_urls.txt")
    remote_set = set(remote_urls)
    image_urls = remote_urls + [u for u in local_urls if u not in remote_set]
    nicknames = load_text_file(base_dir / "data" / "nicknames.txt")
    run_server(GusterApp(image_urls=image_urls, nicknames=nicknames))


if __name__ == "__main__":
    main()
