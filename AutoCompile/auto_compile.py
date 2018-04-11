# 1. parse arguments
# 2. checkout new repo; TA_VERSION or trunk, multi thread
# 3. set environment setup, choosebranch
# 4. make -j8
# 5. make otapackage
# 6. make diff package
# 7. zip file

from util import read_args_from_config, execute_all_command, svn_checkout_parallel_with_map

# project=
# BUILD_VARIANT =  user(default)


if __name__ == '__main__':
    # FULL_PROJECT_NAME, BUILD_VARIANT = get_sys_args()
    is_checkout_new = read_args_from_config()
    if is_checkout_new:
        # can't use both, thread or map
        # svn_checkout_parallel_with_thread()
        svn_checkout_parallel_with_map()
    execute_all_command()
