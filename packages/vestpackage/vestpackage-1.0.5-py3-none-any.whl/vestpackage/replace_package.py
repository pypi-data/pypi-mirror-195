import argparse
import codecs
import glob
import os
import shutil

extends = ["smali", "xml", "html"]
blacklist = ['.idea', '.git', 'build', 'lib', 'META-INF', 'original', 'apktool.yml']
default_package_list = ["com.gbwhatsapp", "com.nouncebeats.otavia", "com.universe.messenger", "com.obwhatsapp",
                        "com.WhatsApp2Plus", "com.yowhatsapp", "com.whatsapp"]
new_package_list = default_package_list.copy()
"""
    主要作用：反编译实现马甲包功能；替换默认包名为新包名。
"""


def load_replace_keys(OO0O0OO0OO0O00O00, OO00O0O0OO00O0O00):
    OO0O0OO0O00OO0OOO = "L" + OO0O0OO0OO0O00O00.replace(".", "/")
    O0000O00OOO000OOO = "L" + OO00O0O0OO00O0O00.replace(".", "/")
    O00OOOO00000OOOOO = [(OO0O0OO0OO0O00O00, OO00O0O0OO00O0O00), (OO0O0OO0O00OO0OOO, O0000O00OOO000OOO)]
    print(O00OOOO00000OOOOO)
    return O00OOOO00000OOOOO


def execute_path(O000000OO0O0OOOOO, O000OOO000O0OOO00, O0O0O00O0O0OO0000, OO000OOOO00O0000O):
    os.chdir(O000000OO0O0OOOOO)
    OOOO0O000O00000O0 = os.getcwd()
    OO0OO0OOOO0O0OO00 = os.listdir(OOOO0O000O00000O0)
    for OOOO0OO0000OOOO0O in OO0OO0OOOO0O0OO00:
        if OOOO0OO0000OOOO0O not in O000OOO000O0OOO00:
            O0OOO0OO0O00OO00O = os.path.join(OOOO0O000O00000O0, OOOO0OO0000OOOO0O)
            if os.path.isfile(O0OOO0OO0O00OO00O):
                print('fpath=', O0OOO0OO0O00OO00O)
                if O0OOO0OO0O00OO00O.split('.')[-1] in O0O0O00O0O0OO0000:
                    with codecs.open(O0OOO0OO0O00OO00O, "r", "utf-8") as O00O000OO000O0O0O:
                        O0O0OO00OO0000O00 = O00O000OO000O0O0O.read()
                    with codecs.open(O0OOO0OO0O00OO00O, "w", "utf-8") as OOOOOO00OOOOO0O0O:
                        OOO0OOOO00O0O0000 = 0
                        for OOO0O00O0000OOO00 in OO000OOOO00O0000O:
                            OOO0OOOO00O0O0000 += O0O0OO00OO0000O00.count(OOO0O00O0000OOO00[0])
                            O0O0OO00OO0000O00 = O0O0OO00OO0000O00.replace(OOO0O00O0000OOO00[0],
                                                                          OOO0O00O0000OOO00[1])
                        print(r'替换次数：', OOO0OOOO00O0O0000)
                        OOOOOO00OOOOO0O0O.write(O0O0OO00OO0000O00)
            elif os.path.isdir(O0OOO0OO0O00OO00O):
                execute_path(O0OOO0OO0O00OO00O, blacklist, O0O0O00O0O0OO0000, OO000OOOO00O0000O)


def rename_directory(O0O0000O0O00O0OO0, OOO00OO00O00OOOOO, O0O0OO0O0000000O0):
    OOO00OO00O00OOOOO = OOO00OO00O00OOOOO.replace(".", "/")
    O0O0OO0O0000000O0 = O0O0OO0O0000000O0.replace(".", "/")
    OO00O00O00O0O0000 = glob.glob(f"{O0O0000O0O00O0OO0}/**/com/{OOO00OO00O00OOOOO}/**")
    for OO0000OO00O0000O0 in OO00O00O00O0O0000:
        O0O0O0O0O0OO0O0O0 = OO0000OO00O0000O0.split(O0O0000O0O00O0OO0)[1]
        O0OOOOO0OOOOO00O0 = O0O0O0O0O0OO0O0O0.replace(OOO00OO00O00OOOOO, O0O0OO0O0000000O0)
        OO0OOO0000OO0OOO0 = f"{O0O0000O0O00O0OO0}/{O0OOOOO0OOOOO00O0}"
        OOOO0OO0O000000OO = os.path.dirname(OO0OOO0000OO0OOO0)
        if not os.path.exists(OOOO0OO0O000000OO):
            os.makedirs(OOOO0OO0O000000OO, exist_ok=True)
        shutil.move(OO0000OO00O0000O0, OO0OOO0000OO0OOO0)
    if OOO00OO00O00OOOOO != O0O0OO0O0000000O0:
        OOO00OO00O00OOOOO = OOO00OO00O00OOOOO.split("/")[0]
        OOO0OO0000OO0O0O0 = glob.glob(f"{O0O0000O0O00O0OO0}/**/com/{OOO00OO00O00OOOOO}")
        for OO0OO0OOO000000O0 in OOO0OO0000OO0O0O0:
            removeDir(OO0OO0OOO000000O0)


def removeDir(OO0OO0O0O0OOO0O00):
    OO0OOO0OO00OOO00O = os.listdir(OO0OO0O0O0OOO0O00)
    for O0O0OO0000000O00O in OO0OOO0OO00OOO00O:
        OOOOOOO00O00OO000 = os.path.join(OO0OO0O0O0OOO0O00, O0O0OO0000000O00O)
        if os.path.isdir(OOOOOOO00O00OO000):
            shutil.rmtree(OOOOOOO00O00OO000, ignore_errors=True)
    os.rmdir(OO0OO0O0O0OOO0O00)


def getFolderName(OOO0000O000O0000O):
    OO000O00OOOOO00O0 = OOO0000O000O0000O.split(".")
    OOO0O0OO00OO00000 = OO000O00OOOOO00O0[-1]
    if len(OO000O00OOOOO00O0) > 2:
        OOO0O0OO00OO00000 = OOO0000O000O0000O[len(OO000O00OOOOO00O0[0]) + 1:]
    return OOO0O0OO00OO00000


def main():
    OOOO00O000O0O000O = argparse.ArgumentParser()
    OOOO00O000O0O000O.add_argument("folder_path")
    O0O0OOO0000OO0O00 = OOOO00O000O0O000O.parse_args()
    OOO00000O0O00OO0O = O0O0OOO0000OO0O00.folder_path
    OO000000O00O00OOO = input(
        '请输入默认包名对应的数字：1->com.gbwhatsapp", "2->com.nouncebeats.otavia",' ' "3->com.universe.messenger",\n"4->com.obwhatsapp", "5->com.WhatsApp2Plus", ' '"6->com.yowhatsapp", "7->com.whatsapp""8->其他包名"\n')
    if OO000000O00O00OOO.strip() == "8":
        O0O00OO0OO0OO00O0 = input('请输入默认包名：\n')
        default_package_list.append(O0O00OO0OO0OO00O0.strip())
    OOO0OOOOO0O0O0OOO = input(
        '请输入默认包名对应的数字：1->com.gbwhatsapp", "2->com.nouncebeats.otavia",' ' "3->com.universe.messenger",\n"4->com.obwhatsapp", "5->com.WhatsApp2Plus", ' '"6->com.yowhatsapp", "7->com.whatsapp""8->其他包名"\n')
    if OOO0OOOOO0O0O0OOO.strip() == "8":
        O0OO0O0OO00O000OO = input('请输入新包名：\n')
        new_package_list.append(O0OO0O0OO00O000OO.strip())
    OOOO00O00OO00O0OO = int(OO000000O00O00OOO) - 1
    O000O0OO0000OOOOO = int(OOO0OOOOO0O0O0OOO) - 1
    OO0O0OO0O0OOO0O0O = default_package_list[OOOO00O00OO00O0OO]
    O00OO0OOOOOOOOO00 = new_package_list[O000O0OO0000OOOOO]
    OO00O0OOO000O00O0 = load_replace_keys(OO0O0OO0O0OOO0O0O, O00OO0OOOOOOOOO00)
    execute_path(OOO00000O0O00OO0O, blacklist, extends, OO00O0OOO000O00O0)
    O0OOOOO0OO0O00OOO = getFolderName(OO0O0OO0O0OOO0O0O)
    O00OO0OOOOOOOOO00 = getFolderName(O00OO0OOOOOOOOO00)
    rename_directory(OOO00000O0O00OO0O, O0OOOOO0OO0O00OOO, O00OO0OOOOOOOOO00)
    print(f"执行完毕，输出结果保存到{OOO00000O0O00OO0O}")


if __name__ == '__main__':
    main()
