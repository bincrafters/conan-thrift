#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class ThriftConan(ConanFile):
    name = "thrift"
    version = "0.11.0"
    description =   "Thrift is a lightweight, \
                    language-independent software \
                    stack with an associated code \
                    generation mechanism for RPC."
    url = "https://github.com/helmesjo/conan-thrift"
    homepage = "https://github.com/original_author/original_lib"

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
        "flex/2.6.4@bincrafters/stable",
        "bison/3.0.4@bincrafters/stable",
        "libevent/2.1.8@bincrafters/stable",
        "zlib/1.2.11@conan/stable",
        "OpenSSL/1.1.0g@conan/stable",
    )

    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "build_qt4_lib": [True, False],
        "build_qt5_lib": [True, False],
        "build_c_glib_lib": [True, False],
        "build_csharp_lib": [True, False],
        "build_java_lib": [True, False],
        "build_erlang_lib": [True, False],
        "build_nodejs_lib": [True, False],
        "build_lua_lib": [True, False],
        "build_python_lib": [True, False],
        "build_perl_lib": [True, False],
        "build_php_lib": [True, False],
        "build_php_extension_lib": [True, False],
        "build_ruby_lib": [True, False],
        "build_haskell_lib": [True, False],
        "build_go_lib": [True, False],
        "build_d_lib": [True, False],
        "build_tests": [True, False],
        "build_tutorials": [True, False],
        "build_examples": [True, False],
    }

    default_options = (
        "shared=False",
        "fPIC=True",
        "build_qt4_lib=False",
        "build_qt5_lib=False",
        "build_c_glib_lib=False",
        "build_csharp_lib=False",
        "build_java_lib=False",
        "build_erlang_lib=False",
        "build_nodejs_lib=False",
        "build_lua_lib=False",
        "build_python_lib=False",
        "build_perl_lib=False",
        "build_php_lib=False",
        "build_php_extension_lib=False",
        "build_ruby_lib=False",
        "build_haskell_lib=False",
        "build_go_lib=False",
        "build_d_lib=False",
        "build_tests=False",
        "build_tutorials=False",
        "build_examples=False",
    )

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def source(self):
        source_url = "https://github.com/apache/thrift"
        tools.get("{0}/archive/{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version

        #Rename to "source_subfolder" is a convention to simplify later steps
        os.rename(extracted_dir, self.source_subfolder)

    def configure_cmake(self):
        cmake = CMake(self)

        if self.settings.os != 'Windows':
            cmake.definitions['CMAKE_POSITION_INDEPENDENT_CODE'] = self.options.fPIC

        cmake.definitions["BUILD_TESTING"] = self.options.build_tests
        cmake.definitions["BUILD_EXAMPLES"] = self.options.build_examples
        cmake.definitions["BUILD_TUTORIALS"] = self.options.build_tutorials

        cmake.definitions["BOOST_ROOT"] = self.deps_cpp_info['boost'].rootpath
        cmake.definitions["OPENSSL_ROOT_DIR"] = self.deps_cpp_info['OpenSSL'].rootpath
        cmake.definitions["ZLIB_ROOT"] = self.deps_cpp_info['zlib'].rootpath

        cmake.configure(source_folder=self.source_subfolder, build_folder=self.build_subfolder)
        return cmake

    def build(self):

        def option_to_flag(opt, value):
            flag_name = opt.replace('build_', '')
            return '--with-{}={}'.format(flag_name, 'yes' if value else 'no')

        build_flags = []
        for attr, _ in self.options.iteritems():
            value = getattr(self.options, attr)
            build_flags.append(option_to_flag(attr, value))

        integration_flags = [
            "--with-boost={}".format(self.deps_cpp_info['boost'].rootpath),
            "--with-openssl={}".format(self.deps_cpp_info['OpenSSL'].rootpath),
            "--with-zlib={}".format(self.deps_cpp_info['zlib'].rootpath),
            "--with-libevent={}".format(self.deps_cpp_info['libevent'].rootpath),
        ]

        flags = "{} {}".format(
                " ".join(build_flags),
                " ".join(integration_flags)
                )

        print("config_options: %s" % flags)

        with tools.chdir(self.source_subfolder):
            self.run('./bootstrap.sh')
            self.run("./configure {}".format(flags))

        cmake = self.configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self.source_subfolder)
        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
