# 1. parse arguments
# 2. checkout new repo; TA_VERSION or trunk, multi thread
# 3. set environment setup, choosebranch
# 4. make -j8
# 5. make otapackage
# 6. make diff package
# 7. zip file
import commands
from enum import Enum

from util import write_execute_result, send_result_mail, execute_command

full_project_name = "5058I_ALAE"
REPO_NAME = "ALPS-MP-N1.MP18-V1_AUS6739_66_N1_INHOUSE/"
sub_project_name = ""
svn_repo_root = "svn://192.168.29.29/repository/L05A/Trunk/ALPS-MP-N1.MP18-V1_AUS6739_66_N1_INHOUSE/"
svn_repo_module = "packages/apps/Settings"
SVN_REPO_NOT_EXIST = "the repo doesn't exist"
SVN_REPO_CHECKOUT_SUCCESSFUL = "svn repo checkout successfully"
PROJECT_NOT_EXIST = "The branch does not exist, please choose again!"
module_name = ""  # default  none, we will make -j8
platform_name = "aus6739_66_n1"
build_variant = "user"
ENG_TYPE = "eng"
DEBUG_TYPE = "user_debug"
USER_TYPE = "user"
BUILD_LOG_FILE = 'build.txt'

FULL_PROJECT_OUT_DIR = "out/target/product/" + platform_name

# project=
# BUILD_VARIANT =  user(default)
BUILD_TYPE = Enum(ENG_TYPE, DEBUG_TYPE, USER_TYPE)

svn_checkout_command = "svn checkout %s" % svn_repo_root + svn_repo_module
execute_command(svn_checkout_command)

if full_project_name.__contains__('_'):
    project_name_split = full_project_name.split('_')
    sub_project_name = project_name_split[0]

# ./choosebranch_auto.sh 5058I
choose_sub_branch_command = "cd %s && ./choosebranch.sh %s " % (REPO_NAME, sub_project_name)

execute_command(choose_sub_branch_command)
choose_full_branch_command = "cd %s && ./choosebranch.sh %s" % (REPO_NAME, full_project_name)

# ./choosebranch_auto.sh 5058I_ALAE
execute_command(choose_full_branch_command)

# buildmodem
build_modem_command = "cd %s && ./buildmodem_L05A.sh"
execute_command(build_modem_command)

# lunch full_aus6739_66_n1-user
lunch_full_project = "cd %s && lunch full_%s-%s" % (REPO_NAME, platform_name, build_variant)
execute_command(lunch_full_project)

# make -j8
build_full_project = "cd %s && make -j8 %s" % (REPO_NAME, module_name)
# send the build result in any situation
execute_command(build_full_project, always_send_email=True)

# make otapackage -j8
module_name = "otapackage"
ota_command = "cd %s && make -j8  %s" % (REPO_NAME, module_name)
# send the build result in any situation
execute_command(ota_command, always_send_email=True)
