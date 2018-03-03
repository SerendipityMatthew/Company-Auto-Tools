class AppFile(object):
    """ let's abstract the application (android Application) file """

    # app_name == application-label
    # 暂时想不出法子取出应用的名称, application: label=
    def __init__(self, module_name, package_name, file_name, version_name):
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
