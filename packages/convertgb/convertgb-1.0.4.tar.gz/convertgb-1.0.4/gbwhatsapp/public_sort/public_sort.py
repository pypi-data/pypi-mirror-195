import argparse
import codecs
import functools
import traceback
import xml.etree.ElementTree as ET

public_data_list = []


class PublicEntity:
    public_type = ""
    public_name = ""
    public_id = 0

    def __init__(O00OO0OO0O0000OOO, O0OOO0O0OOO00O00O, OOOO0000OOOOO0OO0, OO00OO0000O00OOO0):
        O00OO0OO0O0000OOO.public_type = O0OOO0O0OOO00O00O
        O00OO0OO0O0000OOO.public_name = OOOO0000OOOOO0OO0
        O00OO0OO0O0000OOO.public_id = int(OO00OO0000O00OOO0, 16)

    def __repr__(OOO0OO00O00OOO0OO) -> str:
        return f'<public type="{OOO0OO00O00OOO0OO.public_type}" name="{OOO0OO00O00OOO0OO.public_name}"id="{hex(OOO0OO00O00OOO0OO.public_id)}" />'


def sort_func(O00OO00OOOO0O0O00, OOO0000OOOOOO0OO0):
    O0OOOO0000O00OOOO = O00OO00OOOO0O0O00.public_id
    O0OO0000000000O0O = OOO0000OOOOOO0OO0.public_id
    if O0OOOO0000O00OOOO > O0OO0000000000O0O:
        return 1
    elif O0OOOO0000O00OOOO < O0OO0000000000O0O:
        return -1
    else:
        OOO00O0O0O0O0OOO0 = f'资源ID出现重复,请重新命名：<public type="{OOO0000OOOOOO0OO0.public_type}" name="{OOO0000OOOOOO0OO0.public_name}" id="{OOO0000OOOOOO0OO0.public_id}" />'
        raise Exception(OOO00O0O0O0O0OOO0)


def public_sort(OO0O000OO000OOOO0):
    OO000O00O000O0000 = f"{OO0O000OO000OOOO0}/res/values/public.xml"
    O0OOO000OO00O0OOO = ET.parse(OO000O00O000O0000)
    O0000O00O0O0O0O0O = O0OOO000OO00O0OOO.getroot()
    for OOO0O00000OOO0O0O in O0000O00O0O0O0O0O:
        O00OO00OOO00OOOOO: str = OOO0O00000OOO0O0O.attrib["type"]
        OOO00OOO0O00O0O00: str = OOO0O00000OOO0O0O.attrib["name"]
        OOOO0OO00OO0O0O0O: str = OOO0O00000OOO0O0O.attrib["id"]
        if OOOO0OO00OO0O0O0O.startswith("0x"):
            OO0000OO000O0O00O: int
            try:
                OO0000OO000O0O00O = int(OOOO0OO00OO0O0O0O, 16)
            except Exception:
                print(f"错误异常：{traceback.format_exc()}")
                OO0O0OOOO0O0OO0O0 = f'错误原因：资源ID命名错误,：<public type="{O00OO00OOO00OOOOO}" name="{OOO00OOO0O00O0O00}" id="{OOOO0OO00OO0O0O0O}" />'
                raise Exception(OO0O0OOOO0O0OO0O0)
            if OO0000OO000O0O00O <= int("0xffffffff", 16):
                OOO0OO0OO000O0000 = PublicEntity(O00OO00OOO00OOOOO, OOO00OOO0O00O0O00, OOOO0OO00OO0O0O0O)
                public_data_list.append(OOO0OO0OO000O0000)
            else:
                OO0O0OOOO0O0OO0O0 = f'错误原因：资源ID超过最大值0xffffffff,请重新命名资源ID数值：<public type="{O00OO00OOO00OOOOO}" name="{OOO00OOO0O00O0O00}" id="{OOOO0OO00OO0O0O0O}" />'
                raise Exception(OO0O0OOOO0O0OO0O0)
        else:
            OO0O0OOOO0O0OO0O0 = f'错误原因：资源ID请以0x命名,：<public type="{O00OO00OOO00OOOOO}" name="{OOO00OOO0O00O0O00}" id="{OOOO0OO00OO0O0O0O}" />'
            raise Exception(OO0O0OOOO0O0OO0O0)
    public_data_list.sort(key=functools.cmp_to_key(sort_func))


def save_to_file(O0O0O0OOOOOOOO000, OO00OO00O000O0OO0):
    print(OO00OO00O000O0OO0)
    with codecs.open(OO00OO00O000O0OO0, "w+", encoding="utf-8") as O0OO0O0OOOOO0O0OO:
        O0OO0O0OOOOO0O0OO.write('<?xml version="1.0" encoding="utf-8"?>\n')
        O0OO0O0OOOOO0O0OO.write('<resources>\n')
        for OOOOOOOOOO0O0OOO0 in O0O0O0OOOOOOOO000:
            O0OO0O0OOOOO0O0OO.write(
                f'    <public type="{OOOOOOOOOO0O0OOO0.public_type}" name="{OOOOOOOOOO0O0OOO0.public_name}" id="{hex(OOOOOOOOOO0O0OOO0.public_id)}" />\n')
        O0OO0O0OOOOO0O0OO.write('</resources>')


def sort(O000O0000OO0OO0O0):
    public_sort(O000O0000OO0OO0O0)
    O00OO0OOO00OOOOO0 = O000O0000OO0OO0O0 + "/res/values/public.xml"
    save_to_file(public_data_list, O00OO0OOO00OOOOO0)
    print(f"public.xml排序完成,排序结果保存到:{O00OO0OOO00OOOOO0}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("from_path")
    args = parser.parse_args()
    sort(args.from_path)
