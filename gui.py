from tkinter import Tk, Button
from PIL import ImageTk, Image


class Window:
    def __init__(self, name=None):
        self.name = name
        self.img = None

        self.root = Tk()
        self.root.title('Bruton Gaster')

        # Fixed size 600x600
        self.root.geometry("600x600")

        # Centers window
        x_offset = int(self.root.winfo_screenwidth() / 2 - 600 / 2)
        y_offset = int(self.root.winfo_screenheight() / 2 - 600 / 2)
        self.root.geometry("+{}+{}".format(x_offset, y_offset))

        self.button = Button(self.root, text="Press me", command=self.show)
        self.button.pack()

    def show(self):
        """
        Shows a random image of Gus and nickname
        :return: None
        """
        pass

    def update(self):
        """
        Updates current image and nickname
        :return: None
        """
        pass

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    win = Window()
    win.run()
