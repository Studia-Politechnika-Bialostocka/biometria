from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import pathlib
import pygubu
import tkinter as tk
import tkinter.ttk as ttk

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "biometria_gui.ui"


class BiometriaGuiApp:
    def __init__(self, master=None):
        # build ui
        self.original_image = None
        self.main_window = tk.Tk() if master is None else tk.Toplevel(master)
        self.menu_frame = tk.Frame(self.main_window)
        self.select_image_button = tk.Button(self.menu_frame)
        self.select_image_button.configure(cursor='hand2', text='Select Image')
        self.select_image_button.pack(ipadx='10', pady='10', side='top')
        self.select_image_button.configure(command=self.select_and_insert_image)
        self.binarize_image_button = tk.Button(self.menu_frame)
        self.binarize_image_button.configure(cursor='hand2', text='Binarize Image')
        self.binarize_image_button.pack(ipadx='10', pady='10', side='top')
        self.binarize_image_button.configure(command=self.binarize_image)
        self.menu_frame.configure(background='#0d938c', height='800', width='200')
        self.menu_frame.pack(side='left')
        self.menu_frame.pack_propagate(0)
        self.main_frame = tk.Frame(self.main_window)
        self.original_image_canvas = tk.Canvas(self.main_frame)
        self.original_image_canvas.configure(background='#0e5092', cursor='hand2', height='400', width='400')
        self.original_image_canvas.pack(anchor='center', side='left')
        self.original_image_canvas.bind('<Button-1>', self.open_original_image)
        self.changed_image_1_canvas = tk.Canvas(self.main_frame)
        self.changed_image_1_canvas.configure(background='#970925', cursor='hand2', height='400', width='400')
        self.changed_image_1_canvas.pack(anchor='center', side='right')
        self.main_frame.configure(background='#ff80c0', height='800', width='1166')
        self.main_frame.pack(side='top')
        self.main_frame.pack_propagate(0)
        self.main_window.configure(height='200', width='200')
        self.main_window.geometry('1366x768')
        self.main_window.resizable(False, False)
        self.main_window.title('Biometric Basics')

        # Main widget
        self.mainwindow = self.main_window

    def run(self):
        self.mainwindow.mainloop()

    def select_and_insert_image(self):
        filename = filedialog.askopenfilename(title='Select an image')
        img = Image.open(filename)
        self.original_image = img
        img = self.change_image_size(img)
        self.insert_original_image(img)

    def insert_original_image(self, img):
        # PhotoImage class is used to add image to widgets, icons etc
        img = ImageTk.PhotoImage(img)
        self.original_image_canvas.create_image(0, 0, image=img, anchor='nw')
        self.original_image_canvas.image = img
        self.original_image_canvas.configure(height=img.height(), width=img.width())

    def change_image_size(self, img, width=400, height=400):
        return img.resize((width, height), Image.ANTIALIAS)

    def open_original_image(self, event):
        if not self.original_image:
            self.message_popup('Original Image', 'You need to select an image first', 'warning')
        else:
            self.original_image.show()

    def message_popup(self, title, text, type_message='info'):
        if type_message == 'info':
            tk.messagebox.showinfo(title, text)
        elif type_message == 'warning':
            tk.messagebox.showwarning(title, text)
        elif type_message == 'error':
            tk.messagebox.showerror(title, text)

    def binarize_image(self):
        if not self.original_image:
            self.message_popup('Original Image', 'You need to select an image first', 'info')
        pass


if __name__ == '__main__':
    app = BiometriaGuiApp()
    app.run()





