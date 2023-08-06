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

    def __init__(OO0O0000O0O0OOOO0, OO0000000O00000OO, OO0O00OO0OO0O0000, OO00OOO0O0O0OO00O):
        OO0O0000O0O0OOOO0.public_type = OO0000000O00000OO
        OO0O0000O0O0OOOO0.public_name = OO0O00OO0OO0O0000
        OO0O0000O0O0OOOO0.public_id = int(OO00OOO0O0O0OO00O, 16)

    def __repr__(O00OO0OO000O0OO0O) -> str:
        return f'<public type="{O00OO0OO000O0OO0O.public_type}" name="{O00OO0OO000O0OO0O.public_name}"id="{hex(O00OO0OO000O0OO0O.public_id)}" />'


def sort_func(OOOOO0OOOO00OOO0O, OO0O0O0O0OO000O00):
    OO000O0OOO00O00OO = OOOOO0OOOO00OOO0O.public_id
    OO00OOO000O00O0OO = OO0O0O0O0OO000O00.public_id
    if OO000O0OOO00O00OO > OO00OOO000O00O0OO:
        return 1
    elif OO000O0OOO00O00OO < OO00OOO000O00O0OO:
        return -1
    else:
        O0O0O0O00OOOOO0O0 = f'资源ID出现重复,请重新命名：<public type="{OO0O0O0O0OO000O00.public_type}" name="{OO0O0O0O0OO000O00.public_name}" id="{OO0O0O0O0OO000O00.public_id}" />'
        raise Exception(O0O0O0O00OOOOO0O0)


def public_sort(O00O0O0OO00O000OO):
    O0OOOO0OOO00O0O0O = f"{O00O0O0OO00O000OO}/res/values/public.xml"
    O00O0000000OO0OOO = ET.parse(O0OOOO0OOO00O0O0O)
    O0OOOO0OO00O0OOOO = O00O0000000OO0OOO.getroot()
    for OOOO0OOOO0OO0O0OO in O0OOOO0OO00O0OOOO:
        O0000OO00O0O0O000: str = OOOO0OOOO0OO0O0OO.attrib["type"]
        OO00O0OOO00OO0O0O: str = OOOO0OOOO0OO0O0OO.attrib["name"]
        O00000O000O0OO0OO: str = OOOO0OOOO0OO0O0OO.attrib["id"]
        if O00000O000O0OO0OO.startswith("0x"):
            O000OO0OO000000OO: int
            try:
                O000OO0OO000000OO = int(O00000O000O0OO0OO, 16)
            except Exception:
                print(f"错误异常：{traceback.format_exc()}")
                OO0OOO000OO00OOOO = f'错误原因：资源ID命名错误,：<public type="{O0000OO00O0O0O000}" name="{OO00O0OOO00OO0O0O}" id="{O00000O000O0OO0OO}" />'
                raise Exception(OO0OOO000OO00OOOO)
            if O000OO0OO000000OO <= int("0xffffffff", 16):
                O0OOOOOOOO00000OO = PublicEntity(O0000OO00O0O0O000, OO00O0OOO00OO0O0O, O00000O000O0OO0OO)
                public_data_list.append(O0OOOOOOOO00000OO)
            else:
                OO0OOO000OO00OOOO = f'错误原因：资源ID超过最大值0xffffffff,请重新命名资源ID数值：<public type="{O0000OO00O0O0O000}" name="{OO00O0OOO00OO0O0O}" id="{O00000O000O0OO0OO}" />'
                raise Exception(OO0OOO000OO00OOOO)
        else:
            OO0OOO000OO00OOOO = f'错误原因：资源ID请以0x命名,：<public type="{O0000OO00O0O0O000}" name="{OO00O0OOO00OO0O0O}" id="{O00000O000O0OO0OO}" />'
            raise Exception(OO0OOO000OO00OOOO)
    public_data_list.sort(key=functools.cmp_to_key(sort_func))


def save_to_file(OO0OO0OO0O0OOO000, O0OO0OO00O0OO000O):
    print(O0OO0OO00O0OO000O)
    with codecs.open(O0OO0OO00O0OO000O, "w+", encoding="utf-8") as OOOOOO0O0O0OOO00O:
        OOOOOO0O0O0OOO00O.write('<?xml version="1.0" encoding="utf-8"?>\n')
        OOOOOO0O0O0OOO00O.write('<resources>\n')
        for OO0O00O0000OOOO0O in OO0OO0OO0O0OOO000:
            OOOOOO0O0O0OOO00O.write(
                f'    <public type="{OO0O00O0000OOOO0O.public_type}" name="{OO0O00O0000OOOO0O.public_name}" id="{hex(OO0O00O0000OOOO0O.public_id)}" />\n')
        OOOOOO0O0O0OOO00O.write('</resources>')


def sort(O0O0OOOO000000O0O):
    public_sort(O0O0OOOO000000O0O)
    O0O0OOO00OO00000O = O0O0OOOO000000O0O + "/res/values/public.xml"
    save_to_file(public_data_list, O0O0OOO00OO00000O)
    print(f"public.xml排序完成,排序结果保存到:{O0O0OOO00OO00000O}")


def main():
    O0O00OOOOOO00OO00 = argparse.ArgumentParser()
    O0O00OOOOOO00OO00.add_argument("from_path")
    O0OO0O00000O000O0 = O0O00OOOOOO00OO00.parse_args()
    sort(O0OO0O00000O000O0.from_path)


if __name__ == "__main__":
    main()
