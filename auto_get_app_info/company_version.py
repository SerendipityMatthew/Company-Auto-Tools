#! /usr/bin/env python
# -*- coding: cp1252 -*-
import os
import re
import sys

# import ./xlwt-1.3.0/xlwt/Workbook as WorkbookCom
# from xlwt.Workbook import Workbook

# system/priv-app
# system/app
# system/vendor/app
# system/vendor/priv-app
# system/operator
# GMS
# customer apk
# commonAppFilePath = "./"
commonAppFilePath = "/home/xuwanjin/xuwanjin_workserver/source/6739_2/ALPS-MP-N1.MP18-V1_AUS6739_66_N1_INHOUSE/"
customAppFileDir = commonAppFilePath + "vendor/customer"
googleAppFilePath = commonAppFilePath + "vendor/google"
aaptFilePath = commonAppFilePath + "prebuilts/sdk/tools/linux/bin/aapt"
systemFile = {}
gmsFile = "vendor/google/products/gms.mk"
outDir = sys.argv[0]
thirdPartyAppList = []
googleAPpFIleList = []


class AppFile(object):
    """ let's abstract the application (android Application) file """

    # app_name == application-label
    def __init__(self, app_name, version_name, package_name, module_name, file_name):
        self.app_name = app_name
        self.module_name = module_name
        self.package_name = package_name
        self.file_name = file_name
        self.version_name = version_name

    def get_module_name(self):
        return self.module_name

    def get_package_name(self):
        return self.package_name

    def get_file_name(self):
        return self.file_name

    def get_version_name(self):
        return self.version_name

    def get_app_name(self):
        return self.app_name

    def __str__(self):
        return "app_name:%s version_name:%s package_name:%s module_name:%s file_name%s " \
               "" % (self.app_name, self.version_name, self.package_name, self.module_name, self.file_name)

    def get_all_attri(self):
        return [self.app_name, self.version_name, self.package_name, self.module_name, self.file_name]


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


# get application file name: a path
def get_app_file_name_info(app_file_path, files_path):
    file_members = os.listdir(app_file_path)
    for file_member in file_members:
        file_member_path = os.path.join(app_file_path, file_member)
        if file_member_path.endswith(".apk"):
            files_path.append(file_member_path)

        if os.path.isdir(file_member_path):
            get_app_file_name_info(file_member_path, files_path)
    return files_path


def get_app_base_info(app_file_path):
    output_base = os.popen(
        aaptFilePath + " d badging %s" % app_file_path,
        'r', 1).read()
    match_app_base = re.compile(getApkInfo).match(output_base)
    print(app_file_path)
    if not match_app_base:
        raise Exception("can't not get package info")
    output_base_application = os.popen(
        aaptFilePath + " d badging %s | grep \"application: label=\"" % app_file_path,
        'r', 1).read()
    if not output_base_application:
        output_base_application = os.popen(
            aaptFilePath + " d badging %s | grep \"application-label:\'\"" % app_file_path,
            'r', 1).read()
    match_app_base_application = re.compile(getApkAppNameInfo).match(output_base_application)
    if not match_app_base_application:
        match_app_base_application = re.compile("application-label:'(.*)'").match(output_base_application)
    app_name = match_app_base_application.group(1)
    package_name = match_app_base.group(1)
    version_name = match_app_base.group(3)
    print(app_name)
    print(package_name)
    print(version_name)
    return app_name, version_name, package_name


def yield_app_instance(custom_App_File_Dir):
    # a path
    app_files = get_app_file_name_info(custom_App_File_Dir, [])
    print(app_files)
    # for app_file in app_files:
    app_file_list = []
    #### Test
    for app_file in app_files:
        app_info = get_app_base_info(app_file)
        # 333 module name,
        app_file_instance = AppFile(app_info[0], app_info[1], app_info[2], "3333", str(app_file).split('/')[-1])
        app_file_list.append(app_file_instance)

    return app_file_list


# def yield_excel_file(app_file_list, excel_file_name):
#     wbk = Workbook()
#     sheet = wbk.add_sheet(excel_file_name, cell_overwrite_ok=True)
#     for serial_no in range(len(app_file_list)):
#         app_attri_list = app_file_list[serial_no].get_all_attri()
#         print(app_attri_list)
#         for item_index in range(len(app_attri_list)):
#             if item_index == 3:
#                 continue
#             sheet.write(serial_no, item_index, app_attri_list[item_index])
#     wbk.save(excel_file_name + ".xlsx")


def yield_txt_file(app_file_list, txt_file_name):
    f = open(txt_file_name, "w")
    for serial_no in range(len(app_file_list)):
        app_attri_list = app_file_list[serial_no].get_all_attri()
        print(app_attri_list)
        # app name | version name| package name | file name
        for item_index in range(len(app_attri_list)):
            if item_index == 4:
                f.write(app_attri_list[item_index] + "\n")
            else:
                f.write(app_attri_list[item_index] + " | ", )
            print(app_attri_list[item_index])
    f.close()


# yield_excel_file(yield_app_instance(customAppFileDir), "AutoCompanyTools")
# yield_excel_file(yield_app_instance(googleAppFilePath), "google_app_list.txt")
# yield_txt_file(yield_app_instance("/home/xuwanjin/Downloads/software"), "AutoCompanyTools.txt")
yield_txt_file(yield_app_instance(customAppFileDir), "AutoCompanyTools.txt")
yield_txt_file(yield_app_instance(googleAppFilePath), "google_app_list.txt")
