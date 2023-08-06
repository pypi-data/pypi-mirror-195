import argparse
import os
import time
import gbwhatsapp
from gbwhatsapp.androidx_2_androidy.convert_androidy import convertAndroidY
from gbwhatsapp.gbwhatsapp_2_whatsapp.convert_gb import convertGB
from gbwhatsapp.insertcode.getYoSig import sign
from gbwhatsapp.insertcode.md_and_sec import sign as signMd5
from gbwhatsapp.others.others import other
from gbwhatsapp.public_sort.public_sort import sort
from gbwhatsapp.replace_package import replacePackage
from gbwhatsapp.support_2_supporty.convert_supporty import convertSupportY


def main():
    OOOO0O00OO0000OOO = argparse.ArgumentParser()
    OOOO0O00OO0000OOO.add_argument("from_dir")
    OO0O0OO0OO0O00O00 = OOOO0O00OO0000OOO.parse_args()
    O0O00O00OO0O0OOOO = OO0O0OO0OO0O00O00.from_dir
    OOO00000O00000OO0 = gbwhatsapp.__file__
    OO00OO00O0OOOOO0O = OOO00000O00000OO0[0:OOO00000O00000OO0.rindex("/gbwhatsapp")]
    OO00O0O0O0OOO0000 = time.time()
    print(f"*********** 移除{O0O00O00OO0O0OOOO} 所有行号开始 ************")
    os.chdir(O0O00O00OO0O0OOOO)
    os.system("find . -name '*.smali' | xargs sed -i '' -E '/\.line[[:space:]][0-9]+/d'")
    print(f"*********** 移除{O0O00O00OO0O0OOOO} 所有行号结束 ************")
    print("*********** com.whatsapp--》com.gbwhatsapp换包开始 ************")
    replacePackage(O0O00O00OO0O0OOOO)
    print("*********** com.whatsapp--》com.gbwhatsapp换包结束 ************")
    print("*********** gbwhatsapp classes back to whatsapp开始 ************")
    convertGB(O0O00O00OO0O0OOOO, OO00OO00O0OOOOO0O)
    print("*********** gbwhatsapp classes back to whatsapp结束 ************")
    print("*********** androidx_2_androidy开始 ************")
    convertAndroidY(O0O00O00OO0O0OOOO)
    print("*********** androidx_2_androidy结束 ************")
    print("*********** support_2_supporty开始 ************")
    convertSupportY(O0O00O00OO0O0OOOO)
    print("*********** support_2_supporty结束 ************")
    print("*********** 插入签名校验开始 ************")
    sign(O0O00O00OO0O0OOOO)
    signMd5(O0O00O00OO0O0OOOO)
    print("*********** 插入签名校验结束 ************")
    sort(O0O00O00OO0O0OOOO)
    print("*********** 其他操作->删除无用文件夹，替换特定字符串开始 ************")
    other(O0O00O00OO0O0OOOO, OO00OO00O0OOOOO0O)
    print("*********** 其他操作->删除无用文件夹，替换特定字符串结束 ************")
    OOO000OO0OOO0OO00 = time.time()
    print(f"程序执行结束，输出结果保存到：{O0O00O00OO0O0OOOO} 共耗时 {OOO000OO0OOO0OO00 - OO00O0O0O0OOO0000} 秒")


if __name__ == "__main__":
    main()
