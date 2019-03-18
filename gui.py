import os
import tkinter as tk
from PIL import ImageTk, Image

class Window:
    def __init__(self, phrase=None):
        self.phrase = phrase
        self.img = None

        self.root = tk.Tk()
        self.root.title('Bruton Gaster')

        # Fixed size 600x600
        self.root.geometry("600x600")

        # Centers window
        x_offset = int(self.root.winfo_screenwidth() / 2 - 600 / 2)
        y_offset = int(self.root.winfo_screenheight() / 2 - 600 / 2)
        self.root.geometry("+{}+{}".format(x_offset, y_offset))

    def show(self):
        pass

    def update(self):
        pass

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    win = Window()
    win.run()