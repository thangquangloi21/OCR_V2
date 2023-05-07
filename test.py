import sys
# pip install pyqt5, pip install pyqt5 tools
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
# just change the name
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore
import time
from Working_Thread import Working_thread
from View.Qtgui import Ui_Vision_OCR
from vietocr.tool.config import Cfg
from vietocr.model.trainer import Trainer
from CommonAssit.FileManager import *
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic = Ui_Vision_OCR()
        self.uic.setupUi(self)
        self.Working_thread = Working_thread()
        self.thread = {}

        self.uic.Run_Train_Button.clicked.connect(self.start_worker_1)
        self.uic.Stop_Train_Button.clicked.connect(self.stop_worker_1)

    def start_worker_1(self):
        try:
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

class ThreadClass(QtCore.QThread):
    signal = pyqtSignal(int)
    def __init__(self, index=0):
        super().__init__()
        self.index = index

    def run(self):
        print('Starting thread...', self.index)
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
            'iters': 1000,
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

        # print(config)
        trainer = Trainer(config, pretrained=False)

        trainer.config.save('config.yml')

        trainer.visualize_dataset()

        trainer.train()

        trainer.visualize_prediction()

        trainer.precision()

    def stop(self):
        print('Stopping thread...', self.index)
        self.terminate()
        print("Stop trainning perfect")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())