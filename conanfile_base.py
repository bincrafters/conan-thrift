import os
import glob
from conans import ConanFile, tools


class ConanFileBase(ConanFile):
    _base_name = "thrift"
    version = "0.13.0"
    description = "Thrift is an associated code generation mechanism for RPC"
    topics = ("conan", "thrift", "serialization", "rpc")
    url = "https://github.com/bincrafters/conan-thrift"
    homepage = "https://github.com/apache/thrift"
    author = "helmesjo <helmesjo@gmail.com>"
    license = "Apache-2.0"
    exports = ["LICENSE.md", "conanfile_base.py", "patches/*.patch"]
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def source(self):
        sha256 = "8469c8d72c684c6de72ddf55fc65d1c10868a576e7dc4d1f4a21a59814b97110"
        tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, self.version), sha256=sha256)
        extracted_dir = "thrift-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        if self.version == "0.12.0":
            for filename in sorted(glob.glob("patches/*.patch")):
                self.output.info('applying patch "%s"' % filename)
                tools.patch(base_path=self._source_subfolder, patch_file=filename)

        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()
