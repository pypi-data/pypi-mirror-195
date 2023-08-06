import argparse
import os
import shutil
import time
import merge_project_diff.manifest_diff
import merge_project_diff.merge_xml_diff

black_list_dir = ['.idea', ".git", 'build', 'META-INF', 'original', 'apktool.yml']
target_project_path = ""
dir_map = {}
is_allow: bool = False
"""
    对比两个项目的diff之处，把新增文件和xml属性copy到目标项目中
    project_from_dir：代码多的目录
    project_to_dir：代码少的目录
"""


def execute_merge_diff_file(O0O0O0000000OO0O0, OOO000OO0OO0OO000):
    ""
    OO00OOOOO0O000OOO = os.listdir(O0O0O0000000OO0O0)
    O00O00000O000O000 = os.listdir(OOO000OO0OO0OO000)
    for OOO0OO0OOOOO0O0O0 in OO00OOOOO0O000OOO:
        OO0OOO00O0O0O0OO0 = O0O0O0000000OO0O0 + os.sep + OOO0OO0OOOOO0O0O0
        OOOOO000O0O00O000 = OOO000OO0OO0OO000 + os.sep + OOO0OO0OOOOO0O0O0
        if OOO0OO0OOOOO0O0O0 not in black_list_dir:
            if os.path.isdir(OO0OOO00O0O0O0OO0):
                if OOO0OO0OOOOO0O0O0 not in O00O00000O000O000:
                    os.makedirs(OOOOO000O0O00O000, exist_ok=True)
                execute_merge_diff_file(OO0OOO00O0O0O0OO0, OOOOO000O0O00O000)
            elif os.path.isfile(OO0OOO00O0O0O0OO0):
                if OOO0OO0OOOOO0O0O0 not in O00O00000O000O000:
                    if is_allow:
                        shutil.copy(OO0OOO00O0O0O0OO0, OOOOO000O0O00O000)
                    else:
                        O0O0OO00OO0OO0O0O = str(OOOOO000O0O00O000)
                        O00OOOOOOOO000O00 = f'{target_project_path}_diff{O0O0OO00OO0OO0O0O.replace(target_project_path, "")}'
                        OOOO000000OOOO00O = os.path.dirname(O00OOOOOOOO000O00)
                        if not os.path.exists(OOOO000000OOOO00O):
                            os.makedirs(OOOO000000OOOO00O, exist_ok=True)
                        shutil.copy(OO0OOO00O0O0O0OO0, O00OOOOOOOO000O00)
                if OO0OOO00O0O0O0OO0.__contains__("/res/values"):
                    if is_allow:
                        merge_project_diff.merge_xml_diff.merge_diff(OO0OOO00O0O0O0OO0, OOOOO000O0O00O000)
                    else:
                        merge_project_diff.merge_xml_diff.merge_diff_attrs(OO0OOO00O0O0O0OO0, OOOOO000O0O00O000, target_project_path)
                if OO0OOO00O0O0O0OO0.__contains__("AndroidManifest"):
                    if not is_allow:
                        merge_project_diff.manifest_diff.merge_manifest_diff(OOOOO000O0O00O000, OO0OOO00O0O0O0OO0)
                        OOO0000OO0O000OOO = O0O0O0000000OO0O0 + "/AndroidManifest_diff.xml"
                        if os.path.exists(OOO0000OO0O000OOO):
                            OOO00000O0OO00OO0 = OOO000OO0OO0OO000 + "_diff/AndroidManifest_diff.xml"
                            if os.path.exists(OOO00000O0OO00OO0):
                                os.remove(OOO00000O0OO00OO0)
                            shutil.move(OOO0000OO0O000OOO, OOO000OO0OO0OO000 + "_diff")


def main():
    OO0O0O0OOO000000O = argparse.ArgumentParser()
    OO0O0O0OOO000000O.add_argument("project_from_dir")
    OO0O0O0OOO000000O.add_argument("project_to_dir")
    OOO0O0O00OOO0000O = OO0O0O0OOO000000O.parse_args()
    OO000O0000OO00OOO = OOO0O0O00OOO0000O.project_from_dir
    OOOOOO0OO0OO00OOO = OOO0O0O00OOO0000O.project_to_dir
    global target_project_path
    target_project_path = OOOOOO0OO0OO00OOO
    OOOOO0OO0OO0O0OOO = input(f'是否将diff文件输出到:{OOOOOO0OO0OO00OOO}\nyes or no ？\n')
    O0OOO0OOOOOO00000 = OOOOO0OO0OO0O0OOO == "yes"
    OO00O0OOO0O0O0O0O = time.time()
    execute_merge_diff_file(OO000O0000OO00OOO, OOOOOO0OO0OO00OOO)
    OO00O00O0000OOO00 = time.time()
    print(
        f"输出diff完成，写入到{OOOOOO0OO0OO00OOO if O0OOO0OOOOOO00000 == True else OOOOOO0OO0OO00OOO + '_diff'} , 耗时{OO00O00O0000OOO00 - OO00O0OOO0O0O0O0O} 秒")


if __name__ == "__main__":
    main()
