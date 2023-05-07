from CommonAssit import PathFileControl
from CommonAssit.FileManager import *
from CommonAssit import CommonAssit
import tqdm

vocab_file_path = "./vocab.txt"
image_dir = r"D:\Study\EAUT\KY 4\DACN1\docchuviettay\ink_dataset\test_img"
annotation_path = r"D:\Study\EAUT\KY 4\DACN1\docchuviettay\ink_dataset\test_annotation.txt"
vocab_file = TextFile(vocab_file_path)
annotation_file = TextFile(annotation_path)

try:    vocab = vocab_file.readFile()[0] + " \r\n"
except:
    vocab = ""

def read_all_file_path():
    global vocab
    info_list = []
    image_path_list = CommonAssit.getAllImagePath(image_dir)
    for image_path in tqdm.tqdm(image_path_list):
        image_name = get_image_name(image_path)
        text_info = get_text_inside_image(image_name)
        valid_flag = True
        for _char in text_info:
            if _char not in vocab:
                # vocab += _char
                valid_flag = False
                break
        if not valid_flag:
            continue
        if text_info != "":
            info_list.append(f"{image_path}\t{text_info}")
    return info_list

def get_text_inside_image(image_name):
    text_path = image_name + ".txt"
    text_file = TextFile(text_path)
    text_file.readFile()
    try:
        if len(text_file.dataList) > 0:
            return text_file.dataList[0]
        else:
            return ""
    except Exception as error:
        print(f"ERROR {error}")
        return ""

def get_image_name(image_path: str):
    return image_path[:image_path.rfind(".")]

def add_image_info_into_file(list_name):
    annotation_file.dataList = list_name
    annotation_file.saveFile()

if __name__ == '__main__':
    info_list = read_all_file_path()
    add_image_info_into_file(info_list)

    # vocab_file.dataList = [vocab]
    # vocab_file.saveFile()
    print(vocab)