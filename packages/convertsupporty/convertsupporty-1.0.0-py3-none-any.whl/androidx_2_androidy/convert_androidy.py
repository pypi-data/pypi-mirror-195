import argparse
import codecs
import glob
import os
import shutil
import time

extends = ["smali", "xml"]
blacklist = ['.idea', '.git', 'build', 'assets', 'kotlin', 'lib', 'META-INF', 'original', 'apktool.yml']


def change_androidx_2_androidy(OO00O000OOOOOOOO0):
    OO00OO00OO00OOOO0 = glob.glob(f"{OO00O000OOOOOOOO0}/smali/androidx/**/*.smali", recursive=True)
    for O0OO0O0OOOO00O0O0 in OO00OO00OO00OOOO0:
        OOOOOO000O0O0O000 = O0OO0O0OOOO00O0O0.replace("androidx", "androidy")
        O00O000OOO00000O0 = os.path.dirname(OOOOOO000O0O0O000)
        if not os.path.exists(O00O000OOO00000O0):
            os.makedirs(O00O000OOO00000O0, exist_ok=True)
        shutil.move(O0OO0O0OOOO00O0O0, OOOOOO000O0O0O000)


def traverse_folder(O000OO0O000000OO0, OO00OO00OO0000000):
    O000O00OOOOO000OO = os.listdir(O000OO0O000000OO0)
    for OOOO0O0OO00O00OOO in O000O00OOOOO000OO:
        O00OOOO000OO00O00 = str(os.path.join(O000OO0O000000OO0, OOOO0O0OO00O00OOO))
        print(O00OOOO000OO00O00)
        if OOOO0O0OO00O00OOO not in blacklist:
            if os.path.isdir(O00OOOO000OO00O00):
                traverse_folder(O00OOOO000OO00O00, OO00OO00OO0000000)
            elif os.path.isfile(O00OOOO000OO00O00):
                if O00OOOO000OO00O00.split(".")[-1] in extends:
                    save_2_file(O00OOOO000OO00O00, OO00OO00OO0000000)


def save_2_file(OO00O0OOO0OOOO0O0, O0O0OOO00O00OOO0O):
    with codecs.open(OO00O0OOO0OOOO0O0, "r", "utf-8") as O0O0OOO00O0OO0O0O:
        OOOO000OOOO0O0OOO = O0O0OOO00O0OO0O0O.read()
    with codecs.open(OO00O0OOO0OOOO0O0, "w", "utf-8") as O0O000OO0OO0O00OO:
        OO0OOO0000O0OO0O0 = 0
        for OO000O0O000OO00O0, OOO0OOO0O00O00000 in O0O0OOO00O00OOO0O.items():
            OO0OOO0000O0OO0O0 += OOOO000OOOO0O0OOO.count(OO000O0O000OO00O0)
            OOOO000OOOO0O0OOO = OOOO000OOOO0O0OOO.replace(OO000O0O000OO00O0, OOO0OOO0O00O00000)
        print(r'替换次数：', OO0OOO0000O0OO0O0)
        O0O000OO0OO0O00OO.write(OOOO000OOOO0O0OOO)


def convertAndroidY(OO0OO0OOOOOO0O0OO):
    OOOOO0OOOOO00O00O = time.time()
    change_androidx_2_androidy(OO0OO0OOOOOO0O0OO)
    traverse_folder(OO0OO0OOOOOO0O0OO, {"androidx": "androidy"})
    O000O0OO000OOOO0O = time.time()
    print(f"执行完毕，输出结果保存到：{OO0OO0OOOOOO0O0OO} 共耗时{O000O0OO000OOOO0O - OOOOO0OOOOO00O00O} 秒")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("from_dir")
    args = parser.parse_args()
    convertAndroidY(args.from_dir)


if __name__ == "__main__":
    main()
