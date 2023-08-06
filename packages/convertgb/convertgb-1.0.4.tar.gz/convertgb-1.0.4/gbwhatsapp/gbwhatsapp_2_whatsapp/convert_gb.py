import argparse
import codecs
import glob
import os
import shutil
import time
import xml.etree.ElementTree as ET

dir_path = ""
smali_1_folder_list = []
smali_2_folder_list = []
default_folder_name = "gbwhatsapp"
new_folder_name = "whatsapp"
smali_folder_list = []
smali_classes2_folder_list = []
extends = ["smali", "xml"]
blacklist = ['.idea', '.git', 'build', 'assets', 'kotlin', 'lib', 'META-INF', 'original', 'apktool.yml']


def get_data_list(O0O000O0O00O00OO0):
    OO00O000OOO0O0OOO = ET.parse(O0O000O0O00O00OO0)
    O0000OOO0OO00OOO0 = OO00O000OOO0O0OOO.getroot()
    OOO0O0OO00O0O0OOO = []
    for O0000O00OO0OO0O0O in O0000OOO0OO00OOO0:
        OOO0O0OO00O0O0OOO.append(O0000O00OO0OO0O0O.text)
    return OOO0O0OO00O0O0OOO


def get_correct_path(O0OOO0O00000O00OO, O0O0OOOO0OOOO00OO):
    OO0OO0O0OO000000O = O0OOO0O00000O00OO[len(dir_path) + 1:]
    O00OOOOOOOO0O0O0O = f'{dir_path}/{O0O0OOOO0OOOO00OO}{OO0OO0O0OO000000O[OO0OO0O0OO000000O.index("/"):]}'
    return O00OOOOOOOO0O0O0O


def start_move_file(O0O0O00O0O00000O0, O000OO0OO0O00OO00, O00O0OO00OO00O00O):
    OOOOOOO000OO0O0O0 = False
    O00000O00OO0O0O00 = O000OO0OO0O00OO00.replace(default_folder_name, new_folder_name)
    if O0O0O00O0O00000O0 in smali_1_folder_list:
        O00000O00OO0O0O00 = get_correct_path(O00000O00OO0O0O00, "smali")
        create_folder(O000OO0OO0O00OO00, O00000O00OO0O0O00)
        if O00O0OO00OO00O00O:
            if os.path.exists(O000OO0OO0O00OO00):
                shutil.move(O000OO0OO0O00OO00, O00000O00OO0O0O00)
        else:
            smali_folder_list.append(O000OO0OO0O00OO00)
        OOOOOOO000OO0O0O0 = True
    elif O0O0O00O0O00000O0 in smali_2_folder_list:
        O00000O00OO0O0O00 = get_correct_path(O00000O00OO0O0O00, "smali_classes2")
        create_folder(O000OO0OO0O00OO00, O00000O00OO0O0O00)
        if O00O0OO00OO00O00O:
            if os.path.exists(O000OO0OO0O00OO00):
                shutil.move(O000OO0OO0O00OO00, O00000O00OO0O0O00)
        else:
            smali_classes2_folder_list.append(O000OO0OO0O00OO00)
        OOOOOOO000OO0O0O0 = True
    return OOOOOOO000OO0O0O0


def create_folder(OO0OOOO000OO00O00, OOO0O0O00OO0OOO00):
    if os.path.isdir(OO0OOOO000OO00O00):
        if not os.path.exists(OOO0O0O00OO0OOO00):
            os.makedirs(OOO0O0O00OO0OOO00, exist_ok=True)
    elif os.path.isfile(OO0OOOO000OO00O00):
        OOO00O0OOO000O0O0 = os.path.dirname(OOO0O0O00OO0OOO00)
        if not os.path.exists(OOO00O0OOO000O0O0):
            os.makedirs(OOO00O0OOO000O0O0, exist_ok=True)


def traverse_folder(O0OOO0OOOO0O0000O):
    OOO0O0O00OO00O000 = os.listdir(O0OOO0OOOO0O0000O)
    for O0OOOO0O0000OOO00 in OOO0O0O00OO00O000:
        O0000O0OO00OO00O0 = str(os.path.join(O0OOO0OOOO0O0000O, O0OOOO0O0000OOO00))
        O000O0O0OO00O0OO0 = False
        if O0000O0OO00OO00O0.__contains__("smali"):
            if os.path.isdir(O0000O0OO00OO00O0):
                if O0000O0OO00OO00O0.__contains__(default_folder_name):
                    O00O000OO0OOO00O0 = len(O0000O0OO00OO00O0.split(default_folder_name)) - 1
                    O0OOOO0O0000OOO00 = default_folder_name + O0000O0OO00OO00O0.split(default_folder_name)[
                        O00O000OO0OOO00O0]
                    O000O0O0OO00O0OO0 = start_move_file(O0OOOO0O0000OOO00, O0000O0OO00OO00O0, False)
                if O000O0O0OO00O0OO0:
                    continue
                else:
                    traverse_folder(O0000O0OO00OO00O0)
            elif os.path.isfile(O0000O0OO00OO00O0):
                if O0000O0OO00OO00O0.__contains__(default_folder_name):
                    O00O000OO0OOO00O0 = len(O0000O0OO00OO00O0.split(default_folder_name)) - 1
                    O0OOOO0O0000OOO00 = default_folder_name + O0000O0OO00OO00O0.split(default_folder_name)[
                        O00O000OO0OOO00O0]
                    start_move_file(O0OOOO0O0000OOO00, O0000O0OO00OO00O0, True)
        else:
            continue


def moveFile_2_target_folder(OO0OO0O0O0O00O00O, O00OO000000O0O0O0):
    ""
    O0OOO0O0000O00O0O = os.listdir(OO0OO0O0O0O00O00O)
    for OO000O0O000OOO000 in O0OOO0O0000O00O0O:
        O0O0OOOOO0OO0O0OO = str(os.path.join(OO0OO0O0O0O00O00O, OO000O0O000OOO000))
        O0O0O0O00O0OOOOOO = O0O0OOOOO0OO0O0OO.replace(default_folder_name, new_folder_name)
        if os.path.isdir(O0O0OOOOO0OO0O0OO):
            moveFile_2_target_folder(O0O0OOOOO0OO0O0OO, O00OO000000O0O0O0)
            pass
        elif os.path.isfile(O0O0OOOOO0OO0O0OO):
            if O00OO000000O0O0O0:
                O0O0O0O00O0OOOOOO = get_correct_path(O0O0O0O00O0OOOOOO, "smali")
                create_folder(O0O0OOOOO0OO0O0OO, O0O0O0O00O0OOOOOO)
                shutil.move(O0O0OOOOO0OO0O0OO, O0O0O0O00O0OOOOOO)
            else:
                O0O0O0O00O0OOOOOO = get_correct_path(O0O0O0O00O0OOOOOO, "smali_classes2")
                create_folder(O0O0OOOOO0OO0O0OO, O0O0O0O00O0OOOOOO)
                shutil.move(O0O0OOOOO0OO0O0OO, O0O0O0O00O0OOOOOO)


def get_package_map(OO0O0OO0OOOOOO0O0):
    O0OO0O00O00O0OOO0 = {}
    O0O000000OOOO00OO = OO0O0OO0OOOOOO0O0[0:OO0O0OO0OOOOOO0O0.rindex(".")]
    O0O00OOOO0OO0OO00 = O0O000000OOOO00OO.replace("/", ".")
    OOO00O0000O0OO0OO = O0O000000OOOO00OO.replace(new_folder_name, default_folder_name)
    O0O000000000OO0OO = O0O00OOOO0OO0OO00.replace(new_folder_name, default_folder_name)
    O0OO0O00O00O0OOO0[f"L{OOO00O0000O0OO0OO}"] = f"L{O0O000000OOOO00OO}"
    O0OO0O00O00O0OOO0[O0O000000000OO0OO] = O0O00OOOO0OO0OO00
    return O0OO0O00O00O0OOO0


def replace_package():
    O00O0OO0O00OO0000 = glob.glob(f"{dir_path}/smali*/com/{new_folder_name}/**/*.smali", recursive=True)
    O0O0OO0O0OO00OO0O = {}
    for OOOO0O000O0O0O000 in O00O0OO0O00OO0000:
        OOOOO00OOO0O0OOOO = f"{dir_path}/smali_classes2"
        if OOOO0O000O0O0O000.__contains__(OOOOO00OOO0O0OOOO):
            O0000O00O00O00O0O = OOOO0O000O0O0O000[len(OOOOO00OOO0O0OOOO) + 1:]
            OO00OO000O000OOOO = get_package_map(O0000O00O00O00O0O)
            for O0O0O0O0O00OO00OO, O00000000O0OOO00O in OO00OO000O000OOOO.items():
                O0O0OO0O0OO00OO0O[O0O0O0O0O00OO00OO] = O00000000O0OOO00O
        else:
            O0000O00O00O00O0O = OOOO0O000O0O0O000[len(f"{dir_path}/smali") + 1:]
            OO00OO000O000OOOO = get_package_map(O0000O00O00O00O0O)
            for O0O0O0O0O00OO00OO, O00000000O0OOO00O in OO00OO000O000OOOO.items():
                O0O0OO0O0OO00OO0O[O0O0O0O0O00OO00OO] = O00000000O0OOO00O
    if len(O0O0OO0O0OO00OO0O) > 0:
        traverse_folder_replace_package(dir_path, O0O0OO0O0OO00OO0O)


def traverse_folder_replace_package(OO0OOOOO000O0O000, OOO0000O00OO0O0OO):
    OO0O0OO00O00OO0O0 = os.listdir(OO0OOOOO000O0O000)
    for O0O0O0OOOOO00OO00 in OO0O0OO00O00OO0O0:
        OOOO00O0OOOOO0000 = str(os.path.join(OO0OOOOO000O0O000, O0O0O0OOOOO00OO00))
        if O0O0O0OOOOO00OO00 not in blacklist:
            if os.path.isdir(OOOO00O0OOOOO0000):
                traverse_folder_replace_package(OOOO00O0OOOOO0000, OOO0000O00OO0O0OO)
            elif os.path.isfile(OOOO00O0OOOOO0000):
                if OOOO00O0OOOOO0000.split('.')[-1] in extends:
                    print('fpath=', OOOO00O0OOOOO0000)
                    if O0O0O0OOOOO00OO00 == "AndroidManifest.xml":
                        save_2_xml(OOOO00O0OOOOO0000, OOO0000O00OO0O0OO)
                    else:
                        save_2_file(OOOO00O0OOOOO0000, OOO0000O00OO0O0OO)


def save_2_xml(OOOOOOOO0OOO0OO0O, O000O0000000OO00O):
    ET.register_namespace('android', "http://schemas.android.com/apk/res/android")
    O0O0OO0OOO0O0OOOO = ET.parse(OOOOOOOO0OOO0OO0O)
    O0OO0OOOOOOO0O00O = ET.tostring(O0O0OO0OOO0O0OOOO.getroot(), encoding="utf-8").decode('utf-8').replace(' />', '/>')
    O0OO0OOOOOOO0O00O = f'<?xml version="1.0" encoding="utf-8" standalone="no"?>{O0OO0OOOOOOO0O00O}'
    with codecs.open(OOOOOOOO0OOO0OO0O, "w", "utf-8") as OO0O0000O00O0000O:
        OO0OO000OO0OOOO00 = 0
        for OOO000000OOO00O00, OOOOOOO000OO0OO0O in O000O0000000OO00O.items():
            OO0OO000OO0OOOO00 += O0OO0OOOOOOO0O00O.count(OOO000000OOO00O00)
            O0OO0OOOOOOO0O00O = O0OO0OOOOOOO0O00O.replace(OOO000000OOO00O00, OOOOOOO000OO0OO0O)
        print(r'替换次数：', OO0OO000OO0OOOO00)
        OO0O0000O00O0000O.write(O0OO0OOOOOOO0O00O)


def save_2_file(OO0O00O0O00O0O00O, OOO0O00O0O0O00OOO):
    with codecs.open(OO0O00O0O00O0O00O, "r", "utf-8") as OOOO00O00OOO0OO00:
        OO00OO0O00OO00OO0 = OOOO00O00OOO0OO00.read()
    with codecs.open(OO0O00O0O00O0O00O, "w", "utf-8") as OO00OO0O0O0O0O0OO:
        O000O0OO00000O0OO = 0
        for O0O0O000O0O0OO0O0, OOOO00OO000OOOOO0 in OOO0O00O0O0O00OOO.items():
            O000O0OO00000O0OO += OO00OO0O00OO00OO0.count(O0O0O000O0O0OO0O0)
            OO00OO0O00OO00OO0 = OO00OO0O00OO00OO0.replace(O0O0O000O0O0OO0O0, OOOO00OO000OOOOO0)
        print(r'替换次数：', O000O0OO00000O0OO)
        OO00OO0O0O0O0O0OO.write(OO00OO0O00OO00OO0)


def convert_2_whatsapp():
    traverse_folder(dir_path)
    for O00O0O0O00OOO0O00 in smali_folder_list:
        moveFile_2_target_folder(O00O0O0O00OOO0O00, True)
    for O00O0O0O00OOO0O00 in smali_classes2_folder_list:
        moveFile_2_target_folder(O00O0O0O00OOO0O00, False)
    replace_package()


def convertGB(OO0OO00OO000OO0O0, O0OO00000000OO0OO):
    global dir_path, smali_1_folder_list, smali_2_folder_list
    dir_path = OO0OO00OO000OO0O0
    OO00O00O000O00OO0 = time.time()
    smali_1_folder_list = get_data_list(f"{O0OO00000000OO0OO}/gbwhatsapp/gbwhatsapp_2_whatsapp/smali.xml")
    smali_2_folder_list = get_data_list(f"{O0OO00000000OO0OO}/gbwhatsapp/gbwhatsapp_2_whatsapp/smali_classes2.xml")
    convert_2_whatsapp()
    O0000O0O0O0OOOO0O = time.time()
    print(f"执行完毕，输出结果保存到：{dir_path} 共耗时{O0000O0O0O0OOOO0O - OO00O00O000O00OO0} 秒")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("from_dir")
    args = parser.parse_args()
    convertGB(args.from_dir, os.getcwd())
