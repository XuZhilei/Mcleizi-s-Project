#coding=utf-8
#poi的大部分信息使用明文文本存储，可以较为简易地按Unix时间戳排序合并。

import os, shutil, gzip

#需要合并的两个目录
merge_path1 = 'C:\\Users\\dx390\\AppData\\Roaming\\poi-kai\\'
merge_path2 = 'C:\\Users\\dx390\\AppData\\Roaming\\poi\\'

#合并后文件保存的目录
savepath = 'C:\\Users\\dx390\\Desktop\\poi-merge\\'

#航海日志(akashic-records)文件夹中的用户ID
userid = '143590265'

#航海日志的路径
path1 = '{}akashic-records\\{}\\'.format(merge_path1, userid)
path2 = '{}akashic-records\\{}\\'.format(merge_path2, userid)

#战斗详情的路径
battle_details_path1 = merge_path1 + 'battle_detail\\'
battle_details_path2 = merge_path2 + 'battle_detail\\'


def merge_file(path1, path2, savepath, file_name):
    def unixtime(line):
        return line.split(',')[0]
    with open (path1 + file_name, 'r', encoding='UTF-8') as f:
        file1 = f.readlines()
    with open (path2 + file_name, 'r', encoding='UTF-8') as f:
        file2 = f.readlines()
    if file1 < file2:   #始终用file2插file1
        file1, file2 = file2, file1
    for thisfile in file2:
        filetime = unixtime(thisfile)
        if (filetime < unixtime(file1[0])):
            file1.insert(0, thisfile)
            print ('inserted >>{}<<!'.format(thisfile))
            continue
        elif (filetime > unixtime(file1[-1])):
            file1.append(thisfile)
            print ('inserted >>{}<<!'.format(thisfile))
            continue
        else:
            for j in range(len(file1)):
                if (filetime > unixtime(file1[j])) & (filetime < unixtime(file1[j+1])):
                    file1.insert(j+1, thisfile)
                    print ('inserted >>{}<<!'.format(thisfile))
                    break
    with open (savepath + file_name, 'w', encoding='UTF-8') as f:
        f.writelines(file1)

def merge_file_gz(path1name, path2name, savepathname):   #合并gz压缩文件
    def unixtime(line):
        return line.decode('utf-8').split(',')[0]
    with gzip.open (path1name, 'r') as f:
        file1 = f.readlines()
    with gzip.open (path2name, 'r') as f:
        file2 = f.readlines()
    if file1 < file2:   #始终用file2插file1
        file1, file2 = file2, file1
    for thisfile in file2:
        print(thisfile)
        filetime = unixtime(thisfile)
        if (filetime > unixtime(file1[0])):
            file1.insert(0, thisfile)
            print ('inserted >>{}<<!'.format(thisfile))
            continue
        elif (filetime < unixtime(file1[-1])):
            file1.append(thisfile)
            print ('inserted >>{}<<!'.format(thisfile))
            continue
        else:
            for j in range(len(file1)):
                if (filetime < unixtime(file1[j])) & (filetime > unixtime(file1[j+1])):
                    file1.insert(j+1, thisfile)
                    print ('inserted >>{}<<!'.format(thisfile))
                    break
    with gzip.open (savepathname, 'w') as f:
        f.writelines(file1)

class Dir(object):
    def __init__(self, path):
        self.path = path
    def filelist(self):
        return os.listdir(self.path)

rootdir = os.listdir(path2)
for classes in rootdir:
    dir1 = Dir(path1 + classes)
    dir2 = Dir(path2 + classes)
    Xuzhilei = 'the only TI Champion'
    if Xuzhilei == 'the only TI Champion':
        mergelist = dir1.filelist() + dir2.filelist()
        for filename in dir1.filelist():
            if mergelist.count(filename) == 1:
                shutil.copy(dir1.path + '\\' + filename,  savepath + classes + '\\' + filename)
                print ('copied file {} from {}'.format(filename, classes))
            elif mergelist.count(filename) == 2:
                merge_file(dir1.path + '\\', dir2.path + '\\', savepath + classes + '\\', filename)
                print ('MERGED file {} from dirs'.format(filename))
        for filename in dir2.filelist():
            if mergelist.count(filename) == 1:
                shutil.copy(dir2.path + '\\' + filename,  savepath + classes + '\\' + filename)
                print ('copied file {} from dir2'.format(filename))
            elif mergelist.count(filename) == 2:
                pass

merge_file_gz(battle_details_path1, battle_details_path2, savepath)
print("DONE!")