# -*- coding: utf-8 -*-
import os
from conans import ConanFile, tools


class ThriftBase(ConanFile):
    version = "0.12.0"
    description = "Thrift is an associated code generation mechanism for RPC"
    url = "https://github.com/helmesjo/conan-thrift"
    homepage = "https://github.com/apache/thrift"
    author = "helmesjo <helmesjo@gmail.com>"
    topics = ("conan", "thrift", "serialization", "rpc")
    license = "Apache-2.0"
    exports = ["LICENSE.md", "thrift_base.py"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def source(self):
        sha256 = "b7452d1873c6c43a580d2b4ae38cfaf8fa098ee6dc2925bae98dce0c010b1366"
        tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, self.version), sha256=sha256)
        extracted_dir = "thrift-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()
