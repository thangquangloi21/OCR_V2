import shutil
import sys
import time
from PIL import Image
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from View.Qtgui import Ui_Vision_OCR
from Working_Thread import Working_thread
from run_train import ThreadClass

class MainWindow:
    def __init__(self):
        start_time = time.time()
        self.thread = {}
        self.thead1 = ThreadClass()
        self.file_show = None
        self.file = None
        self.main_win = QMainWindow()
        self.main_win.show()
        self.Working_thread = Working_thread()
        self.uic = Ui_Vision_OCR()
        self.uic.setupUi(self.main_win)
        end_time = time.time()
        elapsed_time = end_time - start_time
        self.writeLog(f"Khởi động app: {elapsed_time} Giây")
        self.writeLog("Chào mừng đến với Vision OCR")
        # topview_file
        self.uic.Open_File.triggered.connect(self.openfile)
        self.uic.Open_Foder.triggered.connect(self.openfile)

        # topview_image
        self.uic.Setting_Camera.triggered.connect(self.setting_camera)
        self.uic.Connect_camera.triggered.connect(self.Working_thread.connect_camera)
        self.uic.Disconect_camera.triggered.connect(self.Working_thread.disconect_camera)
        self.uic.Capture_Image.triggered.connect(self.Working_thread.capture_image)
        self.uic.Capture_Video.triggered.connect(self.Working_thread.capture_video)
        self.uic.Save_image.triggered.connect(self.Working_thread.save_image)

        # topview_light
        self.uic.setting_light.triggered.connect(self.Working_thread.setting_light)
        self.uic.light_Connect.triggered.connect(self.Working_thread.connect_light)
        self.uic.light_Disconnect.triggered.connect(self.Working_thread.disconect_light)

        # topview_plc
        self.uic.PLC_Setting.triggered.connect(self.Working_thread.setting_plc)
        self.uic.PLC_Connect.triggered.connect(self.Working_thread.connect_plc)
        self.uic.PlC_Disconnect.triggered.connect(self.Working_thread.disconect_plc)

        # leftview_btn
        self.uic.Testing_Button.clicked.connect(self.testing)
        self.uic.Run_Button.clicked.connect(self.Working_thread.run_btn)
        self.uic.Stop_Button.clicked.connect(self.Working_thread.stop_btn)
        # Train
        self.uic.Setting_Button.clicked.connect(self.Working_thread.setting_train)
        self.uic.Run_Train_Button.clicked.connect(self.start_worker_1)
        self.uic.Stop_Train_Button.clicked.connect(self.stop_worker_1)

        # next+backpic
        self.uic.Next_pic.clicked.connect(self.nextpic)
        self.uic.Back_pic.clicked.connect(self.backpic)

        # bottomview
        self.uic.show_img_button.clicked.connect(self.Curent_showimg)
        self.uic.save_current_img.clicked.connect(self.save_img)
        self.uic.export_log.clicked.connect(self.export_log)
        self.uic.Load_config_btnn.clicked.connect(self.load_config)

    def start_worker_1(self):

        try:
            shutil.rmtree("train_hw")
            shutil.rmtree("valid_hw")
            self.thread[1] = ThreadClass(index=1)
            self.thread[1].start()
            # self.thread[1].signal.connect(self.my_function)
            self.uic.Run_Train_Button.setEnabled(False)
            self.uic.Stop_Train_Button.setEnabled(True)
        except Exception as error:
            QMessageBox.about(self, "Title", "ERROR : {}".format(error))
            print("ERROR Camera setting : {}".format(error))

    def stop_worker_1(self):
        try:
            self.thread[1].stop()
            self.uic.Stop_Train_Button.setEnabled(False)
            self.uic.Run_Train_Button.setEnabled(True)
        except Exception as error:
            QMessageBox.about(self, "Title", "ERROR : {}".format(error))
            print("ERROR Camera setting : {}".format(error))
    def openfile(self):
        self.file = self.Working_thread.open_file()
        print(self.file)
        self.show_image(self.file)


    def nextpic(self):
        if self.Working_thread.current_index < len(self.Working_thread.list_image_path) - 1:
            self.Working_thread.current_index += 1
            # print(self.Working_thread.current_index)
            self.show_image(self.Working_thread.list_image_path[self.Working_thread.current_index])

    def backpic(self):
        if self.Working_thread.current_index > 0:
            self.Working_thread.current_index -= 1
            # print(self.Working_thread.current_index)
            self.show_image(self.Working_thread.list_image_path[self.Working_thread.current_index])

    def testing(self):
        try:
            print(self.file_show)
            kq = self.Working_thread.testing_btn(file=self.file_show)
            self.uic.kq_show.setText(kq)
            self.Working_thread.logshow(kq)
            _kq = "Kết Quả: " + kq
            self.writeLog(_kq)
        except Exception as error:
            self.writeLog(error)
            return error

    def show_image(self, file):
        self.uic.img_link.setText(file)
        self.file_show = file
        self.uic.Show_img.setPixmap(QtGui.QPixmap(self.file_show))

    def writeLog(self, text):
        now = QDateTime.currentDateTime().toString('hh:mm:ss dd/MM/yyyy')
        log = "{}: {}\n".format(now, text)
        print(log)
        self.Working_thread.logshow(log)
        self.uic.Show_log.append(log)

    # bottom view
    def Curent_showimg(self):
        img = Image.open(self.file_show)
        # Hiển thị hình ảnh
        img.show()

    def save_img(self):
        img = Image.open(self.file_show)
        # Hiển thị hình ảnh
        img.save()
    def export_log(self):
        ...

    def load_config(self):
        self.Working_thread.loading_config()

    def setting_camera(self):
        self.Working_thread.setting_camera()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    sys.exit(app.exec())