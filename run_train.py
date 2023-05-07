from PyQt5 import QtCore
from vietocr.tool.config import Cfg
from vietocr.model.trainer import Trainer
from CommonAssit.FileManager import *


class ThreadClass(QtCore.QThread):
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


