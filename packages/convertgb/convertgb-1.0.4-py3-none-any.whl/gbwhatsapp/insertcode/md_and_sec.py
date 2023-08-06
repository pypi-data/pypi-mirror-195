import codecs
import os
import argparse

extends = ["smali"]
blacklist = ['.idea', '.git', 'build', 'assets', 'kotlin', 'lib', 'META-INF', 'original', 'res', 'unknown',
             'AndroidManifest.xml', 'apktool.yml', 'smali_classes5', 'smali_classes6', 'smali_classes7']
find_file_list = []
targetStr = "PkTwKSZqUfAUyR0rPQ8hYJ0wNsQQ3dW1+3SCnyTXIfEAxxS75FwkDf47wNv/c8pP3p0GXKR6OOQmhyERwx74fw1RYSU10I4r1gyBVDbRJ40pidjM41G1I1oN"
code1 = """
    invoke-static {}, Lcom/gbwhatsapp/yo/yo;->sec()Ljavax/crypto/SecretKey;
    """
code2 = """
    invoke-static {}, Lcom/gbwhatsapp/yo/yo;->md()[B
    """


def find_file(OOOOO00OOO0OO0OO0, OOOO0O0O00O0O0O0O, O0OO0O0OOO0OOO00O):
    O00O00O0000O00OO0 = os.listdir(OOOOO00OOO0OO0OO0)
    for OO00OO0O0OOO00OOO in O00O00O0000O00OO0:
        OO0OO00OOOOOO0OOO = str(os.path.join(OOOOO00OOO0OO0OO0, OO00OO0O0OOO00OOO))
        if OO00OO0O0OOO00OOO not in blacklist:
            if os.path.isdir(OO0OO00OOOOOO0OOO):
                find_file(OO0OO00OOOOOO0OOO, OOOO0O0O00O0O0O0O, O0OO0O0OOO0OOO00O)
            elif os.path.isfile(OO0OO00OOOOOO0OOO):
                if OO0OO00OOOOOO0OOO.split('.')[-1] in extends:
                    with codecs.open(OO0OO00OOOOOO0OOO, mode="r", encoding="utf-8") as O0OOO0O00OO000000:
                        OO00OO00O0O0OOOO0 = O0OOO0O00OO000000.read()
                        if OO00OO00O0O0OOOO0.__contains__(OOOO0O0O00O0O0O0O):
                            O0OO0O0OOO0OOO00O.append(OO0OO00OOOOOO0OOO)


def insert_code(OO00O0OOOO00O000O):
    for OOO0OO0O0O00OOO00 in OO00O0OOOO00O000O:
        OO00OOO00OOOO0OO0 = False
        with codecs.open(OOO0OO0O0O00OOO00, mode="r", encoding="utf-8") as O00O0O0O0O0O00000:
            O0O0OOO00O000O00O = list(
                map(lambda OOOOOO0O000OOO000: OOOOOO0O000OOO000.replace("\n", ""), O00O0O0O0O0O00000.readlines()))
            for O00O0000OOO0O0O0O in range(0, len(O0O0OOO00O000O00O)):
                OOOOOO0OOO0O0OOO0 = str(O0O0OOO00O000O00O[O00O0000OOO0O0O0O]).rstrip()
                if OOOOOO0OOO0O0OOO0.endswith("([B[BII)Ljavax/crypto/SecretKey;"):
                    OOOOOO0OOO0O0OOO0 = str(O0O0OOO00O000O00O[O00O0000OOO0O0O0O + 2])
                    if OOOOOO0OOO0O0OOO0.__contains__("move-result"):
                        OO00OOO00OOOO0OO0 = True
                        O0OO00OO0OOO00O00 = O0O0OOO00O000O00O[O00O0000OOO0O0O0O + 1]
                        OOOOOO0OOO0O0OOO0 = O0OO00OO0OOO00O00.replace(str(O0O0OOO00O000O00O[O00O0000OOO0O0O0O + 1]),
                                                                      code1)
                        O0O0OOO00O000O00O[O00O0000OOO0O0O0O + 1] = OOOOOO0OOO0O0OOO0
                elif OOOOOO0OOO0O0OOO0.endswith("(Landroid/content/Context;)[B"):
                    OOOOOO0OOO0O0OOO0 = str(O0O0OOO00O000O00O[O00O0000OOO0O0O0O + 2])
                    if OOOOOO0OOO0O0OOO0.__contains__("move-result"):
                        OO00OOO00OOOO0OO0 = True
                        O0OO00OO0OOO00O00 = O0O0OOO00O000O00O[O00O0000OOO0O0O0O + 1]
                        OOOOOO0OOO0O0OOO0 = O0OO00OO0OOO00O00.replace(O0OO00OO0OOO00O00, code2)
                        O0O0OOO00O000O00O[O00O0000OOO0O0O0O + 1] = OOOOOO0OOO0O0OOO0
        if OO00OOO00OOOO0OO0:
            with open(OOO0OO0O0O00OOO00, 'w') as OO0OOO0O0O0O00000:
                OO0OOO0O0O0O00000.write("\n".join(O0O0OOO00O000O00O))
                print("写入" + OOO0OO0O0O00OOO00)


def sign(OOOO0O0OOOOO0O0OO):
    find_file(OOOO0O0OOOOO0O0OO, targetStr, find_file_list)
    insert_code(find_file_list)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("from_dir")
    args = parser.parse_args()
    sign(args.from_dir)
