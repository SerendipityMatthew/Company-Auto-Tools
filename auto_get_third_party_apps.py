import os
import re
import sys
import xlwt

from app_file_class import AppFile

# system/priv-app
# system/app
# system/vendor/app
# system/vendor/priv-app
# system/operator
# GMS
# customer apk

customAppFileDir = "/home/xuwanjin/xuwanjin_workserver/source/6739_2/ALPS-MP-N1.MP18-V1_AUS6739_66_N1_INHOUSE/vendor/customer/apps"
aaptFilePath = "prebuilts/sdk/tools/linux/bin/aapt"
systemFile = {}
outDir = sys.argv[0]
gmsFile = "vendor/google/products/gms.mk"
googleAppFilePath = "vendor/google/apps"
thirdPartyAppList = []
googleAPpFIleList = []

# 1. 先获取目录下的所有的APP List
# 2. 在去解析相关的文件, 获取这个项目所有的APP List
# 3. 取出所有的需要的APP List的路径
# 4. 获取APP相关的信息
# 5. 生成相关的excel表格



# googleAppFilePath = "/home/xuwanjin/xuwanjin_workserver/" \
#                     "source/6739_2/ALPS-MP-N1.MP18-V1_AUS6739_66_N1_INHOUSE/" \
#                     "vendor/google/apps"

# 获取系统的所有的Apps
with open("installed-files.txt", mode='r') as installedFile:
    for fileLine in installedFile.readlines():
        # eg:     102   /system/priv-app/SettingsProvider/SettingsProvider.apk
        fileLineStr = fileLine.strip("\n")
        fileLineArray = fileLineStr.split("  /")
        #  we need system/priv-app/SettingsProvider/SettingsProvider.apk
        filePath = fileLineArray[1].strip(" ")
        # print(filePath)
        appFile = str(filePath)
        # filer the apk file, don't filter the odex, because some app don't have odex file
        if appFile.endswith(".apk"):
            appFileArray = appFile.split("/")
            # print(appFileArray[-1])
            # systemFile = {k: v for k, v in zip()}

# 先获取所有的apps, 写入到一个文件 
with open("custom.mk", mode='r') as customAppFile:
    with open('custom_app_only.txt', 'w') as customOnlyFile:
        for fileLine in customAppFile.readlines():
            if fileLine.__contains__('PRODUCT_PROPERTY_OVERRIDES'):
                continue
            if fileLine.__contains__('#'):
                continue
            if fileLine.__contains__('PRODUCT_COPY_FILES'):
                if '.apk' not in fileLine:
                    continue
            # if fileLine.__contains__('PRODUCT_PACKAGES += '):
            #     fileLine = fileLine.strip("PRODUCT_PACKAGES += ")

            if len(fileLine.strip()) != 0:
                customOnlyFile.write(fileLine)
# 把所有的文件放到一个列表当中去
with open("custom_app_only.txt", 'r') as customAppOnlyFile:
    for fileLine in customAppOnlyFile.readlines():

        if fileLine.__contains__('PRODUCT_PACKAGES'):
            appDirName = fileLine.strip('PRODUCT_PACKAGES +').strip('= ')
            thirdPartyAppList.append(appDirName.strip("\\\n").strip(' '))
            print(appDirName)
            continue

        if fileLine.__contains__('PRODUCT_COPY_FILES'):
            fileLine = fileLine.strip("PRODUCT_COPY_FILES += ")
            appDirName = fileLine.split(':')[0].split('/')[-2]
            thirdPartyAppList.append(appDirName)
            print(appDirName)
            continue

        appDirName = fileLine.strip('\n').strip('\\').lstrip(' ').rstrip(' ')
        thirdPartyAppList.append(appDirName)
        print(appDirName)

# print(sorted(thirdPartyAppList))  # now we get all the system third party apps.

# 获取扫有的GMS包里面的apk
# 首先遇到了PRODUCT_PACKAGES， 那么把下一行删掉

with open("gms.mk", mode='r') as customAppFile:
    with open("gms_only_app.txt", 'w') as gmsOnlyApkFile:
        for fileLine in customAppFile.readlines():
            if fileLine.__contains__("#"):
                continue
            if fileLine.__contains__('PRODUCT_PROPERTY_OVERRIDES'):
                continue
            if fileLine.__contains__('PRODUCT_PACKAGES'):
                continue
            if fileLine.__contains__('PRODUCT_COPY_FILES'):
                continue
            if fileLine.__contains__('PRODUCT_PACKAGE_OVERLAYS'):
                continue
            if fileLine.__contains__('$'):
                continue
            if fileLine.__contains__('ro.'):
                continue
            if fileLine.__contains__('.jar'):
                continue
            if fileLine.__contains__('ANDROID_PARTNER_GMS_HOME'):
                continue
            if len(fileLine.strip()) != 0:
                gmsOnlyApkFile.write(fileLine)

    gmsOnlyApkFile.close()


def is_file_exists(filepath):
    if os.path.exists(googleAppFilePath):
        print(" file path exist")
        return True
    else:
        print("file path don't exist")
        return False


if is_file_exists(googleAppFilePath):
    googleAppFileList = os.listdir(googleAppFilePath)
    # print(sorted(googleAppFileList))
# some application platformBuildVersionName doesn't exist
# some  version name of application have the blank space. eg: facebookStub/facebook-stub.apk
getApkInfo = "package: name='(\S+)' versionCode='(\d+)' versionName='(.*)' platformBuildVersionName='.*'"

# some the application name have the blank space,
# some the application don't have the icon info,
getApkAppNameInfo = "application: label='(.*)' icon="

files_path = []


# get application file name: a path
def get_app_file_name_info(app_file_path):
    file_members = os.listdir(app_file_path)
    for file_member in file_members:
        file_member_path = os.path.join(app_file_path, file_member)
        if file_member_path.endswith(".apk"):
            files_path.append(file_member_path)

        if os.path.isdir(file_member_path):
            get_app_file_name_info(file_member_path)

    return files_path


# 获取某一个apps的 package name, version name
def get_app_base_info(app_file_path):
    output_base = os.popen(
        "aapt d badging %s" % app_file_path,
        'r', 1).read()
    match_app_base = re.compile(getApkInfo).match(output_base)
    print(app_file_path)
    if not match_app_base:
        raise Exception("can't not get package info")
    output_base_application = os.popen(
        "aapt d badging %s | grep \"application: label=\"" % app_file_path,
        'r', 1).read()
    if not output_base_application:
        output_base_application = os.popen(
            "aapt d badging %s | grep \"application-label:\'\"" % app_file_path,
            'r', 1).read()
    match_app_base_application = re.compile(getApkAppNameInfo).match(output_base_application)
    if not match_app_base_application:
        match_app_base_application = re.compile("application-label:'(.*)'").match(output_base_application)
    app_name = match_app_base_application.group(1)
    package_name = match_app_base.group(1)
    version_name = match_app_base.group(3)
    print(match_app_base_application.group(1))
    print(package_name)
    print(version_name)
    return app_name, version_name, package_name


def yield_app_instance():
    # a path
    app_files = get_app_file_name_info(customAppFileDir)
    print(app_files)
    # for app_file in app_files:
    app_file_list = []
    #### Test
    for app_file in app_files:
        app_info = get_app_base_info(app_file)
        app_file_instance = AppFile(app_info[0], app_info[1], app_info[2], "3333", str(app_file).split('/')[-1])
        app_file_list.append(app_file_instance)

    return app_file_list


def yield_excel_file(app_file_list, excel_file_name):
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet("app_list", cell_overwrite_ok=True)

    for serial_no in range(len(app_file_list)):
        app_attri_list = app_file_list[serial_no].get_all_attri()
        print(app_attri_list)
        for item_index in range(len(app_attri_list)):
            if item_index == 3:
                continue
            sheet.write(serial_no, item_index, app_attri_list[item_index])
    wbk.save(excel_file_name + ".xlsx")


yield_excel_file(yield_app_instance(), "app_list")
