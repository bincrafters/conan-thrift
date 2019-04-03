# -*- coding: utf-8 -*-
import os
from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration


class ThriftConan(ConanFile):
    name = "thrift"
    version = "0.12.0"
    description = "Thrift is an associated code generation mechanism for RPC"
    url = "https://github.com/helmesjo/conan-thrift"
    homepage = "https://github.com/apache/thrift"
    author = "helmesjo <helmesjo@gmail.com>"
    topics = ("conan", "thrift", "serialization", "rpc")
    license = "Apache-2.0"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
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
        "build_examples": [True, False],
        "build_tutorials": [True, False]
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "with_zlib": True,
        "with_libevent": True,
        "with_qt4": False,
        "with_qt5": False,
        "with_openssl": True,
        "with_boost_functional": False,
        "with_boost_smart_ptr": False,
        "with_boost_static": False,
        "with_boostthreads": False,
        "with_stdthreads": True,
        "with_c_glib": False,
        "with_cpp": True,
        "with_java": False,
        "with_python": False,
        "with_haskell": False,
        "with_plugin": False,
        "build_libraries": True,
        "build_compiler": True,
        "build_examples": False,
        "build_tutorials": False,
    }
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == 'Windows':
            del self.options.fPIC

    def configure(self):
        # See: https://github.com/apache/thrift/blob/v0.12.0/build/cmake/DefinePlatformSpecifc.cmake
        if self.settings.os == "Windows" and self.options.shared:
            raise ConanInvalidConfiguration("Thrift does not currently support shared libs on windows. Forcing static...")

    def requirements(self):
        self.requires("boost/1.69.0@conan/stable")
        if self.settings.os == 'Windows':
            self.requires("winflexbison/2.5.17@bincrafters/stable")
        else:
            self.requires("flex/2.6.4@bincrafters/stable")
            self.requires("bison/3.0.5@bincrafters/stable")

        if self.options.with_openssl:
            self.requires("OpenSSL/1.0.2q@conan/stable")
        if self.options.with_zlib:
            self.requires("zlib/1.2.11@conan/stable")
        if self.options.with_libevent:
            self.requires("libevent/2.1.8@bincrafters/stable")

    def source(self):
        sha256 = "b7452d1873c6c43a580d2b4ae38cfaf8fa098ee6dc2925bae98dce0c010b1366"
        tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, self.version), sha256=sha256)
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        for option, value in self.options.items():
            cmake.definitions[option.upper()] = value

        # Make thrift use correct thread lib (see repo/build/cmake/config.h.in)
        cmake.definitions["USE_STD_THREAD"] = self.options.with_stdthreads
        cmake.definitions["USE_BOOST_THREAD"] = self.options.with_boostthreads
        cmake.definitions["WITH_SHARED_LIB"] = self.options.shared
        cmake.definitions["WITH_STATIC_LIB"] = not self.options.shared
        cmake.definitions["BOOST_ROOT"] = self.deps_cpp_info['boost'].rootpath
        cmake.definitions["BUILD_TESTING"] = False

        # Make optional libs "findable"
        if self.options.with_openssl:
            cmake.definitions["OPENSSL_ROOT_DIR"] = self.deps_cpp_info['OpenSSL'].rootpath
        if self.options.with_zlib:
            cmake.definitions["ZLIB_ROOT"] = self.deps_cpp_info['zlib'].rootpath
        if self.options.with_libevent:
            cmake.definitions["LIBEVENT_ROOT"] = self.deps_cpp_info['libevent'].rootpath

        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()
        # Copy generated headers from build tree
        build_source_dir = os.path.join(self._build_subfolder, self._source_subfolder)
        self.copy(pattern="*.h", dst="include", src=build_source_dir, keep_path=True)

    def package_info(self):
        # Make 'thrift' compiler available to consumers
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
        self.cpp_info.libs = tools.collect_libs(self)
        # Make sure libs are link in correct order. Important thing is that libthrift/thrift is last
        # (a little naive to sort, but libthrift/thrift should end up last since rest of the libs extend it with an abbrevation: 'thriftnb', 'thriftz')
        # The library that needs symbols must be first, then the library that resolves the symbols should come after.
        self.cpp_info.libs.sort(reverse = True)

        if self.settings.os == "Windows":
            # To avoid error C2589: '(' : illegal token on right side of '::'
            self.cpp_info.defines.append("NOMINMAX")
        elif self.settings.os == "Linux":
            self.cpp_info.libs.extend(["m", "pthread"])
