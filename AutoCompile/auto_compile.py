# 1. parse arguments
# 2. checkout new repo; TA_VERSION or trunk, multi thread
# 3. set environment setup, choosebranch
# 4. make -j8
# 5. make otapackage
# 6. make diff package
# 7. zip file
import commands
from enum import Enum

from util import write_execute_result, send_result_mail

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

checkout_status, checkout_result = commands.getstatusoutput("svn checkout %s" % svn_repo_root + svn_repo_module)
print "command exec status = %s, result %s " % (checkout_status, checkout_result)

if checkout_status != 0:
    yield_file_name = write_execute_result(checkout_result)
    send_result_mail(yield_file_name)
    raise RuntimeError(SVN_REPO_NOT_EXIST)
else:
    print SVN_REPO_CHECKOUT_SUCCESSFUL

if full_project_name.__contains__('_'):
    project_name_split = full_project_name.split('_')
    sub_project_name = project_name_split[0]

# ./choosebranch 5058I
# ./choosebranch 5058I_ALAE

sub_project_status, sub_project_result = commands.getstatusoutput(
    "cd %s && ./choosebranch.sh %s" % (REPO_NAME, sub_project_name))
print "command exec status = %s, result %s " % (sub_project_status, sub_project_result)
if sub_project_status != 0:
    yield_file_name = write_execute_result(sub_project_result)
    send_result_mail(yield_file_name)
    raise RuntimeError()

## ./choosebranch_auto
full_project_status, full_project_result = commands.getstatusoutput(
    "cd %s && ./choosebranch.sh %s" % (REPO_NAME, full_project_name))
print "command exec status = %s, result %s " % (full_project_status, full_project_result)
if full_project_status != 0:
    yield_file_name = write_execute_result(full_project_result)
    send_result_mail(yield_file_name)
    raise RuntimeError()

# buildmodem
modem_build_status, modem_build_result = commands.getstatusoutput("cd %s && ./buildmodem_L05A.sh")

print "command exec status = %s, result %s " % (modem_build_status, modem_build_result)
if modem_build_status != 0:
    yield_file_name = write_execute_result(modem_build_result)
    send_result_mail(yield_file_name)
    raise RuntimeError

# lunch full_
lunch_status, lunch_result = commands.getstatusoutput(
    "cd %s && lunch full_%s-%s" % (REPO_NAME, platform_name, build_variant))
print "command exec status = %s, result %s " % (lunch_status, lunch_result)
if lunch_status != 0:
    yield_file_name = write_execute_result(lunch_result)
    send_result_mail(yield_file_name)
    raise RuntimeError

# make -j8
build_status, build_result = commands.getstatusoutput("cd %s && make -j8 %s" % (REPO_NAME, module_name))
print "command exec status = %s, result %s " % (build_status, build_result)
if build_status != 0:
    yield_file_name = write_execute_result(build_result)
    send_result_mail(yield_file_name)
    raise RuntimeError

module_name = "otapackage"
otapackage_status, otapackage_result = commands.getstatusoutput("cd %s && make -j8  %s" % (REPO_NAME, module_name))
print "command exec status = %s, result %s " % (otapackage_status, otapackage_result)
if otapackage_status != 0:
    yield_file_name = write_execute_result(otapackage_result)
    send_result_mail(yield_file_name)
    raise RuntimeError()
