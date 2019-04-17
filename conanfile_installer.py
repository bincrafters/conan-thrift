# -*- coding: utf-8 -*-
import os
from conans import CMake
from conanfile_base import ConanBase


class ThriftInstallerConan(ConanBase):
    name = "thrift_installer"
    version = ConanBase.version
    settings = "os_build", "arch_build", "compiler"

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_TESTING"] = False
        cmake.definitions["BUILD_COMPILER"] = True
        cmake.definitions["BUILD_LIBRARIES"] = False
        cmake.definitions["BUILD_EXAMPLES"] = False
        cmake.definitions["BUILD_TUTORIALS"] = False
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def package_info(self):
        bin_dir = os.path.join(self.package_folder, "bin")
        self.env_info.PATH.append(bin_dir)

    def package_id(self):
        del self.info.settings.compiler

