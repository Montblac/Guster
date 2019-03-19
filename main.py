import name
import gui

if __name__ == '__main__':
    namegen = name.NameGenerator()
    names = namegen.names()

    win = gui.Window(names=names, images=None)
    win.run()
