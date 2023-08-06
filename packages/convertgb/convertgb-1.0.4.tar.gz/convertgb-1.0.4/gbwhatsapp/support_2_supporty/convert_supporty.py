import os
import shutil
import codecs
import glob
import argparse
import time

extends = ["smali", "xml"]
blacklist = ['.idea', '.git', 'build', 'assets', 'kotlin', 'lib', 'META-INF', 'original', 'apktool.yml']
data_map = {}


def change_support_2_supporty(OOO0O0OOOOO0OO0OO):
    OOOO000O0OO00000O = glob.glob(f"{OOO0O0OOOOO0OO0OO}/smali/android/support/**/*.smali", recursive=True)
    for OOOOO0O0O0O00OO00 in OOOO000O0OO00000O:
        O0OOO00OOOOO00000 = OOOOO0O0O0O00OO00
        OOO0O0OOOOOOO00O0 = OOOOO0O0O0O00OO00.replace("android/support", "android/supporty")
        OO00OO00OOOOOOO00 = os.path.dirname(OOO0O0OOOOOOO00O0)
        if not os.path.exists(OO00OO00OOOOOOO00):
            os.makedirs(OO00OO00OOOOOOO00, exist_ok=True)
        shutil.move(OOOOO0O0O0O00OO00, OOO0O0OOOOOOO00O0)
        set_data_map(OOO0O0OOOOO0OO0OO, O0OOO00OOOOO00000, OOO0O0OOOOOOO00O0)


def set_data_map(OOOO000OOO0O000O0, OOOOOOOOO0OO0OO0O, OO00O0OO00O0000OO):
    OOO0OO000O00O0OOO = OOOOOOOOO0OO0OO0O[len(f"{OOOO000OOO0O000O0}/smali") + 1:].split(".")[0]
    O000O00OOOO000OO0 = OOO0OO000O00O0OOO.replace("/", ".")
    O000O0000O000OO00 = OO00O0OO00O0000OO[len(f"{OOOO000OOO0O000O0}/smali") + 1:].split(".")[0]
    O00OO0OO00OO0000O = O000O0000O000OO00.replace("/", ".")
    data_map[OOO0OO000O00O0OOO] = O000O0000O000OO00
    data_map[O000O00OOOO000OO0] = O00OO0OO00OO0000O


def traverse_folder(OOO0OOO000OO00000, O0O0000000000O0O0):
    OOO0000OO0O0000OO = os.listdir(OOO0OOO000OO00000)
    for OOOO00000O0O0O00O in OOO0000OO0O0000OO:
        O0000OOOO0OOOOO0O = str(os.path.join(OOO0OOO000OO00000, OOOO00000O0O0O00O))
        print(O0000OOOO0OOOOO0O)
        if OOOO00000O0O0O00O not in blacklist:
            if os.path.isdir(O0000OOOO0OOOOO0O):
                traverse_folder(O0000OOOO0OOOOO0O, O0O0000000000O0O0)
            elif os.path.isfile(O0000OOOO0OOOOO0O):
                if O0000OOOO0OOOOO0O.split(".")[-1] in extends:
                    save_2_file(O0000OOOO0OOOOO0O, O0O0000000000O0O0)


def save_2_file(O00OO000O0O0O0OO0, OOOO0O000O0O0OOOO):
    with codecs.open(O00OO000O0O0O0OO0, "r", "utf-8") as O0O00OO0O000O0O00:
        OO0O0O0O00OO0000O = O0O00OO0O000O0O00.read()
    with codecs.open(O00OO000O0O0O0OO0, "w", "utf-8") as O0OO0O00O0O0O0000:
        O00O00O0OO0OO0OOO = 0
        for O0OOOO0OOOOO00OO0, OOOOO0O0000O00000 in OOOO0O000O0O0OOOO.items():
            O00O00O0OO0OO0OOO += OO0O0O0O00OO0000O.count(O0OOOO0OOOOO00OO0)
            OO0O0O0O00OO0000O = OO0O0O0O00OO0000O.replace(O0OOOO0OOOOO00OO0, OOOOO0O0000O00000)
        print(r'替换次数：', O00O00O0OO0OO0OOO)
        O0OO0O00O0O0O0000.write(OO0O0O0O00OO0000O)


def convertSupportY(O0O0OOOOO0OO0OOO0):
    OO00OO0OOO0OOO000 = time.time()
    change_support_2_supporty(O0O0OOOOO0OO0OOO0)
    traverse_folder(O0O0OOOOO0OO0OOO0, data_map)
    O000O00OO0O00OO0O = time.time()
    print(f"执行完毕，输出结果保存到：{O0O0OOOOO0OO0OOO0} 共耗时{O000O00OO0O00OO0O - OO00OO0OOO0OOO000} 秒")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("from_dir")
    args = parser.parse_args()
    convertSupportY(args.from_dir)
