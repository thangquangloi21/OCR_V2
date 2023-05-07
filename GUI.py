import os
from tkinter import *
import tkinter
from tkinter import filedialog as fd
from tkinter.filedialog import asksaveasfile
from PIL import ImageTk
import matplotlib.pyplot as plt
from PIL import Image
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from tkinter import messagebox


window = Tk()
# inp anh
def inp_image():
    del_image()
    img = fd.askopenfilename(initialdir=os.getcwd(), title="Select Image File", filetypes=())
    #img = './file_test/072199003062.jpeg'
    img = Image.open(img)
    # plt.imshow(img)
    # plt.show()
    s = detector.predict(img)
    print(s)
    img.thumbnail((200, 100))
    # img.show()
    img = ImageTk.PhotoImage(img)
    showimage.configure(image=img)
    showimage.image = img
    showtext.insert(END,s)
    f = open('./log.txt', 'w',encoding='utf-8')
    f.writelines(s)
    f.close()
    print("DA THEM ANH THANH CONG")
    messagebox.showinfo('Thông Báo', 'Đã Đọc Ảnh Thành Công')


def del_image():
    showtext.delete(1.0,END)
    showimage.config(image='')
    showimage.image = ''
# setup btn xuat anh
def xuattxt():
    files = [('Text Document', '*.txt'),('All Files', '*.*')
             ]
    files = asksaveasfile(initialdir=os.getcwd(), title="Select Image File",filetypes=files, defaultextension=files)
    a = open("log.txt",'r')
    files.write(a.read())
    files.close()
    print("Đã Xuất *.txt Thành Công")
    messagebox.showinfo('Thông Báo', 'Đã xuất File Thành Công')
def Delen():
    showimage = Label()




window.title('Đọc Chữ Viết Tay')
# chỉnh cửa sổ
window.geometry('700x400')
#window.config(bg='light yellow')
window.resizable(width=0, height=0)
# thêm label
lbl = tkinter.Label(window, text='BY: TQL', fg='red', font=("Arial", 10))
lbl.place(x=10, y=377)
pb1 = tkinter.Label(window, text='1.0.0', fg='red', font=("Arial", 10))
pb1.place(x=660, y=0)
txtbox = tkinter.Label(window, text='Text:', fg='red', font=("Arial", 10))
txtbox.place(x=410, y=30)
imagebox = tkinter.Label(window, text='Ảnh:', fg='red', font=("Arial", 10))
imagebox.place(x=30, y=30)
# thêm File + đọc chữ
btnOpenfile = Button(window, text="Thêm Ảnh", bg="red", command=inp_image)
btnOpenfile.place(x=325, y=80)
# Xóa Ảnh
Xoaanh = Button(window, text="Xóa Ảnh", bg="red", command=del_image)
Xoaanh.place(x=330, y=130)
# xuat file .txt
Xuatfiletxt = Button(window, text="Xuất File *.txt", bg="red", command=xuattxt)
Xuatfiletxt.place(x=318, y=180)
# text widget1
showtext = Text(window, height=20, width=33, bg="light yellow")
showtext.place(x=410, y=50)
# text widget2
ABC = Label(window, height=20, width=33, bg="light yellow")
ABC.place(x=30, y=50)
# ĐÈ
showimage = Label()
showimage.place(x=30, y=50)

config = Cfg.load_config_from_file('config.yml')
config = Cfg.load_config_from_name('vgg_transformer')
config['weights'] = './weights/transformerocr.pth'
config['cnn']['pretrained'] = False
config['device'] = 'cuda:0'
config['predictor']['beamsearch'] = False
detector = Predictor(config)
window.mainloop(0)
