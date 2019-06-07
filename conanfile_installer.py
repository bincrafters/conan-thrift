# -*- coding: utf-8 -*-
import os
from conans import CMake
from conanfile_base import ConanFileBase


class ConanFileInstaller(ConanFileBase):
    name = ConanFileBase._base_name + "_installer"
    version = ConanFileBase.version

    settings = "os_build", "arch_build", "compiler"

    def requirements(self):
        if self.settings.os_build == "Windows":
            self.requires("winflexbison/2.5.18@bincrafters/stable")
        else:
            self.requires("flex_installer/2.6.4@bincrafters/stable")
            self.requires("bison_installer/3.3.2@bincrafters/stable")

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTING"] = False
        cmake.definitions["BUILD_COMPILER"] = True
        cmake.definitions["BUILD_LIBRARIES"] = False
        cmake.definitions["BUILD_EXAMPLES"] = False
        cmake.definitions["BUILD_TUTORIALS"] = False
        cmake.definitions["WITH_SHARED_LIB"] = False
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def package_info(self):
        bindir = os.path.join(self.package_folder, "bin")
        self.output.info('Appending PATH environment variable: {}'.format(bindir))
        self.env_info.PATH.append(bindir)

    def package_id(self):
        del self.info.settings.compiler
