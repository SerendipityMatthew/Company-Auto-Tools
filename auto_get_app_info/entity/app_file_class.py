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
