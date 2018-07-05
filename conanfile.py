#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment
import os


class ThriftConan(ConanFile):
    name = "thrift"
    version = "0.11.0"
    description =   "Thrift is a lightweight, \
                    language-independent software \
                    stack with an associated code \
                    generation mechanism for RPC."
    url = "https://github.com/helmesjo/conan-thrift"
    homepage = "https://thrift.apache.org/"
    author = "helmesjo <helmesjo@gmail.com>"

    # Indicates License type of the packaged library
    license = "MIT"

    # Packages the license for the conanfile.py
    exports = ["LICENSE.md"]

    # Remove following lines if the target lib does not use cmake.
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    # Options may need to change depending on the packaged library.
    settings = "os", "arch", "compiler", "build_type"

    # Custom attributes for Bincrafters recipe conventions
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"

    # Use version ranges for dependencies unless there's a reason not to
    # Update 2/9/18 - Per conan team, ranges are slow to resolve.
    # So, with libs like zlib, updates are very rare, so we now use static version

    # http://thrift.apache.org/docs/install/
    requires = (
        "boost/1.66.0@conan/stable",
    )

    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_zlib": [True, False],
        "with_libevent": [True, False],
        "with_qt4": [True, False],
        "with_qt5": [True, False],
        "with_openssl": [True, False],
        "with_boost_functional": [True, False],
        "with_boost_smart_ptr": [True, False],
        "with_boost_static": [True, False],
        "with_boostthreads": [True, False],
        "with_stdthreads": [True, False],
        "with_c_glib": [True, False],
        "with_cpp": [True, False],
        "with_java": [True, False],
        "with_python": [True, False],
        "with_haskell": [True, False],
        "with_plugin": [True, False],
        "build_libraries": [True, False],
        "build_compiler": [True, False],
        "build_testing": [True, False],
        "build_examples": [True, False],
        "build_tutorials": [True, False],

    }

    default_options = (
        "shared=False",
        "fPIC=True",
        "with_zlib=True",
        "with_libevent=True",
        "with_qt4=False",
        "with_qt5=False",
        "with_openssl=True",
        "with_boost_functional=False",
        "with_boost_smart_ptr=False",
        "with_boost_static=False",
        "with_boostthreads=False",
        "with_stdthreads=True",
        "with_c_glib=False",
        "with_cpp=True",
        "with_java=False",
        "with_python=False",
        "with_haskell=False",
        "with_plugin=False",
        "build_libraries=True",
        "build_compiler=True",
        "build_testing=False", # Currently fails if 'True' because of too recent boost::test version (?) in package
        "build_examples=False",
        "build_tutorials=False",
    )

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def requirements(self):
        if self.settings.os == 'Windows':
            self.requires("winflexbison/2.5.14@helmesjo/stable")
        else:
            self.requires("flex/2.6.4@bincrafters/stable")
            self.requires("bison/3.0.4@bincrafters/stable")
            
        if self.options.with_openssl:
            self.requires("OpenSSL/1.1.0g@conan/stable")
        if self.options.with_zlib:
            self.requires("zlib/1.2.11@conan/stable")
        if self.options.with_libevent:
            self.requires("libevent/2.0.22@bincrafters/stable")

    def source(self):
        source_url = "https://github.com/apache/thrift"
        tools.get("{0}/archive/{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version

        #Rename to "source_subfolder" is a convention to simplify later steps
        os.rename(extracted_dir, self.source_subfolder)

    def configure_cmake(self):
        def add_cmake_option(option, value):
            var_name = "{}".format(option).upper()
            value_str = "{}".format(value)
            var_value = "ON" if value_str == 'True' else "OFF" if value_str == 'False' else value_str 
            cmake.definitions[var_name] = var_value

        cmake = CMake(self, set_cmake_flags=True)

        if self.settings.os != 'Windows':
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC
        if self.settings.compiler == "Visual Studio":
            add_cmake_option("WITH_MT", self.settings.compiler.runtime == "MT")

        for attr, _ in self.options.iteritems():
            value = getattr(self.options, attr)
            add_cmake_option(attr, value)

        add_cmake_option("WITH_SHARED_LIB", self.options.shared)
        add_cmake_option("WITH_STATIC_LIB", not self.options.shared)
        cmake.definitions["BOOST_ROOT"] = self.deps_cpp_info['boost'].rootpath

        # Make optional libs "findable"
        if self.options.with_openssl:
            cmake.definitions["OPENSSL_ROOT_DIR"] = self.deps_cpp_info['OpenSSL'].rootpath
        if self.options.with_zlib:
            cmake.definitions["ZLIB_ROOT"] = self.deps_cpp_info['zlib'].rootpath
        if self.options.with_libevent:
            cmake.definitions["LIBEVENT_ROOT"] = self.deps_cpp_info['libevent'].rootpath

        cmake.configure(source_folder=self.source_subfolder, build_folder=self.build_subfolder)
        return cmake

    def build(self):
        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self.source_subfolder)
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        # Make 'thrift' compiler available to consumers
        self.env_info.path.append(os.path.join(self.package_folder, "bin"))
        self.cpp_info.libs = tools.collect_libs(self)

        if self.settings.os == "Windows":
            self.cpp_info.defines.append("NOMINMAX") # To avoid error C2589: '(' : illegal token on right side of '::'