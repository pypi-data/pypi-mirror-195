import argparse
import codecs
import glob
import os
import shutil
import time

extends = ["smali", "xml"]
blacklist = ['.idea', '.git', 'build', 'assets', 'kotlin', 'lib', 'META-INF', 'original', 'apktool.yml']


def change_androidx_2_androidy(O0000O0O0OOOOO0OO):
    OOOOOOO00O00OOOO0 = glob.glob(f"{O0000O0O0OOOOO0OO}/smali/androidx/**/*.smali", recursive=True)
    for OO0O00O0OOOO00O00 in OOOOOOO00O00OOOO0:
        OO0OOO0O0OOO00O00 = OO0O00O0OOOO00O00.replace("androidx", "androidy")
        OOOO00000O0OOO0OO = os.path.dirname(OO0OOO0O0OOO00O00)
        if not os.path.exists(OOOO00000O0OOO0OO):
            os.makedirs(OOOO00000O0OOO0OO, exist_ok=True)
        shutil.move(OO0O00O0OOOO00O00, OO0OOO0O0OOO00O00)


def traverse_folder(OO000000000O00OOO, O0OOOOO0O00000O00):
    OO0OOOO0O0OOO00OO = os.listdir(OO000000000O00OOO)
    for OO0000OOOO0O0000O in OO0OOOO0O0OOO00OO:
        OO0O0O0OO0OOO0OOO = str(os.path.join(OO000000000O00OOO, OO0000OOOO0O0000O))
        print(OO0O0O0OO0OOO0OOO)
        if OO0000OOOO0O0000O not in blacklist:
            if os.path.isdir(OO0O0O0OO0OOO0OOO):
                traverse_folder(OO0O0O0OO0OOO0OOO, O0OOOOO0O00000O00)
            elif os.path.isfile(OO0O0O0OO0OOO0OOO):
                if OO0O0O0OO0OOO0OOO.split(".")[-1] in extends:
                    save_2_file(OO0O0O0OO0OOO0OOO, O0OOOOO0O00000O00)


def save_2_file(O0O00O000OO0O0000, O0OOOOO0OO0000O0O):
    with codecs.open(O0O00O000OO0O0000, "r", "utf-8") as OO000O00O0OO00OOO:
        OO000O0OOO0O000OO = OO000O00O0OO00OOO.read()
    with codecs.open(O0O00O000OO0O0000, "w", "utf-8") as OOO0OOO0000OOOO0O:
        OO0O000OO0OOO000O = 0
        for OO0O00000O000000O, O0OOOO00OOO0OOO0O in O0OOOOO0OO0000O0O.items():
            OO0O000OO0OOO000O += OO000O0OOO0O000OO.count(OO0O00000O000000O)
            OO000O0OOO0O000OO = OO000O0OOO0O000OO.replace(OO0O00000O000000O, O0OOOO00OOO0OOO0O)
        print(r'替换次数：', OO0O000OO0OOO000O)
        OOO0OOO0000OOOO0O.write(OO000O0OOO0O000OO)


def convertAndroidY(OO0OO0000OO000OOO):
    OOO00OO00OOO000O0 = time.time()
    change_androidx_2_androidy(OO0OO0000OO000OOO)
    traverse_folder(OO0OO0000OO000OOO, {"androidx": "androidy"})
    OOO0OO00OOO000OO0 = time.time()
    print(f"执行完毕，输出结果保存到：{OO0OO0000OO000OOO} 共耗时{OOO0OO00OOO000OO0 - OOO00OO00OOO000O0} 秒")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("from_dir")
    args = parser.parse_args()
    convertAndroidY(args.from_dir)
