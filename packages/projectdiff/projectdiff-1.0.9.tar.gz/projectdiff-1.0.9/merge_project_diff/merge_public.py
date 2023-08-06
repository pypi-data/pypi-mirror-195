import argparse
import codecs
import re
import lxml.etree as ET

"""
    主要作用：比较两个public.xml不同,
    并把新增属性输出到目标文件中
"""
max_dict = {}
name_dict = {}


def copy_attrs(OO000O0OO0O0OOO0O, OOO0OO0O0000000O0):
    OOO000000OOOOOO00 = ET.parse(OOO0OO0O0000000O0)
    O000O00000000OOO0 = OOO000000OOOOOO00.getroot()
    for O0OO00O0OO000O0O0 in O000O00000000OOO0:
        if O0OO00O0OO000O0O0.tag == "public" and "id" in O0OO00O0OO000O0O0.attrib:
            O0O00OO00OO0O000O = str(O0OO00O0OO000O0O0.attrib['name']).strip()
            OO00O000OOO00O00O = O0OO00O0OO000O0O0.attrib['type'].strip()
            OO0000O000OOO00OO = O0OO00O0OO000O0O0.attrib['id'].strip()
            if OO00O000OOO00O00O not in name_dict:
                name_dict[OO00O000OOO00O00O] = set()
            name_dict[OO00O000OOO00O00O].add(O0O00OO00OO0O000O)
            OO000000O0O0O0OOO = int(OO0000O000OOO00OO, 16)
            if OO00O000OOO00O00O in max_dict:
                if OO000000O0O0O0OOO > int(max_dict[OO00O000OOO00O00O].attrib['id'], 16):
                    max_dict[OO00O000OOO00O00O] = O0OO00O0OO000O0O0
            else:
                max_dict[OO00O000OOO00O00O] = O0OO00O0OO000O0O0
    OOOOO0OOOO0O00000 = ET.parse(OO000O0OO0O0OOO0O)
    OOOO000OOO0O0OO0O = OOOOO0OOOO0O00000.getroot()
    for O0OO00O0OO000O0O0 in OOOO000OOO0O0OO0O:
        if O0OO00O0OO000O0O0.tag == "public" and "id" in O0OO00O0OO000O0O0.attrib:
            OO0O0000OO0O0OO00 = O0OO00O0OO000O0O0.attrib['name'].strip()
            O00O000OOOO0OOO0O = O0OO00O0OO000O0O0.attrib['type'].strip()
            if OO0O0000OO0O0OO00.__contains__("APKTOOL") and not re.match(r"APKTOOL_.*_0x\w{8}", OO0O0000OO0O0OO00):
                continue
            else:
                if OO0O0000OO0O0OO00 not in name_dict[O00O000OOOO0OOO0O]:
                    O000O000O000000OO = max_dict[O00O000OOOO0OOO0O]
                    O0OO00O0OO000O0O0.set('id', str(hex(int(O000O000O000000OO.attrib['id'], 16) + 1)))
                    max_dict[O00O000OOOO0OOO0O] = O0OO00O0OO000O0O0
                    OO0OOO0OO00O000OO = O000O00000000OOO0.index(O000O000O000000OO)
                    O000O00000000OOO0.insert(OO0OOO0OO00O000OO + 1, O0OO00O0OO000O0O0)
    save_to_file(O000O00000000OOO0, OOO0OO0O0000000O0)


def save_to_file(O000000O0000O0OO0, O0O000O0000OOO0OO):
    with codecs.open(O0O000O0000OOO0OO, "w+", encoding="utf-8") as OO0OO0OO0O0O00000:
        OO0OO0OO0O0O00000.write('<?xml version="1.0" encoding="utf-8"?>\n')
        OO0OO0OO0O0O00000.write('<resources>\n')
        for O0OOO000OOOO0OO0O in O000000O0000O0OO0:
            OO0OOO0OOO0OO00OO = O0OOO000OOOO0OO0O.attrib
            OO0OO0OO0O0O00000.write(
                f'    <public type="{OO0OOO0OOO0OO00OO["type"]}" name="{OO0OOO0OOO0OO00OO["name"]}" id="{OO0OOO0OOO0OO00OO["id"]}" />\n')
        OO0OO0OO0O0O00000.write('</resources>')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("from_dir")
    parser.add_argument("to_dir")
    options = parser.parse_args()
    copy_attrs(options.from_dir, options.to_dir)
    print(f"输出结果到：{options.to_dir}")
