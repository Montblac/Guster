from tkinter import Tk, Button, Canvas, Label
from PIL import ImageTk, Image
from io import BytesIO
import random
import requests


class Window:
    def __init__(self, names=None, images=None, urls=None):
        self.name = None
        self.names = names
        self.images = images
        self.urls = urls

        self.root = Tk()
        self.root.title('Burton Guster')
        self.root.after(1, lambda: self.root.focus_force())
        self.root.resizable(False, False)

        # Fixed size 500x500
        self.root.geometry('500x500')

        # Centers window
        x_offset = int(self.root.winfo_screenwidth() / 2 - 500 / 2)
        y_offset = int(self.root.winfo_screenheight() / 2 - 500 / 2)
        self.root.geometry('+{}+{}'.format(x_offset, y_offset))

        # Create canvas
        self.canvas = Canvas(self.root, width=400, height=400)
        self.canvas.grid(row=0, padx=48, pady=10)
        self.image = self.canvas.create_image(200, 200, image=None)

        # Create label
        self.label = Label(self.root, text=None)
        self.label.configure(font=('Calibri', 20))
        self.label.grid(row=2, rowspan=2, sticky='NWSE')

        # Create button
        self.button = Button(self.root, text="Hear about Pluto?", command=self.update)
        self.button.configure(fg='#191970', activeforeground='white', bd=0, font=('Calibri', 20))
        self.button.configure(highlightthickness=0, highlightbackground='#708090')
        self.button.grid(row=4, pady=14, sticky='NWSE')

        # Default background
        default_bg = '#708090'
        self.root.configure(bg=default_bg)
        for widget in self.root.winfo_children():
            widget.configure(bg=default_bg)

        self.update()

    def update(self):
        """
        Updates current image and nickname
        :return: None
        """
        self.update_image()
        self.update_name()

    def update_image(self):
        """
        Modifies current image on canvas
        :return: None
        """
        try:
            if self.urls:
                url = self.get_url()
                data = requests.get(url)
                im = Image.open(BytesIO(data.content))
            else:
                raise IOError
        except IOError:
            im = Image.open(self.get_image())

        im = im.resize((403, 403), Image.ANTIALIAS)
        im = ImageTk.PhotoImage(im)
        self.canvas.itemconfig(self.image, image=im)
        self.canvas.image = im

    def update_name(self):
        """
        Modified current name on canvas
        :return: None
        """
        self.label.config(text=self.get_name())

    def get_image(self):
        return random.choice(self.images)

    def get_name(self):
        return random.choice(self.names)

    def get_url(self):
        return random.choice(self.urls)

    def run(self):
        self.root.mainloop()
