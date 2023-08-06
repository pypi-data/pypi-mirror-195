import argparse
import codecs
import os
import re

extends = ["smali"]
blacklist = ['.idea', '.git', 'build', 'assets', 'kotlin', 'lib', 'META-INF', 'original', 'res', 'unknown',
             'AndroidManifest.xml', 'apktool.yml', 'smali_classes5', 'smali_classes6', 'smali_classes7']
find_file_list = []
targetStr = "[Landroid/content/pm/Signature;"
code1 = """
    invoke-static {{}}, Lcom/gbwhatsapp/yo/yo;->getYoSig()[Landroid/content/pm/Signature;

    move-result-object {register}
"""
code2 = """
    invoke-static {}, Lcom/gbwhatsapp/yo/yo;->getYoSig()[Landroid/content/pm/Signature;
    """


def find_file(O0O00O0O00000OOO0, O0OO00O0OOOOO0OOO, OO0OOO0OOOOO0O0O0):
    OO0OO00OO0OOOO0O0 = os.listdir(O0O00O0O00000OOO0)
    for OO0OO00OOO0O0O00O in OO0OO00OO0OOOO0O0:
        OO0OO000O00OOOO0O = str(os.path.join(O0O00O0O00000OOO0, OO0OO00OOO0O0O00O))
        if OO0OO00OOO0O0O00O not in blacklist:
            if os.path.isdir(OO0OO000O00OOOO0O):
                find_file(OO0OO000O00OOOO0O, O0OO00O0OOOOO0OOO, OO0OOO0OOOOO0O0O0)
            elif os.path.isfile(OO0OO000O00OOOO0O):
                if OO0OO000O00OOOO0O.split('.')[-1] in extends:
                    with codecs.open(OO0OO000O00OOOO0O, mode="r", encoding="utf-8") as O0O0O00OO0O000O00:
                        O0000O0O0OOOO0O00 = O0O0O00OO0O000O00.read()
                        if O0000O0O0OOOO0O00.__contains__(O0OO00O0OOOOO0OOO):
                            OO0OOO0OOOOO0O0O0.append(OO0OO000O00OOOO0O)


def insert_code(O0O00O000O000000O):
    for O000OOOO0OOO00O0O in O0O00O000O000000O:
        OO00OO00OO0OO00OO = False
        with codecs.open(O000OOOO0OOO00O0O, mode="r", encoding="utf-8") as OO000OOOO0O0O0000:
            O0OOOO000O0000O0O = list(
                map(lambda OOOO0000OO00OOO0O: OOOO0000OO00OOO0O.replace("\n", ""), OO000OOOO0O0O0000.readlines()))
            for O0000000O00000000 in range(0, len(O0OOOO000O0000O0O)):
                O0OO0OO000O00O0O0 = O0OOOO000O0000O0O[O0000000O00000000].strip()
                if not O0OO0OO000O00O0O0.__contains__(
                        "Lcom/gbwhatsapp/yo/yo;->getYoSig()[Landroid/content/pm/Signature"):
                    if (O0OO0OO000O00O0O0.startswith("sget-object") or O0OO0OO000O00O0O0.startswith(
                            "iget-object")) and O0OO0OO000O00O0O0.endswith("[Landroid/content/pm/Signature;"):
                        OO00OO00OO0OO00OO = True
                        O0O00OOO0O00OO000 = re.findall(r"[v,p]\d+", O0OO0OO000O00O0O0)[0]
                        O0OOO0OO000000OOO = O0OOOO000O0000O0O[O0000000O00000000 + 1]
                        O0OO0OO000O00O0O0 = O0OOO0OO000000OOO.replace(O0OOO0OO000000OOO,
                                                                      code1.format(register=O0O00OOO0O00OO000))
                        O0OOOO000O0000O0O[O0000000O00000000 + 1] = O0OO0OO000O00O0O0
                    if O0OO0OO000O00O0O0.startswith("invoke-static") and O0OO0OO000O00O0O0.endswith(
                            "[Landroid/content/pm/Signature;"):
                        OO00OO00OO0OO00OO = True
                        O0OOO0OO000000OOO = O0OOOO000O0000O0O[O0000000O00000000 + 1]
                        O0OO0OO000O00O0O0 = O0OOO0OO000000OOO.replace(O0OOO0OO000000OOO, code2)
                        O0OOOO000O0000O0O[O0000000O00000000 + 1] = O0OO0OO000O00O0O0
        if OO00OO00OO0OO00OO:
            with open(O000OOOO0OOO00O0O, 'w') as OO0O0OO0000O00O00:
                OO0O0OO0000O00O00.write("\n".join(O0OOOO000O0000O0O))
                print("写入" + O000OOOO0OOO00O0O)


def sign(O00OOOOO0O00OOO0O):
    find_file(O00OOOOO0O00OOO0O, targetStr, find_file_list)
    insert_code(find_file_list)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("from_dir")
    args = parser.parse_args()
    sign(args.from_dir)
