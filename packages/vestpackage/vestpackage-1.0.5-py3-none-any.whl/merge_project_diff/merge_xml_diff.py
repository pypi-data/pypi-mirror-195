import argparse
import glob
import os
import re
import shutil
import traceback
import lxml.etree as ET
import merge_project_diff.merge_public

reStr = "APKTOOL_.*_0x\w{8}"
"""
    对比两个不同项目values目录下xml不同，
    查找diff不同处，并把diff复制到对应目标文件。
"""


def traverse_folder(OOOO00O000OOO00OO, OOO00OO000O0OOO0O):
    O00O0OO00OOOOOOOO = os.sep + "res" + os.sep + "values*" + os.sep + "**"
    OOOO0O00OOOO0000O = glob.glob(OOOO00O000OOO00OO + O00O0OO00OOOOOOOO)
    for O00OO00O00O0OOOO0 in OOOO0O00OOOO0000O:
        O00O00000O0O0O00O = os.path.basename(O00OO00O00O0OOOO0)
        OOO00O0OOOOOOOOO0 = O00OO00O00O0OOOO0[len(OOO00OO000O0OOO0O):O00OO00O00O0OOOO0.rindex(os.sep)]
        O0OO0O0000O0OO0OO = OOO00OO000O0OOO0O + os.sep + "res" + os.sep + OOO00O0OOOOOOOOO0
        O0O0O00O0OO00OOOO = str(O0OO0O0000O0OO0OO) + os.sep + O00O00000O0O0O00O
        if not os.path.exists(O0OO0O0000O0OO0OO):
            os.makedirs(O0OO0O0000O0OO0OO, exist_ok=True)
            shutil.copy(O00OO00O00O0OOOO0, O0OO0O0000O0OO0OO)
        merge_diff(O00OO00O00O0OOOO0, O0O0O00O0OO00OOOO)


def merge_diff(OOO00O0OOO0O00000, O00OO0O00OO00O0OO):
    if not os.path.isfile(O00OO0O00OO00O0OO):
        shutil.copy(OOO00O0OOO0O00000, O00OO0O00OO00O0OO)
    else:
        OOO0OO000O0O0O0O0 = os.path.basename(OOO00O0OOO0O00000)
        OOOO0OO0000O0O00O = ET.parse(O00OO0O00OO00O0OO)
        OOOOO00O0OO00O0OO = OOOO0OO0000O0O00O.getroot()
        O00O0O0OOOOOOOO00 = {}
        O000OO00O00000O00 = []
        for OO00OOOO0OO0O000O in OOOOO00O0OO00O0OO:
            O0OO0OO0OO0OOO0OO = OO00OOOO0OO0O000O.attrib
            OOOO00000OO00OO00 = O0OO0OO0OO0OOO0OO.get("name")
            if OOOO00000OO00OO00 is not None:
                if OOOO00000OO00OO00.__contains__("APKTOOL") and not re.match(reStr, OOOO00000OO00OO00):
                    continue
                else:
                    if OOO0OO000O0O0O0O0 == "public.xml":
                        O00OO000O0O000O00 = O0OO0OO0OO0OOO0OO.get("type")
                        OOOO00000OO00OO00 = f"{OOOO00000OO00OO00}#{O00OO000O0O000O00}"
                    O00O0O0OOOOOOOO00[OOOO00000OO00OO00] = OO00OOOO0OO0O000O
        O0O00O00O0O00O0OO = ET.parse(OOO00O0OOO0O00000)
        O0OO0OOO0OOO00O00 = O0O00O00O0O00O0OO.getroot()
        O0O0O0000O0OOO00O: bool = False
        for O0O0O000OO0O0O0OO in O0OO0OOO0OOO00O00:
            O00OO0000O0O0OO00 = O0O0O000OO0O0O0OO.attrib
            O0OOO0O00O00OO00O = O00OO0000O0O0OO00.get("name")
            if O0OOO0O00O00OO00O is not None:
                if O0OOO0O00O00OO00O.__contains__("APKTOOL") and not re.match(reStr, O0OOO0O00O00OO00O):
                    continue
                else:
                    if OOO0OO000O0O0O0O0 == "public.xml":
                        OOO00OOO0O0O0O00O = O00OO0000O0O0OO00.get("type")
                        O0OOO0O00O00OO00O = f"{O0OOO0O00O00OO00O}#{OOO00OOO0O0O0O00O}"
                    if O0OOO0O00O00OO00O not in O00O0O0OOOOOOOO00.keys():
                        OOOOO00O0OO00O0OO.append(O0O0O000OO0O0O0OO)
                        O000OO00O00000O00.append(O0O0O000OO0O0O0OO)
                        O0O0O0000O0OOO00O = True
        if O0O0O0000O0OOO00O:
            OO0OOO000OO000OOO = convert_str(OOOOO00O0OO00O0OO)
            if os.path.basename(O00OO0O00OO00O0OO) == "public.xml":
                merge_project_diff.merge_public.copy_attrs(OOO00O0OOO0O00000, O00OO0O00OO00O0OO)
            else:
                save_2_file(OO0OOO000OO000OOO, O00OO0O00OO00O0OO)


def merge_diff_attrs(OOOO0OO00OO0OO0OO, O00OOOO00O0000O0O, OO0O0O0O00OO0O00O):
    O00O00O0OOOOOOO00 = str(O00OOOO00O0000O0O)
    OO0O0O0O000OO0OOO = f'{OO0O0O0O00OO0O00O}_diff{O00O00O0OOOOOOO00.replace(OO0O0O0O00OO0O00O, "")}'
    O0O0OO0O00OOOOOO0 = os.path.dirname(OO0O0O0O000OO0OOO)
    if not os.path.exists(O00OOOO00O0000O0O):
        if not os.path.exists(O0O0OO0O00OOOOOO0):
            os.makedirs(O0O0OO0O00OOOOOO0, exist_ok=True)
        shutil.copy(OOOO0OO00OO0OO0OO, O0O0OO0O00OOOOOO0)
    else:
        O00OOOO00O00O0OO0 = os.path.basename(OOOO0OO00OO0OO0OO)
        OOOO000OO00000000 = ET.parse(O00OOOO00O0000O0O)
        O000OOO0O0OO0O0O0 = OOOO000OO00000000.getroot()
        O0OO00O0OO0OO00O0 = {}
        OO00O000OOOO0000O = []
        for O0OOO00O000000O00 in O000OOO0O0OO0O0O0:
            OO0OO0000OOOOOO0O = O0OOO00O000000O00.attrib
            OO0O0OO0000OOO00O = OO0OO0000OOOOOO0O.get("name")
            if OO0O0OO0000OOO00O is not None:
                if OO0O0OO0000OOO00O.__contains__("APKTOOL") and not re.match(reStr, OO0O0OO0000OOO00O):
                    continue
                else:
                    if O00OOOO00O00O0OO0 == "public.xml":
                        OO0000O0OO0O000O0 = OO0OO0000OOOOOO0O.get("type")
                        OO0O0OO0000OOO00O = f"{OO0O0OO0000OOO00O}#{OO0000O0OO0O000O0}"
                    O0OO00O0OO0OO00O0[OO0O0OO0000OOO00O] = O0OOO00O000000O00
        O0OOOOO0O0OOO0OOO = ET.parse(OOOO0OO00OO0OO0OO)
        OO0OOO00OO00OO00O = O0OOOOO0O0OOO0OOO.getroot()
        OO0O00000OO0OOO00: bool = False
        for OO00O00OOOOO000O0 in OO0OOO00OO00OO00O:
            OO000O000OOOOO0O0 = OO00O00OOOOO000O0.attrib
            OO0O000O0O00O00OO = OO000O000OOOOO0O0.get("name")
            if OO0O000O0O00O00OO is not None:
                if OO0O000O0O00O00OO.__contains__("APKTOOL") and not re.match(reStr, OO0O000O0O00O00OO):
                    continue
                else:
                    if O00OOOO00O00O0OO0 == "public.xml":
                        OO0O0OOOOOOO00OOO = OO000O000OOOOO0O0.get("type")
                        OO0O000O0O00O00OO = f"{OO0O000O0O00O00OO}#{OO0O0OOOOOOO00OOO}"
                    if OO0O000O0O00O00OO not in O0OO00O0OO0OO00O0.keys():
                        OO00O000OOOO0000O.append(OO00O00OOOOO000O0)
                        OO0O00000OO0OOO00 = True
        if OO0O00000OO0OOO00:
            O0000000OO0OOO0OO = convert_str(OO00O000OOOO0000O)
            if not os.path.exists(O0O0OO0O00OOOOOO0):
                os.makedirs(O0O0OO0O00OOOOOO0, exist_ok=True)
            save_2_file(O0000000OO0OOO0OO, OO0O0O0O000OO0OOO)


def convert_str(OO00OO0O0000O0O0O):
    OOO0OOO00O0O0O00O: str = '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
    O00000000000O0000 = len(OO00OO0O0000O0O0O)
    for O0O00O0OO0OO00O0O, OOO00OOOOO0O00OO0 in enumerate(OO00OO0O0000O0O0O):
        O0OO00O0O0O000OO0 = OOO00OOOOO0O00OO0.tag
        OOO0OOO0O0OOO000O = OOO00OOOOO0O00OO0.text
        OOO0OOO00O0O0O00O += "    "
        if (O0OO00O0O0O000OO0 == "string" and str(OOO0OOO0O0OOO000O).__contains__(
                ">")) or O0OO00O0O0O000OO0 == "plurals":
            OOOOO000OO0OOOOO0 = ET.tostring(OOO00OOOOO0O00OO0, encoding="utf-8").decode('utf-8').strip().replace('&gt;',
                                                                                                                 '>')
            OOO0OOO00O0O0O00O += OOOOO000OO0OOOOO0
        else:
            OOO0OOO00O0O0O00O += ET.tostring(OOO00OOOOO0O00OO0, encoding='utf-8').decode('utf-8').strip().replace('/>',
                                                                                                                  ' />')
        if O0O00O0OO0OO00O0O < O00000000000O0000 - 1:
            OOO0OOO00O0O0O00O += '\n'
    OOO0OOO00O0O0O00O += '\n</resources>\n'
    return OOO0OOO00O0O0O00O


def save_2_file(OO0OO0OOO0OO000OO, O0OO0000OO00000OO):
    try:
        with open(O0OO0000OO00000OO, 'w+') as O0OO0O0O0O000OO00:
            O0OO0O0O0O000OO00.write(OO0OO0OOO0OO000OO)
    except Exception as OO00O0O00O00OO00O:
        print(f"写入{O0OO0000OO00000OO}出现异常: {OO00O0O00O00OO00O}")
        print(traceback.format_exc())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("project_from_dir")
    parser.add_argument("project_to_dir")
    args = parser.parse_args()
    traverse_folder(args.project_from_dir, args.project_to_dir)
