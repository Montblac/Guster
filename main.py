import image
import gui

if __name__ == '__main__':
    imgen = image.ImageGenerator()
    app = gui.WebApp(images=imgen.images)
    app.run()
