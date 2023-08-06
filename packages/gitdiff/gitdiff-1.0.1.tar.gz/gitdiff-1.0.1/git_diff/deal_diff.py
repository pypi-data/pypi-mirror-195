import argparse
import codecs
import json
import os
import shutil

add_file_list = []
modify_file_list = []
del_file_list = []
other_file_list = []


def exec_diff(O00O0OOOO0OO00OO0):
    with codecs.open(O00O0OOOO0OO00OO0, mode="r", encoding="utf-8") as OOO0O000OO0OO0OO0:
        O00O0O00OO00OO0OO = OOO0O000OO0OO0OO0.readlines()
        for O0OOO000O0O0O00O0 in O00O0O00OO00OO0OO:
            O00O000OOO00O0OO0 = O0OOO000O0O0O00O0.strip().split("	")
            O0000O0000O0O0000 = O00O000OOO00O0OO0[0]
            O0OO0OO00OO0OOO00 = O00O000OOO00O0OO0[1]
            if O0000O0000O0O0000 == "M":
                if not O0OO0OO00OO0OOO00 in modify_file_list:
                    modify_file_list.append(O0OO0OO00OO0OOO00)
            elif O0000O0000O0O0000 == "D":
                if not O0OO0OO00OO0OOO00 in del_file_list:
                    del_file_list.append(O0OO0OO00OO0OOO00)
            elif O0000O0000O0O0000 == "A":
                if not O0OO0OO00OO0OOO00 in add_file_list:
                    add_file_list.append(O0OO0OO00OO0OOO00)
            else:
                if not O0OO0OO00OO0OOO00 in other_file_list:
                    other_file_list.append(O0OO0OO00OO0OOO00)


def save_data_to_file(O0O0O0000OOOOOOO0, OOO0O0O00OO0OO00O):
    OOOOOOOO000000O0O = json.dumps(O0O0O0000OOOOOOO0, ensure_ascii=False, indent=2)
    with codecs.open(OOO0O0O00OO0OO00O, "w+", encoding="utf-8") as OOO0000OOOOOOO0OO:
        OOO0000OOOOOOO0OO.write(OOOOOOOO000000O0O)


def copy_file_to_new_folder(O0O0O000000O00O00, O00O00OO0O0OOO000, OOO0O000O0O0OO0O0, O0OO0O0O00OO000O0: str):
    O00000OO00OOO0OO0 = f"{O00O00OO0O0OOO000}/{OOO0O000O0O0OO0O0}"
    print(f"fold_path = {O00000OO00OOO0OO0}")
    if not os.path.exists(O00000OO00OOO0OO0):
        os.makedirs(O00000OO00OOO0OO0, exist_ok=True)
    os.chdir(O00O00OO0O0OOO000)
    print(f"current_path = {os.getcwd()}")
    for O00OO000O0OOO0000 in O0O0O000000O00O00:
        O0O00OO0OO0000OO0 = O00OO000O0OOO0000.find("/")
        O000000O0O0OO00O0 = O00OO000O0OOO0000.rfind("/")
        O00OOOO00O0000O0O = os.path.basename(O00OO000O0OOO0000)
        O00O0OO0O0O0O00OO = O0OO0O0O00OO000O0.index(O00OO000O0OOO0000[0:O0O00OO0OO0000OO0])
        O000O000OOO0O000O = O0OO0O0O00OO000O0[0:O00O0OO0O0O0O00OO] + O00OO000O0OOO0000
        O0OOO000OO000O000 = O00000OO00OOO0OO0 + O00OO000O0OOO0000[O0O00OO0OO0000OO0:O000000O0O0OO00O0 + 1]
        OOOO00OO00OO0000O = O0OOO000OO000O000 + O00OOOO00O0000O0O
        print(f"oldFilePath = {O00OO000O0OOO0000} new_file_path = {OOOO00OO00OO0000O}")
        if not os.path.exists(O0OOO000OO000O000):
            os.makedirs(O0OOO000OO000O000, exist_ok=True)
        shutil.copy(O000O000OOO0O000O, OOOO00OO00OO0000O)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("diff_path")
    args = parser.parse_args()
    exec_diff(args.diff_path)
    mCurrentPath = os.getcwd()
    target_folder = mCurrentPath + "/scripts/git_diff"
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    os.chdir(target_folder)
    save_data_to_file(add_file_list, "add.json")
    print(f"新增文件，输出到：{target_folder}/add.json")
    save_data_to_file(modify_file_list, "modify.json")
    print(f"文件变化，输出到：{target_folder}/modify.json")
    save_data_to_file(del_file_list, "del.json")
    print(f"文件删除，输出到：{target_folder}/del.json")
    save_data_to_file(other_file_list, "other.json")
    print(f"文件其他操作，输出到：{target_folder}/other.json")


if __name__ == "__main__":
    main()