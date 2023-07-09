from os import path,system,makedirs,popen,listdir,rmdir,startfile
from time import sleep
from sys import exit
from psutil import disk_partitions
from re import compile

"""
from ctypes import windll
def is_admin():
    try:
        return windll.shell32.IsUserAnAdmin()
    except:
        return False
if is_admin():
    pass
else:
    print("需要管理员权限。")
    sleep(3)
    exit(1)
"""

def getDiskList():  
    diskList = []
    for diskIndex in range(65,91):
        disk = str(chr(diskIndex)) + ':'
        if path.isdir(disk):
            diskList.append(disk)
    return diskList

dirList = ["C:\\DISK\\","C:\\Temp\\DISK\\","D:\\DISK\\","D:\\Temp\\DISK\\",".\\DISK\\"]

print("不要把这个程序在需要隐藏的磁盘上运行！")
print("不要把这个程序在需要隐藏的磁盘上运行！")
print("不要把这个程序在需要隐藏的磁盘上运行！")

while True:
    diskMask = input("盘符？（输入字母就行）：")
    if len(str(diskMask)) != 1:
        print("输入有误")
    elif str(diskMask).isalpha():
        diskMask = str(diskMask).upper() + str(":")
        break
    else:
        print("输入有误")

print(("操作的盘符：%s")%(diskMask))

while True:
    print("挂载点？")
    for i in range(0,len(dirList)):
        print(("[%s]%s")%(str(i+1),str(dirList[i])))
    print("注意挂载点磁盘只能是NTFS，完整路径无中文")
    diskDir = input("：")
    if len(str(diskDir)) != 1:
        print("输入有误")
    elif str(diskDir).isdigit():
        if int(diskDir) in range(1,len(dirList)+1):
            diskDir = str(dirList[int(diskDir)-1])
            break
        else:
            print("输入有误")
    else:
        print("输入有误")

diskDir = str(path.abspath(str(diskDir)))

# 检查路径
zhPattern = compile(u'[\u4e00-\u9fa5]+')
match = zhPattern.search(diskDir)
 
if match:
    print("完整路径有中文，会导致mountvol无法挂载文件夹。")
    print("请重新运行并选择合适的路径。")
    sleep(3)
    exit(1)
else:
    pass

# 检查是不是NTFS
diskInfo = disk_partitions()
thisDiskMask = str(diskDir)[0:2]
for i in range(0,len(diskInfo)):
    if str(thisDiskMask) + str("\\") == str(diskInfo[i].device):
        if str(diskInfo[i].fstype) == str("NTFS"):
            pass
        else:
            print(("%s 不是 NTFS 文件系统，而是 %s")%(str(thisDiskMask),str(diskInfo[i].fstype)))
            print("请重新运行并选择NTFS磁盘所在路径。")
            sleep(3)
            exit(1)

if str(diskDir[-1]) == str("\\"):
    pass
else:
    diskDir += str("\\")
print(("操作的磁盘挂载文件夹：%s")%(diskDir))

while True:
    print("操作？")
    print("[1]隐藏盘符，并映射到本地文件夹")
    print("[2]恢复盘符，取消本地文件夹映射")
    umount = input("：")
    if int(umount) == 1:
        umount = False
        print("操作：[1]隐藏盘符，并映射到本地文件夹")
        break
    elif int(umount) == 2:
        umount = True
        print("操作：[2]恢复盘符，取消本地文件夹映射")
        break
    else:
        print("输入有误")

if umount == False:
    print("获取磁盘ID...")
    diskPath = str(str(popen("mountvol "+diskMask+" /L").readline()).replace("\n","").replace(" ",""))
    if str("系统找不到指定的文件。") in diskPath:
        print("磁盘指定错误或格式错误，格式：E:或E:/")
        sleep(3)
        exit(1)
    else:
        print(("磁盘ID是：%s")%(diskPath))
    print("卸载磁盘...")
    system("mountvol "+diskMask+" /D")
    print("卸载磁盘完成")
    try:
        makedirs(diskDir)
        print("文件夹已创建")
    except FileExistsError:
        print("文件夹存在，注意检查是否非空")
    if len(listdir(diskDir)) == 0:
        print("执行挂载操作中...")
        command = str("mountvol "+diskDir+" "+diskPath)
        print("命令行："+command)
        system(command)
        print("操作已经完成。")
        try:
            print("尝试打开："+diskDir+"\\APP\\U盘小偷\\")
            startfile(diskDir+"\\APP\\U盘小偷\\")
        except FileNotFoundError:
            print("打开失败！")
            print("尝试打开："+diskDir)
            startfile(diskDir)
        sleep(3)
    else:
        print("文件夹非空，请检查。")
        sleep(3)
        exit(1)
else:
    print("获取磁盘ID...")
    command = str("mountvol "+diskDir+" /L")
    diskPath = str(str(popen(command).readline()).replace("\n","").replace(" ",""))
    if str("系统找不到指定的文件。") in diskPath:
        print("挂载文件夹指定错误或格式错误，格式：E:或E:/")
        sleep(3)
        exit(1)
    else:
        print(("磁盘ID是：%s")%(diskPath))
    print("卸载挂载点...")
    system("mountvol "+diskDir+" /D")
    print("卸载挂载点完成")
    print("恢复盘符...")
    command = str("mountvol "+diskMask+" "+diskPath)
    print("命令行："+command)
    system(command)
    print("盘符已恢复")
    while True:
        print("删除挂载点文件夹吗？")
        print("[1]是")
        print("[2]否")
        umount = input("：")
        if int(umount) == 1:
            print("正在删除挂载点文件夹。")
            rmdir(diskDir)
            print("已删除挂载点文件夹。")
            break
        elif int(umount) == 2:
            print("保留挂载点文件夹。")
            break
        else:
            print("输入有误")

    print("操作已经完成。")
    sleep(3)

