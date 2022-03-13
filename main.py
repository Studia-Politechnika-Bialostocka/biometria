from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog
import pathlib
import pygubu
import tkinter as tk
import tkinter.ttk as ttk
import numpy as np
import matplotlib.pyplot as plt

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "biometria_gui.ui"


class BiometriaGuiApp:
    def __init__(self, master=None):
        # build ui
        self.changed_image_1 = None
        self.original_image = None
        self.main_window = tk.Tk() if master is None else tk.Toplevel(master)
        self.menu_frame = tk.Frame(self.main_window)
        self.select_image_button = tk.Button(self.menu_frame)
        self.select_image_button.configure(cursor='hand2', text='Select Image')
        self.select_image_button.pack(fill='x', ipadx='10', padx='10', pady='10', side='top')
        self.select_image_button.configure(command=self.select_and_insert_image)
        self.frame1 = tk.Frame(self.menu_frame)
        self.binarize_threshold_scale = tk.Scale(self.frame1)
        self.binarize_threshold_scale.configure(from_='0', label='Threshold', orient='horizontal', to='255')
        self.binarize_threshold_scale.pack(fill='x', side='top')
        self.binarize_threshold_scale.set(120)
        self.__tkvar = tk.StringVar(value='Normal')
        __values = ['Red', 'Green', 'Blue', 'Normal']
        self.binarize_options = tk.OptionMenu(self.frame1, self.__tkvar, 'Normal', *__values, command=self.set_binarize_option)
        self.set_binarize_option(self.__tkvar.get())
        self.binarize_options.pack(anchor='n', fill='x', side='top')
        self.binarize_image_button = tk.Button(self.frame1)
        self.binarize_image_button.configure(text='Binarize Image')
        self.binarize_image_button.pack(fill='x', side='top')
        self.binarize_image_button.configure(command=self.binarize_and_insert_image)
        self.frame1.configure(height='117', width='200')
        self.frame1.pack(padx='10', side='top')
        self.frame1.pack_propagate(0)
        self.menu_frame.configure(background='#F6AE2D', height='800', width='200')
        self.menu_frame.pack(side='left')
        self.menu_frame.pack_propagate(0)
        self.main_frame = tk.Frame(self.main_window)
        self.original_image_canvas = tk.Canvas(self.main_frame)
        self.original_image_canvas = tk.Canvas(self.main_frame)
        self.original_image_canvas.configure(background='#0e5092', cursor='hand2', height='350', width='350')
        self.original_image_canvas.place(anchor='nw', relx='0.13', rely='0.03', x='0', y='0')
        self.original_image_canvas.bind('<Button-1>', lambda _: self.open_image_in_new_window(self.original_image_canvas, self.original_image))
        self.changed_image_1_canvas = tk.Canvas(self.main_frame)
        self.changed_image_1_canvas.configure(background='#F26419', cursor='hand2', height='350', width='350')
        self.changed_image_1_canvas.place(anchor='ne', relx='0.87', rely='0.03', x='0', y='0')
        self.changed_image_1_canvas.bind('<Button-1>', lambda _: self.open_image_in_new_window(self.changed_image_1_canvas, self.changed_image_1))
        self.grey_original_image_canvas = tk.Canvas(self.main_frame)
        self.grey_original_image_canvas.configure(background='#65dc80', height='350', width='350')
        self.grey_original_image_canvas.place(anchor='sw', relx='0.13', rely='0.97', x='0', y='0')
        self.grey_changed_image_1_canvas = tk.Canvas(self.main_frame)
        self.grey_changed_image_1_canvas.configure(background='#8986bb', height='350', width='350')
        self.grey_changed_image_1_canvas.place(anchor='se', relx='0.87', rely='0.97', x='0', y='0')
        self.histogram_1 = tk.Button(self.main_frame)
        self.histogram_1.configure(text='Histogram 1')
        self.histogram_1.place(relx='0.035', rely='0.25', x='0', y='0')
        self.histogram_1.configure(command=lambda: self.generate_and_display_histogram(self.original_image))
        self.histogram_2 = tk.Button(self.main_frame)
        self.histogram_2.configure(text='Histogram 2')
        self.histogram_2.place(anchor='se', relx='0.965', rely='0.25', x='0', y='0')
        self.histogram_2.configure(command=lambda: self.generate_and_display_histogram(self.changed_image_1, 'changed_image_1'))
        self.histogram_3 = tk.Button(self.main_frame)
        self.histogram_3.configure(text='Histogram 3')
        self.histogram_3.place(anchor='nw', relx='0.035', rely='0.75', x='0', y='0')
        self.histogram_3.configure(command=self.generate_and_display_histogram)
        self.histogram_3.configure(command=lambda: self.generate_and_display_histogram(self.grey_original_image, 'grey_original_image'))
        self.histogram_4 = tk.Button(self.main_frame)
        self.histogram_4.configure(text='Histogram 4')
        self.histogram_4.place(anchor='se', relx='0.965', rely='0.75', x='0', y='0')
        self.histogram_4.configure(command=lambda: self.generate_and_display_histogram(self.grey_changed_image_1, 'grey_changed_image_1'))
        self.main_frame.configure(background='#03256C', height='800', width='1166')
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

    def gray_scale_image(self, image):
        image = image.convert('L')
        return image

    def select_and_insert_image(self):
        filename = filedialog.askopenfilename(title='Select an image')
        if not filename:
            self.message_popup('No image selected', 'No image selected', 'warning')
            return
        img = Image.open(filename)
        self.original_image = img
        self.insert_image(img, self.original_image_canvas)
        grey_image = self.gray_scale_image(img)
        self.grey_original_image = grey_image.copy()
        self.insert_image(grey_image, self.grey_original_image_canvas)

    def change_image_size(self, img, width=350, height=350):
        return img.resize((width, height), Image.ANTIALIAS)

    def open_image_in_new_window(self, event, img):
        if not img:
            self.message_popup('Image', 'You need to select an image first', 'info')
        else:
            img.show()

    def message_popup(self, title, text, type_message='info'):
        if type_message == 'info':
            tk.messagebox.showinfo(title, text)
        elif type_message == 'warning':
            tk.messagebox.showwarning(title, text)
        elif type_message == 'error':
            tk.messagebox.showerror(title, text)

    def binarize_image(self):
        threshold = self.binarize_threshold_scale.get()
        image = self.original_image.copy()
        binarize_option = self.binarize_option
        for x in range(image.width):
            for y in range(image.height):
                pixel = image.getpixel((x, y))
                if binarize_option == 'Normal':
                    pixel = int((pixel[0] + pixel[1] + pixel[2]) / 3)
                elif binarize_option == 'Red':
                    pixel = pixel[0]
                elif binarize_option == 'Green':
                    pixel = pixel[1]
                elif binarize_option == 'Blue':
                        pixel = pixel[2]
                if pixel < threshold:
                    image.putpixel((x, y), (0, 0, 0))
                else:
                    image.putpixel((x, y), (255, 255, 255))
        self.changed_image_1 = image
        return image

    def set_binarize_option(self, option):
        self.binarize_option = option

    def binarize_and_insert_image(self):
        if not self.original_image:
            self.message_popup('Original Image', 'You need to select an image first', 'info')
        else:
            binarized_image = self.binarize_image()
            self.insert_image(binarized_image, self.changed_image_1_canvas)
            grey_image = self.gray_scale_image(binarized_image.copy())
            self.grey_changed_image_1 = grey_image.copy()
            self.insert_image(grey_image, self.grey_changed_image_1_canvas)

    def insert_image(self, img, canvas):
        img = self.change_image_size(img)
        img = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, image=img, anchor='nw')
        canvas.image = img
        canvas.configure(height=img.height(), width=img.width())

    def generate_and_display_histogram(self, image, type_histogram='original'):
        if not image:
            self.message_popup('Image', 'You need to select an image first', 'info')
            return
        histogram = np.zeros(256)
        for x in range(image.width):
            for y in range(image.height):
                pixel = image.getpixel((x, y))
                if type(pixel) == tuple:
                    pixel = int((pixel[0] + pixel[1] + pixel[2]) / 3)
                histogram[pixel] += 1
        plt.figure()
        plt.bar(range(256), histogram)
        plt.title('Histogram of ' + type_histogram + ' image')
        plt.xlabel('Pixel value')
        plt.ylabel('Number of pixels')
        plt.grid(True, which='major', axis='y')
        # max value for plt
        plt.ylim(0, max(histogram) + 100)

        plt.show()


if __name__ == '__main__':
    app = BiometriaGuiApp()
    app.run()





