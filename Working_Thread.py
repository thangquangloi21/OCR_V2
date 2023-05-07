import json
import os
from vietocr.tool.config import Cfg
from vietocr.model.trainer import Trainer
from CommonAssit.FileManager import *

# from tkinter import messagebox
import jsonpickle
from PIL import Image
from PyQt5 import QtWidgets
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QFileDialog, QMessageBox

from CommonAssit.FileManager import JsonFile
from View.setting_camera import Ui_setting_camera

class Working_thread():
    camera: Ui_setting_camera
    def __init__(self):
        super().__init__()
        self.iters = 1000
        self.parameterList = []
        self.camera_widget = QtWidgets.QWidget()
        self.ui_setting_camera = Ui_setting_camera()
        self.ui_setting_camera.setupUi(self.camera_widget)
        self.detector = None
        self.config = None
        self.current_index = 0
        self.list_image_path = []
        self.name = ''
        self.id = ''
        self.interface = ''
        self.brand = ''
        self.flip = ''
        self.rotate = ''
        self.load()


    # topview_file
    def open_file(self):
        self.files = QFileDialog.getOpenFileName(None, 'Image files', '', "*.jpg *png *.ico *.bmp *.gif *.GIF *.jpeg ")
        self.path_image = self.files[0]

        # print(self.originalImage)
        self.image_dir = os.path.dirname(self.path_image)
        if len(self.image_dir) != 0:
            self.list_name_image_in_folder = os.listdir(self.image_dir)
            # print(self.path_image, self.image_dir)

            list_duoi = ["jpg", "png", "ico", "bmp", "gif", "GIF", "jpeg"]
            for name_image in self.list_name_image_in_folder:
                index = name_image.rfind('.')
                extension_path = name_image[index + 1:]
                if extension_path in list_duoi:
                    path = self.image_dir + '/' + name_image
                    self.list_image_path.append(path)
            self.current_index = self.list_image_path.index(self.path_image)
            # print(self.list_image_path)
            # print(f"current img idex: {self.current_index}")
        # print(len(self.path_image))
        if len(self.path_image) == 0:
            pass
        else:
            return self.path_image

    # topview_camera
    def setting_camera(self):
        self.camera_widget.show()
        self.ui_setting_camera.pushButton_ok.clicked.connect(self.setting_cam_ok)
        self.ui_setting_camera.pushButton_thoat.clicked.connect(self.camera_widget.hide)

    def setting_cam_ok(self):
        try:
            self.saveCameraSelected()
            # self.getInfo()
        except Exception as error:
            QMessageBox.about(self, "Title", "ERROR Camera setting : {}".format(error))
            print("ERROR Camera setting : {}".format(error))
            # QMessageBox.Ok(self.mainWindow.languageManager.localized("cameraChangeTitle"), "{}".format(error))
        self.camera_widget.hide()
    def saveCameraSelected(self):
        try:
            self.name = self.ui_setting_camera.comboBox_name.currentText()
            self.id = self.ui_setting_camera.comboBox_id.currentText()
            self.interface = self.ui_setting_camera.comboBox_conn.currentText()
            self.brand = self.ui_setting_camera.comboBox_Brand.currentText()
            self.flip = self.ui_setting_camera.comboBox_Flip.currentText()
            self.rotate = self.ui_setting_camera.comboBox_Rotate.currentText()
        except Exception as error:
            QMessageBox.about(self, "error", "Detail: {}".format(error))
            print("Detail: {}".format(error))
        self.parameterList.append(self.name)
        self.parameterList.append(self.id)
        self.parameterList.append(self.interface)
        self.parameterList.append(self.brand)
        self.parameterList.append(self.flip)
        self.parameterList.append(self.rotate)
        print(self.parameterList)
        self.save(self.parameterList)

    def save(self, parameterList=None):
        folderPath = "./config"
        dataFilePath = "./config/camera.json"
        data = []

        if parameterList is None:
            parameterList = []
            for camera in self.cameraList:
                parameterList.append(camera.parameter)

        if not os.path.exists(folderPath):
            os.makedirs(folderPath)
        try:
            for cameraInfo in parameterList:
                data.append(jsonpickle.encode(cameraInfo))
            file = JsonFile(dataFilePath)
            file.data = data
            file.saveFile()
        except Exception as error:
            print("ERROR Camera save parameter: {}".format(error))

    def load(self):
        with open('config/camera.json') as f:
            data = json.load(f)
        camera_name = data[0]
        camera_id = data[1]
        camera_cnn = data[2]
        camera_brand = data[3]
        camera_flip = data[4]
        camera_rotate = data[5]
        # xoa ""
        camera_name = camera_name[1:-1]
        camera_id = camera_id[1:-1]
        camera_cnn = camera_cnn[1:-1]
        camera_brand = camera_brand[1:-1]
        camera_flip = camera_flip[1:-1]
        camera_rotate = camera_rotate[1:-1]
        # set
        self.ui_setting_camera.comboBox_name.setCurrentText(camera_name)
        self.ui_setting_camera.comboBox_id.setCurrentText(camera_id)
        self.ui_setting_camera.comboBox_conn.setCurrentText(camera_cnn)
        self.ui_setting_camera.comboBox_Brand.setCurrentText(camera_brand)
        self.ui_setting_camera.comboBox_Flip.setCurrentText(camera_flip)
        self.ui_setting_camera.comboBox_Rotate.setCurrentText(camera_rotate)

        print(camera_name)  # "Camera 0"
        print(camera_id)  # "0"
        print(camera_cnn)  # "GigE"
        print(camera_brand)  # "Basler"
        print(camera_flip)  # "None"
        print(camera_rotate)  # "0"

    def connect_camera(self):
        print("connected")

    def disconect_camera(self):
        print("disconect")

    def capture_image(self):
        print("capture_pic")

    def capture_video(self):
        print("video")

    def save_image(self):
        print("save img")

    # topview_light
    def setting_light(self):
        print("light")

    def connect_light(self):
        print("connectlight")

    def disconect_light(self):
        print("disconectlight")

    # topview_plc
    def setting_plc(self):
        print("plcsetting")

    def connect_plc(self):
        print("connectplc")

    def disconect_plc(self):
        print("disconectplc")

    # leftview_btn
    def testing_btn(self, file):
        # try except để xử lý ngoại lệ khỏi die app
        try:
            img = Image.open(file)
            s = self.detector.predict(img)
            print(s)
            return s
        except Exception as error:
            QMessageBox.about(None, "Error", "Cho ảnh hay load config vào đi bạn ơi : {}".format(error))
            print("err: ", error)
            return error

    def run_btn(self):
        print("run_thoi")

    def stop_btn(self):
        print("Dừng mauuuu")
    # train

    def setting_train(self):
        print("setting train")

    def run_train(self):
        config = Cfg.load_config_from_name('vgg_transformer')
        vocab_file_path = "./vocab.txt"
        vocab_file = TextFile(vocab_file_path)
        try:
            vocab = vocab_file.readFile()[0] + "\r\n"
        except:
            vocab = ""

        dataset_params = {
            'name': 'hw',
            'data_root': './ink_dataset/',
            'train_annotation': 'train_annotation.txt',
            'valid_annotation': 'test_annotation.txt'
        }

        params = {
            'batch_size': 16,
            'print_every': 10,
            'valid_every': 200,
            'iters': self.iters,
            'checkpoint': './checkpoint/transformerocr_checkpoint.pth',
            'export': './weights/transformerocr.pth',
            'metrics': 1000
        }

        dataloader_params = {
            'num_workers': 0,
            'pin_memory': True
        }
        config['dataloader'].update(dataloader_params)
        config['trainer'].update(params)
        config['dataset'].update(dataset_params)
        config['device'] = 'cuda:0'

        config['vocab'] = vocab

        print(config)
        trainer = Trainer(config, pretrained=False)

        trainer.config.save('config.yml')

        trainer.visualize_dataset()

        trainer.train()

        trainer.visualize_prediction()

        trainer.precision()
        print("run train")

    def stop_train(self):
        print("stop_train")

    def logshow(self, text):
        with open('log.txt', 'a', encoding="utf-8") as file:
            file.write(text)

    def loading_config(self):
        self.config = Cfg.load_config_from_name('vgg_transformer')  # sử dụng config mặc định của mình
        self.config['weights'] = './weights/transformerocr.pth'  # đường dẫn đến trọng số đã huấn luyện hoặc comment để sử dụng pretrained model của mình
        self.config['device'] = 'cuda:0'  # device chạy 'cuda:0', 'cuda:1', 'cpu'
        self.detector = Predictor(self.config)
        img = Image.open("Welcome.png")
        s = self.detector.predict(img)
        QMessageBox.about(None, "Thông Báo", "Load config đã xong")

