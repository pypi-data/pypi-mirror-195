import argparse
import codecs
import os
import xml.etree.ElementTree as ET

android_scheme = "http://schemas.android.com/apk/res/android"
permission_data_list = []
component_data_list = []
permission_list_diff = []
component_list_diff = []
"""
    主要作用：对比两个AndroidManifest.xml查找不同处，并输出diff到新的xml中。
    from_dir:代码少的目录
    to_dir:代码多的目录
"""


def merge_manifest_diff(O0O0O00O0OOO0O000, O0O0O0O00O000OO0O):
    parse_old_manifest(O0O0O00O0OOO0O000)
    parse_new_manifest(O0O0O0O00O000OO0O)
    save_2_file(O0O0O0O00O000OO0O)


def parse_old_manifest(O00OOO0OO0OOOOO00):
    ET.register_namespace("android", android_scheme)
    OOOO0OO0000O0OO0O = ET.parse(O00OOO0OO0OOOOO00)
    O0O0OOO0OO00OO0O0 = OOOO0OO0000O0OO0O.getroot()
    for O0O0O0OO0OOO000OO in O0O0OOO0OO00OO0O0:
        O0OOOOO0O00O0OO0O = O0O0O0OO0OOO000OO.tag
        if O0OOOOO0O00O0OO0O == "queries":
            permission_data_list.append(O0OOOOO0O00O0OO0O)
            continue
        OOO00OO00000O0OO0 = "{" + android_scheme + "}"
        if O0OOOOO0O00O0OO0O != "application":
            O0OOO0O00OOOO0O0O = O0O0O0OO0OOO000OO.attrib[f"{OOO00OO00000O0OO0}name"]
            permission_data_list.append(O0OOO0O00OOOO0O0O)
        else:
            for O000000O00000OO0O in O0O0O0OO0OOO000OO:
                O0OOO000O0OO0OO00 = O000000O00000OO0O.attrib[f"{OOO00OO00000O0OO0}name"]
                component_data_list.append(O0OOO000O0OO0OO00)


def parse_new_manifest(O0O000O0O0OOOO00O):
    ET.register_namespace("android", android_scheme)
    OOOO000OOOO0OOOOO = ET.parse(O0O000O0O0OOOO00O)
    O0O0OOO00O000OO0O = OOOO000OOOO0OOOOO.getroot()
    for OO000OO0O0OO0OOOO in O0O0OOO00O000OO0O:
        OO0O0OO00OOOOO000 = OO000OO0O0OO0OOOO.tag
        if OO0O0OO00OOOOO000 == "queries":
            if OO0O0OO00OOOOO000 not in permission_data_list:
                permission_list_diff.append(OO000OO0O0OO0OOOO)
            continue
        OO0OOOOO0O0000000 = "{" + android_scheme + "}"
        OOO0O0O000OOO000O = OO000OO0O0OO0OOOO.attrib[f"{OO0OOOOO0O0000000}name"]
        OO0O0O0O0OO0O0OO0 = OOO0O0O000OOO000O.replace("whatsapp", "gbwhatsapp")
        if OO0O0OO00OOOOO000 != "application":
            if OOO0O0O000OOO000O not in permission_data_list and OO0O0O0O0OO0O0OO0 not in permission_data_list:
                permission_list_diff.append(OO000OO0O0OO0OOOO)
        else:
            for OO0O00OOO000OOO0O in OO000OO0O0OO0OOOO:
                OOO0O0O00O0000OOO = OO0O00OOO000OOO0O.attrib[f"{OO0OOOOO0O0000000}name"]
                OOOO000OO0O000OOO = OOO0O0O00O0000OOO.replace("gbwhatsapp", "whatsapp")
                if OOO0O0O00O0000OOO not in component_data_list and OOOO000OO0O000OOO not in component_data_list:
                    component_list_diff.append(OO0O00OOO000OOO0O)


def save_2_file(OOOOOO000OOO0O000):
    OOOOOO0O0O000O0O0 = 'xmlns:android="http://schemas.android.com/apk/res/android"'
    O00O00OO0OO000O00: str = '<?xml version="1.0" encoding="utf-8"?>\n<manifest>\n '
    for O00O0OO0O000O000O in permission_list_diff:
        O00O00OO0OO000O00 += "    " + ET.tostring(O00O0OO0O000O000O, encoding='utf-8').decode('utf-8').strip().replace(
            ' />', '/>')
        O00O00OO0OO000O00 = O00O00OO0OO000O00.replace(f'{OOOOOO0O0O000O0O0} ', "")
        O00O00OO0OO000O00 = O00O00OO0OO000O00.replace(OOOOOO0O0O000O0O0, "")
        O00O00OO0OO000O00 += '\n'
    O00O00OO0OO000O00 += '    <application>\n'
    for OOO0OO0OOOO000OOO in component_list_diff:
        O00O00OO0OO000O00 += "        " + ET.tostring(OOO0OO0OOOO000OOO, encoding='utf-8').decode(
            'utf-8').strip().replace(' />', '/>')
        O00O00OO0OO000O00 = O00O00OO0OO000O00.replace(f'{OOOOOO0O0O000O0O0} ', "")
        O00O00OO0OO000O00 = O00O00OO0OO000O00.replace(OOOOOO0O0O000O0O0, "")
        O00O00OO0OO000O00 += '\n'
    O00O00OO0OO000O00 += '    </application>\n</manifest>\n'
    O0O0O0OOOO00OO0OO = OOOOOO000OOO0O000
    if os.path.exists(O0O0O0OOOO00OO0OO):
        O00O0O0OOOOOOO00O = os.path.dirname(O0O0O0OOOO00OO0OO)
        O0O0O0OOOO00OO0OO = f"{O00O0O0OOOOOOO00O}/AndroidManifest_diff.xml"
    with codecs.open(O0O0O0OOOO00OO0OO, mode="w", encoding="utf-8") as O0OOO00O000OOO0OO:
        O0OOO00O000OOO0OO.write(O00O00OO0OO000O00)
    print(f"输出AndroidManifest.xml diff完成，保存到{O0O0O0OOOO00OO0OO}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("fro_dir")
    parser.add_argument("to_dir")
    args = parser.parse_args()
    merge_manifest_diff(args.fro_dir, args.to_dir)
