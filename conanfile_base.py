# -*- coding: utf-8 -*-
import os
from conans import ConanFile, tools


class ConanFileBase(ConanFile):
    _base_name = "thrift"
    version = "0.12.0"
    description = "Thrift is an associated code generation mechanism for RPC"
    topics = ("conan", "thrift", "serialization", "rpc")
    url = "https://github.com/swissembedded/conan-thrift"
    homepage = "https://github.com/apache/thrift"
    author = "Daniel Haensse <daniel.haensse@swissembedded.com>"
    license = "Apache-2.0"
    exports = ["LICENSE.md", "conanfile_base.py", "patches/thrift-0.12.0_t_cpp_generator_struct_less_operator.patch", "patches/thrift-0.12.0_t_cpp_generator_struct_less_operator_DebugProtoTest_extras.cpp.patch", "patches/thrift-0.12.0_t_cpp_generator_struct_operator_less_ThriftTest_extras.patch"]
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
        _patch_source_dir = os.path.join(self.source_folder, self._source_subfolder)
        print(_patch_source_dir)
        # patching cpp struct less operator
        tools.patch(_patch_source_dir, os.path.join(self.source_folder,"patches/thrift-0.12.0_t_cpp_generator_struct_less_operator.patch"))
        # patching tests
        tools.patch(_patch_source_dir, os.path.join(self.source_folder, "patches/thrift-0.12.0_t_cpp_generator_struct_less_operator_DebugProtoTest_extras.cpp.patch"))
        tools.patch(_patch_source_dir, os.path.join(self.source_folder, "patches/thrift-0.12.0_t_cpp_generator_struct_operator_less_ThriftTest_extras.patch"))

        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()
