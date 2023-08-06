import os
import shutil
import codecs
import glob
import argparse
import time

extends = ["smali", "xml"]
blacklist = ['.idea', '.git', 'build', 'assets', 'kotlin', 'lib', 'META-INF', 'original', 'apktool.yml']
data_map = {}


def change_support_2_supporty(OOOOO00OO00O000O0):
    OO000O00O00O0O00O = glob.glob(f"{OOOOO00OO00O000O0}/smali/android/support/**/*.smali", recursive=True)
    for OO0O000000O00000O in OO000O00O00O0O00O:
        O00O00OOO0000000O = OO0O000000O00000O
        OOOOO00O000OOO0OO = OO0O000000O00000O.replace("android/support", "android/supporty")
        OO00OO0OO0O00O0OO = os.path.dirname(OOOOO00O000OOO0OO)
        if not os.path.exists(OO00OO0OO0O00O0OO):
            os.makedirs(OO00OO0OO0O00O0OO, exist_ok=True)
        shutil.move(OO0O000000O00000O, OOOOO00O000OOO0OO)
        set_data_map(OOOOO00OO00O000O0, O00O00OOO0000000O, OOOOO00O000OOO0OO)


def set_data_map(O0O00O00O0000OOOO, O0OOOO0OOOOOOO0OO, OO00OOOOOOO000OO0):
    O000O0O000O0OOOOO = O0OOOO0OOOOOOO0OO[len(f"{O0O00O00O0000OOOO}/smali") + 1:].split(".")[0]
    O00OOOOO000O0OOOO = O000O0O000O0OOOOO.replace("/", ".")
    O00O0OO00O0OO0O0O = OO00OOOOOOO000OO0[len(f"{O0O00O00O0000OOOO}/smali") + 1:].split(".")[0]
    O0O00000OOO000O0O = O00O0OO00O0OO0O0O.replace("/", ".")
    data_map[O000O0O000O0OOOOO] = O00O0OO00O0OO0O0O
    data_map[O00OOOOO000O0OOOO] = O0O00000OOO000O0O


def traverse_folder(OOOOOOO000O000OOO, O0O00O00O0O00OOOO):
    O0O0O00O00OOOO00O = os.listdir(OOOOOOO000O000OOO)
    for OOOO0O0O0OO000OOO in O0O0O00O00OOOO00O:
        OO0O00000O0OOO000 = str(os.path.join(OOOOOOO000O000OOO, OOOO0O0O0OO000OOO))
        print(OO0O00000O0OOO000)
        if OOOO0O0O0OO000OOO not in blacklist:
            if os.path.isdir(OO0O00000O0OOO000):
                traverse_folder(OO0O00000O0OOO000, O0O00O00O0O00OOOO)
            elif os.path.isfile(OO0O00000O0OOO000):
                if OO0O00000O0OOO000.split(".")[-1] in extends:
                    save_2_file(OO0O00000O0OOO000, O0O00O00O0O00OOOO)


def save_2_file(O000O0OO0O000OO0O, OOO000OO00OOOOOO0):
    with codecs.open(O000O0OO0O000OO0O, "r", "utf-8") as OO00O00O000OO0OO0:
        OO00OOO0O0OO0O00O = OO00O00O000OO0OO0.read()
    with codecs.open(O000O0OO0O000OO0O, "w", "utf-8") as O0OO00OOOOOO00000:
        O00OO0O000O0O0OOO = 0
        for O0OO00O0OO00O0OO0, O000O00000O0OO0O0 in OOO000OO00OOOOOO0.items():
            O00OO0O000O0O0OOO += OO00OOO0O0OO0O00O.count(O0OO00O0OO00O0OO0)
            OO00OOO0O0OO0O00O = OO00OOO0O0OO0O00O.replace(O0OO00O0OO00O0OO0, O000O00000O0OO0O0)
        print(r'替换次数：', O00OO0O000O0O0OOO)
        O0OO00OOOOOO00000.write(OO00OOO0O0OO0O00O)


def convertSupportY(O0O00000OO0OO00O0):
    O00O0O0OOOOOOOOOO = time.time()
    change_support_2_supporty(O0O00000OO0OO00O0)
    traverse_folder(O0O00000OO0OO00O0, data_map)
    O00OOOO000O0O0O0O = time.time()
    print(f"执行完毕，输出结果保存到：{O0O00000OO0OO00O0} 共耗时{O00OOOO000O0O0O0O - O00O0O0OOOOOOOOOO} 秒")


def main():
    O0OOO0OOOO00000O0 = argparse.ArgumentParser()
    O0OOO0OOOO00000O0.add_argument("from_dir")
    O0000O00OO0O0OO0O = O0OOO0OOOO00000O0.parse_args()
    convertSupportY(O0000O00OO0O0OO0O.from_dir)


if __name__ == "__main__":
    main()
