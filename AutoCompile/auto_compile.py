# 1. parse arguments
# 2. checkout new repo; TA_VERSION or trunk, multi thread
# 3. set environment setup, choosebranch
# 4. make -j8
# 5. make otapackage
# 6. make diff package
# 7. zip file
import commands
import sys

import multiprocessing
from enum import Enum

from SvnCheckoutThread import SvnCheckoutThread
from util import execute_command

REPO_NAME = "ALPS-MP-N1.MP18-V1_AUS6739_66_N1_INHOUSE/"
SVN_REPO_PATH = "svn://192.168.29.29/repository/L05A/Trunk/ALPS-MP-N1.MP18-V1_AUS6739_66_N1_INHOUSE/"
svn_repo_module = "packages/apps/Settings"
SVN_REPO_NOT_EXIST = "the repo doesn't exist"
SVN_REPO_CHECKOUT_SUCCESSFUL = "svn repo checkout successfully"
PROJECT_NOT_EXIST = "The branch does not exist, please choose again!"
module_name = ""  # default  none, we will make -j8
platform_name = "aus6739_66_n1"
BUILD_VARIANT = "user"
ENG_TYPE = "eng"
DEBUG_TYPE = "user_debug"
USER_TYPE = "user"
BUILD_LOG_FILE = 'build.txt'
FULL_PROJECT_NAME = "5058A"
CHECKOUT_NEW_REPO = True

FULL_PROJECT_OUT_DIR = "out/target/product/" + platform_name

# project=
# BUILD_VARIANT =  user(default)
BUILD_TYPE = Enum(ENG_TYPE, DEBUG_TYPE, USER_TYPE)


# -p 5058I_ALAE1 -t user
def get_sys_args():
    full_project_name = ""
    build_variant = USER_TYPE
    print sys.argv
    for opt in sys.argv:
        if opt == "-h":
            print "choose a project, like" \
                  "project=5058I_ALAE1  type=user"
        elif str(opt).lower().__contains__('project='):
            full_project_name = str(opt).lower().lstrip('project=')
            if full_project_name.lstrip().strip().__sizeof__() == 0:
                raise RuntimeError("you should choose a project")
        elif str(opt).lower().__contains__('type='):
            var = str(opt).lower().lstrip('type=')
            if var in BUILD_TYPE:
                build_variant = var
    return full_project_name, build_variant


def read_args_from_config():
    with open("config.txt", 'r') as config_file:
        for line in config_file.readlines():
            variant = line.split("=")[-1].strip("\n").strip(" ")
            print "read_args_from_config: global variant for repo: variant = %s " % variant
            if line.__contains__("project_svn_path="):
                global SVN_REPO_PATH
                SVN_REPO_PATH = variant
            if line.__contains__("build_type"):
                global BUILD_VARIANT
                BUILD_VARIANT = variant
            if line.__contains__("project_name"):
                global FULL_PROJECT_NAME
                FULL_PROJECT_NAME = variant
            if line.__contains__("repo_name"):
                global REPO_NAME
                REPO_NAME = variant
            if line.__contains__("checkout_new_repo"):
                global CHECKOUT_NEW_REPO
                CHECKOUT_NEW_REPO = variant



def execute_all_command():
    # svn_checkout_command = "svn checkout %s" % svn_repo_root
    # execute_command(svn_checkout_command)
    sub_project_name = ""
    if FULL_PROJECT_NAME.__contains__('_'):
        project_name_split = FULL_PROJECT_NAME.split('_')
        sub_project_name = project_name_split[0]

    # ./choosebranch_auto.sh 5058I
    choose_sub_branch_command = "cd %s && ./choosebranch_auto.sh %s " % (REPO_NAME, sub_project_name)

    execute_command(choose_sub_branch_command)
    choose_full_branch_command = "cd %s && ./choosebranch_auto.sh %s" % (REPO_NAME, FULL_PROJECT_NAME)

    # ./choosebranch_auto.sh 5058I_ALAE
    execute_command(choose_full_branch_command)

    # buildmodem
    build_modem_command = "cd %s && ./buildmodem_L05A.sh"
    execute_command(build_modem_command)

    # source build/envsetup.sh
    source_project = "cd %s && source build/envsetup.sh"
    execute_command(source_project)

    # lunch full_aus6739_66_n1-user
    lunch_full_project = "cd %s && lunch full_%s-%s" % (REPO_NAME, platform_name, BUILD_VARIANT)
    execute_command(lunch_full_project)

    # make -j8
    build_full_project = "cd %s && make -j8" % REPO_NAME
    # send the build result in any situation
    execute_command(build_full_project, always_send_email=True)

    # make otapackage -j8
    module_name = "otapackage"
    ota_command = "cd %s && make -j8  %s" % (REPO_NAME, module_name)
    # send the build result in any situation
    execute_command(ota_command, always_send_email=True)


def svn_checkout_parallel_with_thread():
    status, result = commands.getstatusoutput("svn list %s" % SVN_REPO_PATH)
    file_list = result.split("\n")

    for f in file_list:
        checkout_thread = SvnCheckoutThread(
            "mkdir %s && cd %s && svn checkout %s/%s" % (REPO_NAME, REPO_NAME, SVN_REPO_PATH, f))
        checkout_thread.setName(f)
        checkout_thread.start()


def svn_checkout_parallel_with_map():
    status, result = commands.getstatusoutput("svn list %s" % SVN_REPO_PATH)
    file_list = result.split("\n")
    command_list = list()
    command_list_file = list()
    command_list_file.append("svn checkout --depth=empty %s " % SVN_REPO_PATH + REPO_NAME)

    for f in file_list:
        if is_file(f):
            command_list_file.append('cd %s && svn update %s' % (REPO_NAME, f))
        else:
            command_list.append('cd %s && svn checkout %s%s' % (REPO_NAME, SVN_REPO_PATH, f))

    # svn update , will produce the svn lock file, so we need queue the update task
    for f in command_list_file:
        execute_command(f)

    pool = multiprocessing.Pool(processes=8)
    pool.map(execute_command, command_list)
    pool.close()
    pool.join()


def is_file(f):
    status, result = commands.getstatusoutput("svn list  --depth=files %s" % SVN_REPO_PATH)
    if status == 0:
        return result.__contains__(f)
    raise RuntimeError("svn list command execute exception")


if __name__ == '__main__':
    # FULL_PROJECT_NAME, BUILD_VARIANT = get_sys_args()
    read_args_from_config()
    # svn_checkout_parallel_with_thread()
    svn_checkout_parallel_with_map()
    execute_all_command()
