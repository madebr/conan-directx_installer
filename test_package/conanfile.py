# -*- coding: utf-8 -*-

from conans import ConanFile, tools
from conans.errors import ConanException
import os

class DirectXInstallerTestConan(ConanFile):
    exports_sources = 'bincrafters.png'

    def build(self):
        with tools.chdir(self.source_folder):
            self.run('texconv -w 256 -h 256 -f A8R8G8B8 -nologo -o "{outdir}" "bincrafters.png"'.format(outdir=self.build_folder))

    def test(self):
        dds_file = os.path.join(self.build_folder, 'bincrafters.dds')
        if not os.path.exists(dds_file):
            raise ConanException('Texture converter did not run')
