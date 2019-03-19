from tkinter import Tk, Button, Canvas, Label
from PIL import ImageTk, Image


class Window:
    def __init__(self, name=None):
        self.name = name
        self.img = None

        self.root = Tk()
        self.root.title('Bruton Gaster')
        self.root.resizable(False, False)

        # Fixed size 500x500
        self.root.geometry("500x500")

        # Centers window
        x_offset = int(self.root.winfo_screenwidth() / 2 - 500 / 2)
        y_offset = int(self.root.winfo_screenheight() / 2 - 500 / 2)
        self.root.geometry("+{}+{}".format(x_offset, y_offset))

        # Create canvas
        canvas = Canvas(self.root, width=400, height=400)
        canvas.grid(row=0, padx=48, pady=10)

        #im = ImageTk.PhotoImage(Image.open("images/med_img1.jpg"))
        #canvas.create_image(400, 400, image=im)
        #canvas.create_rectangle(0, 0, 400, 400, fill='blue')

        # Create label
        self.label = Label(self.root, text="Gus")
        self.label.configure(font=('Calibri', 20))
        self.label.grid(row=2, rowspan=2, sticky='NWSE')

        # Create button
        self.button = Button(self.root, text="Hear about Pluto?", command=self.show)
        self.button.configure(fg='#191970', activeforeground='white', bd=0, font=('Calibri', 20))
        self.button.configure(highlightthickness=0, highlightbackground='#708090')
        self.button.grid(row=4, pady=14, sticky='NWSE')

        # Default background
        default_bg = '#708090'
        self.root.configure(bg=default_bg)
        for widget in self.root.winfo_children():
            widget.configure(bg=default_bg)

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
