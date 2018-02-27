import os
import sys

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
# googleAppFilePath = "/home/xuwanjin/xuwanjin_workserver/" \
#                     "source/6739_2/ALPS-MP-N1.MP18-V1_AUS6739_66_N1_INHOUSE/" \
#                     "vendor/google/apps"
count = 0
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

# 取出所有的第三方Apps,
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

print(sorted(thirdPartyAppList))  # now we get all the system third party apps.

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


def isFileExists(filepath):
    if os.path.exists(googleAppFilePath):
        print(" file path exist")
        return True
    else:
        print("file path don't exist")
        return False


if isFileExists(googleAppFilePath):
    googleAppFileList = os.listdir(googleAppFilePath)
    # print(sorted(googleAppFileList))

import re
import zipfile

getApkInfo = "package: name='(\S+)' versionCode='(\d+)' versionName='(\S+)' platformBuildVersionName='\S+'"


def getAppBaseInfo(appFilePath):
    output = os.popen(
        "./../../../android/aosp/android-8.0.0_r16/prebuilts/sdk/tools/linux/bin/aapt d badging %s" % appFilePath).read()
    match = re.compile(getApkInfo).match(output)
    if not match:
        raise Exception("con't not get package info")
    package_name = match.group(1)
    version_code = match.group(1)
    version_name = match.group(1)
    print(package_name)
    print(version_code)
    print(version_name)


getAppBaseInfo("/home/xuwanjin/Downloads/software/shadowsocks-nightly-4.2.5.apk")
