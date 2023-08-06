import os
import argparse
import lxml.etree as ET
import codecs
import shutil

blacklist = ['.idea', '.git', 'build', 'lib', 'META-INF', "res", 'original', 'AndroidManifest.xml', 'apktool.yml']
android_scheme = "http://schemas.android.com/apk/res/android"
strDict = {"market://details?id=com.gbwhatsapp.w4b&utm_source=": "market://details?id=com.whatsapp.w4b&utm_source=",
           "com.gbwhatsapp.sticker.READ": "com.whatsapp.sticker.READ"}


def replaceManifest(O00OOOOO00OO0OO00):
    ET.register_namespace('android', android_scheme)
    OO00000OOO000OOO0 = ET.parse(O00OOOOO00OO0OO00)
    OOO0OOO000O0OO0OO = OO00000OOO000OOO0.getroot()
    O00OOO00O0OOOOO0O = OOO0OOO000O0OO0OO.attrib
    OO00000000OOOOOO0 = "{" + android_scheme + "}"
    O00OOO00O0OOOOO0O[OO00000000OOOOOO0 + "compileSdkVersion"] = "23"
    O00OOO00O0OOOOO0O[OO00000000OOOOOO0 + "compileSdkVersionCodename"] = "6.0-2438415"
    O00OOO00O0OOOOO0O["platformBuildVersionCode"] = "31"
    O00OOO00O0OOOOO0O["platformBuildVersionName"] = "12"
    for O0O0O0OOO0000O0O0 in OOO0OOO000O0OO0OO:
        O0000OOO000O00O00 = O0O0O0OOO0000O0O0.attrib
        OO00000O000O00OO0 = O0O0O0OOO0000O0O0.tag
        if OO00000O000O00OO0 == "queries":
            queries(O0O0O0OOO0000O0O0, OO00000000OOOOOO0)
        elif OO00000O000O00OO0 == "uses-permission":
            O0OO00O0OO000OO0O = O0000OOO000O00O00.get(OO00000000OOOOOO0 + "name")
            if not O0OO00O0OO000OO0O is None and O0OO00O0OO000OO0O == "com.gbwhatsapp.sticker.READ":
                O0000OOO000O00O00[OO00000000OOOOOO0 + "name"] = "com.whatsapp.sticker.READ"
        elif OO00000O000O00OO0 == "application":
            for O0OO0OOOOOOO0OO0O in O0O0O0OOO0000O0O0:
                OOOO0OO0O0OO00OOO = O0OO0OOOOOOO0OO0O.attrib
                O00000O0O0OO000OO = OOOO0OO0O0OO00OOO.get(OO00000000OOOOOO0 + "name")
                if O0OO0OOOOOOO0OO0O.tag == "activity" and not O00000O0O0OO000OO is None and O00000O0O0OO000OO.__contains__(
                        "AddThirdPartyStickerPackActivity"):
                    for O00OOO00OO00O00OO in O0OO0OOOOOOO0OO0O:
                        for O0OO0OOOOOOO0OO0O in O00OOO00OO00O00OO:
                            if O0OO0OOOOOOO0OO0O.tag == "action":
                                O0O0000O0OOOOO0O0 = O0OO0OOOOOOO0OO0O.attrib.get(OO00000000OOOOOO0 + "name")
                                if not O0O0000O0OOOOO0O0 is None:
                                    O0OO0OOOOOOO0OO0O.attrib[OO00000000OOOOOO0 + "name"] = O0O0000O0OOOOO0O0.replace(
                                        "gbwhatsapp", "whatsapp")
    O0O000000O0O0OO00 = ET.tostring(OOO0OOO000O0OO0OO, encoding="utf-8").decode('utf-8').replace(' />', '/>')
    O0000O00O000O0O00 = f'<?xml version="1.0" encoding="utf-8" standalone="no"?>{O0O000000O0O0OO00}'
    write_2_file(O00OOOOO00OO0OO00, O0000O00O000O0O00)


def queries(O00O0O0O0OOO000O0, O0OOO00O0OO0O0O00):
    for OO00O000OO000000O in O00O0O0O0OOO000O0:
        O0O000O00O0OOO00O = OO00O000OO000000O.attrib.get(O0OOO00O0OO0O0O00 + "authorities")
        if OO00O000OO000000O.tag == "provider" and not O0O000O00O0OOO00O is None and O0O000O00O0OOO00O.__contains__(
                ".car.app.connection"):
            OO00O000OO000000O.attrib[O0OOO00O0OO0O0O00 + "name"] = "com.gbwhatsapp.car.app.connection"


def write_2_file(OOO000O0OO0OOOOOO, OOOO0OO000OOOO00O):
    try:
        with codecs.open(OOO000O0OO0OOOOOO, mode='w+', encoding="utf-8") as OOOOOOOOOO0O000OO:
            OOOOOOOOOO0O000OO.write(OOOO0OO000OOOO00O)
    except Exception as O00O00OOO0000000O:
        print(f"写入{OOO000O0OO0OOOOOO}异常: {O00O00OOO0000000O}")


def replaceApktool(OOO0OOOO00000O0O0):
    with codecs.open(OOO0OOOO00000O0O0, "r", "utf-8") as OO0000O0O00OO0O00:
        OO00000OOO00OO0O0 = OO0000O0O00OO0O00.readlines()
    with codecs.open(OOO0OOOO00000O0O0, "w", "utf-8") as OOO0OO00O0OOOO0OO:
        OO0O0O0OO00000O0O = ""
        global pos
        OOO00OO000OO0O0OO = len(OO00000OOO00OO0O0)
        for OOOOOO00OO00OO000 in range(OOO00OO000OO0O0OO):
            O0OOOO0O0O00OO0OO = OO00000OOO00OO0O0[OOOOOO00OO00OO000]
            if O0OOOO0O0O00OO0OO.__contains__("- resources.arsc"):
                continue
            elif O0OOOO0O0O00OO0OO.__contains__("- png"):
                OOOOO000O00O00O00 = "#resources.arsc\n#- png\n"
                OO0O0O0OO00000O0O += OOOOO000O00O00O00
            elif O0OOOO0O0O00OO0OO.__contains__("targetSdkVersion"):
                OOOOO000O00O00O00 = "  targetSdkVersion: '29'\n"
                OO0O0O0OO00000O0O += OOOOO000O00O00O00
            elif O0OOOO0O0O00OO0OO.__contains__("unknownFiles:"):
                OOOOO000O00O00O00 = "unknownFiles: {}\n"
                OO0O0O0OO00000O0O += OOOOO000O00O00O00
                pos = OOOOOO00OO00OO000
                break
            else:
                OO0O0O0OO00000O0O += O0OOOO0O0O00OO0OO
        for OOOOOO00OO00OO000 in range(pos, len(OO00000OOO00OO0O0)):
            O0OOOO0O0O00OO0OO = OO00000OOO00OO0O0[OOOOOO00OO00OO000]
            if O0OOOO0O0O00OO0OO.__contains__("usesFramework:"):
                pos = OOOOOO00OO00OO000
                break
        for OOOOOO00OO00OO000 in range(pos, len(OO00000OOO00OO0O0)):
            O0OOOO0O0O00OO0OO = OO00000OOO00OO0O0[OOOOOO00OO00OO000]
            OO0O0O0OO00000O0O += O0OOOO0O0O00OO0OO
        OOO0OO00O0OOOO0OO.write(OO0O0O0OO00000O0O)


def transFolderReplaceStr(O00OO0O0OOO0OOO00):
    OOOO000000OO0OOO0 = os.listdir(O00OO0O0OOO0OOO00)
    for OO0O0O000000O0O00 in OOOO000000OO0OOO0:
        OO00O0OOOO0OO00OO = os.path.join(O00OO0O0OOO0OOO00, OO0O0O000000O0O00)
        if not OO0O0O000000O0O00 in blacklist:
            if os.path.isdir(OO00O0OOOO0OO00OO):
                if OO0O0O000000O0O00 == "unknown":
                    shutil.rmtree(OO00O0OOOO0OO00OO, ignore_errors=True)
                else:
                    transFolderReplaceStr(OO00O0OOOO0OO00OO)
            elif os.path.isfile(OO00O0OOOO0OO00OO):
                if OO0O0O000000O0O00.split(".")[-1] == "smali":
                    with codecs.open(OO00O0OOOO0OO00OO, "r", "utf-8") as OO000OOO0O0OO0O0O:
                        O0OO000O000O000OO = OO000OOO0O0OO0O0O.read()
                    with codecs.open(OO00O0OOOO0OO00OO, "w", "utf-8") as O000O00000OO0O00O:
                        for O0O0000OOOOO00OOO, O0OOO0OO0O0O0OOO0 in strDict.items():
                            O0OO000O000O000OO = O0OO000O000O000OO.replace(O0O0000OOOOO00OOO, O0OOO0OO0O0O0OOO0)
                        O000O00000OO0O00O.write(O0OO000O000O000OO)


def moveFiles(O0OO000OO0OO0000O, O00OOOO000OOOOO00):
    if not os.path.exists(O0OO000OO0OO0000O):
        os.makedirs(O0OO000OO0OO0000O, exist_ok=True)
    O000O0OO0000OO000 = f"{O00OOOO000OOOOO00}/gbwhatsapp/yo"
    O000OOOOO0OOO0OOO = os.listdir(O000O0OO0000OO000)
    for OO00O0OOO0O000OOO in O000OOOOO0OOO0OOO:
        O00OO0000OO0OO000 = os.path.join(O000O0OO0000OO000, OO00O0OOO0O000OOO)
        O0O0OO0O00OO0OOO0 = os.path.join(O0OO000OO0OO0000O, OO00O0OOO0O000OOO)
        shutil.copy(O00OO0000OO0OO000, O0O0OO0O00OO0OOO0)


def other(O00OOOOO0OOO000OO, O0O000OO0OOOOOO00):
    replaceManifest(f"{O00OOOOO0OOO000OO}/AndroidManifest.xml")
    replaceApktool(f"{O00OOOOO0OOO000OO}/apktool.yml")
    transFolderReplaceStr(O00OOOOO0OOO000OO)
    moveFiles(f"{O00OOOOO0OOO000OO}/smali_classes5/gbwhatsapp/yo", O0O000OO0OOOOOO00)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("from_dir")
    args = parser.parse_args()
    from_dir = args.from_dir
    other(from_dir, os.getcwd())
