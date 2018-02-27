# Add Custom Apps and Services
PRODUCT_PACKAGES += ActivateLATAM \
                    Apps \
                    AppsOverlay \
                    BrowserTcl \
                    BrowserOverlay \
                    CompassTcl \
                    CompassOverlay \
                    Diagnostics \
                    Elabel \
                    ElabelOverlay \
                    EnjoyNow \
                    FileManagerTcl \
                    FileManagerOverlay \
                    Fota \
                    Officesuit \
                    SuperCleaner \
                    SetupWizardTcl \
                    SimpleLauncher \
                    SingleLogin \
                    UserCare \
                    UserCareOverlay \
                    Weather \
                    WeatherOverlay \
                    JoyLauncherOverlay \
                    JoyLauncher \
                    ThemeCenter \
                    ThemeCenterOverlay \
                    Gallery_Global \
                    CameraTcl \
                    CameraOverlay \
                    EnjoyNowOverlay \
                    facebookStub \
                    facebook-appmanager \
                    facebook-installer \
                    facebook-services \
                    Instagram \
                    MessengerFacebook \
                    DisneyMagicKingdom_LATAM \
                    SpidermanUltimatePower_LATAM \
                    MotocrossTrialExtreme \
                    PuzzlePets \
                    ModernCombat4 \
                    Toolkit

# Overrides
PRODUCT_PROPERTY_OVERRIDES +=

# add facebook config file use in TCL project
PRODUCT_COPY_FILES += vendor/customer/appmanager.conf:system/etc/appmanager.conf
PRODUCT_COPY_FILES += vendor/customer/privapp-permissions-facebook.xml:system/etc/permissions/privapp-permissions-facebook.xml
PRODUCT_COPY_FILES += vendor/customer/OfficeSuiteAlcatel.txt:system/etc/OfficeSuiteAlcatel.txt
PRODUCT_COPY_FILES += vendor/customer/apps/Officesuit/OfficeSuite_Free_9.1.10758.apk:system/vendor/operator/app/Officesuit/Officesuit.apk
PRODUCT_COPY_FILES += vendor/customer/apps/WhatsApp/WhatsApp.apk:system/vendor/operator/app/WhatsApp/WhatsApp.apk

