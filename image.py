import os


class ImageGenerator:
    def __init__(self):
        self.images = []
        self.urls = []
        self.path = None

        self.get_path()
        self.get_images()

    def get_path(self):
        self.path = os.path.join(os.getcwd(), 'images')

    def get_images(self):
        if os.path.exists(self.path):
            for file in os.listdir(self.path):
                if not file.startswith('.'):
                    self.images.append(os.path.join(self.path, file))

    def get_urls(self):
        if os.path.exists('img'):
            print('entered if')
            with open('img') as f:
                data = f.readlines()
                for url in data:
                    self.urls.append(url.strip())
