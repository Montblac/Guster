import os


class ImageGenerator:
    def __init__(self, source_path='img'):
        self.source_path = source_path
        self.urls = []
        self.get_urls()

    def get_urls(self):
        if os.path.exists(self.source_path):
            with open(self.source_path, encoding='utf-8') as handle:
                for line in handle:
                    value = line.strip()
                    if value and not value.startswith('#'):
                        self.urls.append(value)
