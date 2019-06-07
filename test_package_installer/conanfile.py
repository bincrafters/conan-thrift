# -*- coding: utf-8 -*-

from conans import ConanFile, tools


class TestPackageConan(ConanFile):

    def test(self):
        if not tools.cross_building(self.settings):
            self.run("thrift --version", run_environment=True)
