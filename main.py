import name
import image
import gui

if __name__ == '__main__':
    namegen = name.NameGenerator()
    names = namegen.names

    imgen = image.ImageGenerator()
    images = imgen.images
    urls = imgen.urls

    win = gui.Window(names=names, images=images, urls=urls)
    win.run()

