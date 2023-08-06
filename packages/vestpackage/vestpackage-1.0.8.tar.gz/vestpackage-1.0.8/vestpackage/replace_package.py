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


def load_replace_keys(OOOOO0O00OOO00OO0, O0OOOO00OO00OOO0O):
    O0O000OOO0OOO0O00 = "L" + OOOOO0O00OOO00OO0.replace(".", "/")
    O0000O0OOO00000OO = "L" + O0OOOO00OO00OOO0O.replace(".", "/")
    OO00OO000OO0O000O = [(OOOOO0O00OOO00OO0, O0OOOO00OO00OOO0O), (O0O000OOO0OOO0O00, O0000O0OOO00000OO)]
    print(OO00OO000OO0O000O)
    return OO00OO000OO0O000O


def execute_path(OOO0OOO00OOOO000O, O000OOOO00OOOO0O0, OOO00O0O0OOO000O0, O0O0O0O000O00O0O0):
    os.chdir(OOO0OOO00OOOO000O)
    OOOO0OO000OO0O0O0 = os.getcwd()
    OOOO0000OOO0OOO0O = os.listdir(OOOO0OO000OO0O0O0)
    for OO0O000OO0OO0O0O0 in OOOO0000OOO0OOO0O:
        if OO0O000OO0OO0O0O0 not in O000OOOO00OOOO0O0:
            OOO0O0000OOO00OO0 = os.path.join(OOOO0OO000OO0O0O0, OO0O000OO0OO0O0O0)
            if os.path.isfile(OOO0O0000OOO00OO0):
                print('fpath=', OOO0O0000OOO00OO0)
                if OOO0O0000OOO00OO0.split('.')[-1] in OOO00O0O0OOO000O0:
                    with codecs.open(OOO0O0000OOO00OO0, "r", "utf-8") as OO000OOOO0OO0000O:
                        O0OOO00000000000O = OO000OOOO0OO0000O.read()
                    with codecs.open(OOO0O0000OOO00OO0, "w", "utf-8") as O00O000OO000O0O00:
                        O0O0OO0O0O0O0OO00 = 0
                        for OO00O00O00OO0O0O0 in O0O0O0O000O00O0O0:
                            O0O0OO0O0O0O0OO00 += O0OOO00000000000O.count(OO00O00O00OO0O0O0[0])
                            O0OOO00000000000O = O0OOO00000000000O.replace(OO00O00O00OO0O0O0[0], OO00O00O00OO0O0O0[1])
                        print(r'替换次数：', O0O0OO0O0O0O0OO00)
                        O00O000OO000O0O00.write(O0OOO00000000000O)
            elif os.path.isdir(OOO0O0000OOO00OO0):
                execute_path(OOO0O0000OOO00OO0, blacklist, OOO00O0O0OOO000O0, O0O0O0O000O00O0O0)


def rename_directory(OOO000O0O000OO000, OOO0O0OO0OOO0OOOO, OO0OO00OO0O000000):
    OOO0O0OO0OOO0OOOO = OOO0O0OO0OOO0OOOO.replace(".", "/")
    OO0OO00OO0O000000 = OO0OO00OO0O000000.replace(".", "/")
    O00OOOO0O0O0OO0O0 = glob.glob(f"{OOO000O0O000OO000}/**/com/{OOO0O0OO0OOO0OOOO}/**")
    for OO0O0000OO0OOO0O0 in O00OOOO0O0O0OO0O0:
        O0000OO000O0O0OOO = OO0O0000OO0OOO0O0.split(OOO000O0O000OO000)[1]
        OO00O00O0O0OOOO00 = O0000OO000O0O0OOO.replace(OOO0O0OO0OOO0OOOO, OO0OO00OO0O000000)
        O0O0OOOOO0OOOOOO0 = f"{OOO000O0O000OO000}/{OO00O00O0O0OOOO00}"
        OO0O0O000O00OOO0O = os.path.dirname(O0O0OOOOO0OOOOOO0)
        if not os.path.exists(OO0O0O000O00OOO0O):
            os.makedirs(OO0O0O000O00OOO0O, exist_ok=True)
        shutil.move(OO0O0000OO0OOO0O0, O0O0OOOOO0OOOOOO0)
    if OOO0O0OO0OOO0OOOO != OO0OO00OO0O000000:
        OOO0O0OO0OOO0OOOO = OOO0O0OO0OOO0OOOO.split("/")[0]
        O0OOOO00OO0OOOO00 = glob.glob(f"{OOO000O0O000OO000}/**/com/{OOO0O0OO0OOO0OOOO}")
        for O0OOOO0000O00OOO0 in O0OOOO00OO0OOOO00:
            removeDir(O0OOOO0000O00OOO0)


def removeDir(O000OO0O0O0O0O0OO):
    OO0O00O0O000OO0OO = os.listdir(O000OO0O0O0O0O0OO)
    for OOO0OO0OO0O0OO00O in OO0O00O0O000OO0OO:
        OO00O0000OOO0O00O = os.path.join(O000OO0O0O0O0O0OO, OOO0OO0OO0O0OO00O)
        if os.path.isdir(OO00O0000OOO0O00O):
            shutil.rmtree(OO00O0000OOO0O00O, ignore_errors=True)
    os.rmdir(O000OO0O0O0O0O0OO)


def getFolderName(OOO00OO0OOO0OO0OO):
    O00OOO000O0O0OO0O = OOO00OO0OOO0OO0OO.split(".")
    OOOOO0O0OO00OOOO0 = O00OOO000O0O0OO0O[-1]
    if len(O00OOO000O0O0OO0O) > 2:
        OOOOO0O0OO00OOOO0 = OOO00OO0OOO0OO0OO[len(O00OOO000O0O0OO0O[0]) + 1:]
    return OOOOO0O0OO00OOOO0


def main():
    O00O000O00OO000OO = argparse.ArgumentParser()
    O00O000O00OO000OO.add_argument("folder_path")
    O0OO000O0O0O0O00O = O00O000O00OO000OO.parse_args()
    O00O0OOOOOOO00OO0 = O0OO000O0O0O0O00O.folder_path
    O00OO000O0OOOO000 = input(
        '请输入默认包名对应的数字：1->com.gbwhatsapp", "2->com.nouncebeats.otavia",' ' "3->com.universe.messenger",\n"4->com.obwhatsapp", "5->com.WhatsApp2Plus", ' '"6->com.yowhatsapp", "7->com.whatsapp""8->其他包名"\n')
    if O00OO000O0OOOO000.strip() == "8":
        O0O000000O0OO000O = input('请输入默认包名：\n')
        default_package_list.append(O0O000000O0OO000O.strip())
    OO0OOO0000O0000O0 = input(
        '请输入新包名对应的数字：1->com.gbwhatsapp", "2->com.nouncebeats.otavia",' ' "3->com.universe.messenger",\n"4->com.obwhatsapp", "5->com.WhatsApp2Plus", ' '"6->com.yowhatsapp", "7->com.whatsapp""8->其他包名"\n')
    if OO0OOO0000O0000O0.strip() == "8":
        O00O0O0OOOO0O00OO = input('请输入新包名：\n')
        new_package_list.append(O00O0O0OOOO0O00OO.strip())
    O000OO0OO00OOOO0O = int(O00OO000O0OOOO000) - 1
    O00O0O00O00OO0OO0 = int(OO0OOO0000O0000O0) - 1
    OOOOO0OO0O0O0OOOO = default_package_list[O000OO0OO00OOOO0O]
    O0OOO0OOOO00OOO0O = new_package_list[O00O0O00O00OO0OO0]
    O000OOOOO0O00O0O0 = load_replace_keys(OOOOO0OO0O0O0OOOO, O0OOO0OOOO00OOO0O)
    execute_path(O00O0OOOOOOO00OO0, blacklist, extends, O000OOOOO0O00O0O0)
    O0OOO0OO0OO00O0O0 = getFolderName(OOOOO0OO0O0O0OOOO)
    O0OOO0OOOO00OOO0O = getFolderName(O0OOO0OOOO00OOO0O)
    rename_directory(O00O0OOOOOOO00OO0, O0OOO0OO0OO00O0O0, O0OOO0OOOO00OOO0O)
    print(f"执行完毕，输出结果保存到{O00O0OOOOOOO00OO0}")


if __name__ == '__main__':
    main()
