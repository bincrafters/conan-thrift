# -*- coding: utf-8 -*-
from conans import ConanFile, tools


class TestPackageConan(ConanFile):
    settings = "os", "arch"

    def build(self):
        pass

    def test(self):
        if not tools.cross_building(self.settings):
            self.run("thrift --version", run_environment=True)
