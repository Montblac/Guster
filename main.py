import image
import gui
import name

if __name__ == '__main__':
    imgen = image.ImageGenerator()
    ngen = name.NameGenerator()
    app = gui.WebApp(images=imgen.urls, nicknames=ngen.names)
    app.run()
