# -*- coding: utf-8 -*-
from conans import ConanFile, tools


class TestPackageConan(ConanFile):
    settings = "os", "arch"

    def build(self):
        pass

    def test(self):
        if tools.cross_building(self.settings):
            self.output.warn("Skipping test package: Target is incompatible with current arch.")
        self.run("thrift --version", run_environment=True)
