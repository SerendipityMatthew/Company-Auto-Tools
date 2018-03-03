import os
import sys
import re

# system/priv-app
# system/app
# system/vendor/app
# system/vendor/priv-app
# system/operator
# GMS
# customer apk

aaptFilePath = "prebuilts/sdk/tools/linux/bin/aapt"

systemFile = {}
outDir = sys.argv[0]
gmsFile = "vendor/google/products/gms.mk"
googleAppFilePath = "vendor/google/apps"
thirdPartyAppList = []
googleAPpFIleList = []

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

getApkInfo = "package: name='(\S+)' versionCode='(\d+)' versionName='(\S+)' platformBuildVersionName='\S+'"
getApkAppNameInfo = "application: label='(\S+)' icon='(\S+)'"

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
    # application: label='Shadowsocks'
    # app_package_info_str = str(output_base)
    # print(app_package_info_str)
    # for app_info_line in app_package_info_str.split('\n'):
    #     if app_info_line.__contains__("application: label="):
    #         app_info_line.split(" ")
    #         print(app_info_line.split(" ")[1].strip('label=').lstrip("'").rstrip("'"))
    #     # print(fileLine)

    if not match_app_base:
        raise Exception("can't not get package info")
    output_base_application = os.popen(
        "aapt d badging %s | grep \"application: label=\"" % app_file_path,
        'r', 1).read()
    print(str(output_base_application).strip("\n"))
    match_app_base_application = re.compile(getApkAppNameInfo).match(output_base_application)
    print(match_app_base_application.group(1))
    app_name = match_app_base_application.group(1)
    package_name = match_app_base.group(1)
    version_code = match_app_base.group(2)
    version_name = match_app_base.group(3)
    print(package_name)
    print(version_code)
    print(version_name)
    return package_name, version_code, version_name, app_name


# a path
app_files = get_app_file_name_info("/home/xuwanjin/Downloads/software/")
print(app_files)
# for app_file in app_files:

#### Test
for app_file in app_files:
    get_app_base_info(app_file)
