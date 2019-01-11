# -*- coding: utf-8 -*-

import os
from conans import ConanFile, tools
from conans.util.env_reader import get_env
import tempfile


class DirectXInstallerConan(ConanFile):
    name = 'directx_installer'
    version = 'Jun10'
    description = 'Microsoft DirectX is a collection of application programming interfaces (APIs) for handling tasks related to multimedia, especially game programming and video, on Microsoft platforms.'
    url = 'https://github.com/bincrafters/conan-directx'
    homepage = 'https://www.microsoft.com/en-us/download/details.aspx?id=6812'
    author = 'bincrafters <bincrafters@gmail.com>'

    license = 'MSEULA'

    settings = {'os_build': ['Windows'], 'arch_build': None}

    build_requires = ('7z_installer/1.0@conan/stable',)

    def build(self):
        name = 'DXSDK_{}.exe'.format(self.version)
        url = 'https://download.microsoft.com/download/A/E/7/AE743F1F-632B-4809-87A9-AA1BB3458E31/{}'.format(name)
        sha256 = '9f818a977c32b254af5d649a4cec269ed8762f8a49ae67a9f01101a7237ae61a'

        targetdlfn = '{}'.format(os.path.join(tempfile.gettempdir(), name))

        if os.path.exists(targetdlfn) and not get_env('DIRECTX9_FORCE_DOWNLOAD', False):
            self.output.info('Skipping download. Using cached {}'.format(targetdlfn))
        else:
            self.output.info('Downloading sdk from {} to {}'.format(url, targetdlfn))
            tools.download(url, targetdlfn)
        tools.check_sha256(targetdlfn, sha256)

        self.run('7z x "{}" -y'.format(targetdlfn))

        dirs = [
            os.path.join('DXSDK', 'Include'),
            os.path.join('DXSDK', 'Lib', 'x86'),
            os.path.join('DXSDK', 'Lib', 'x64'),
        ]
        for d in dirs:
            for f in os.listdir(d):
                fp = os.path.join(d, f)
                import stat
                os.chmod(fp, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWOTH)

    def package(self):
        base_folder = os.path.join(self.build_folder, 'DXSDK')
        if self.settings.arch_build == 'x86':
            bin_folder = os.path.join(base_folder, 'Utilities', 'bin', 'x86')
        elif self.settings.arch_build == 'x86_64':
            bin_folder = os.path.join(base_folder, 'Utilities', 'bin', 'x64')
        self.copy(pattern='*', dst='bin', src=bin_folder)
        self.copy(pattern='*', dst='licenses', src=os.path.join(base_folder, 'Documentation', 'License Agreements'))

    def package_info(self):
        self.cpp_info.bindirs = [os.path.join(self.package_folder, 'bin')]

        for bindir in self.cpp_info.bindirs:
            self.output.info('Appending PATH environment variable: {}'.format(bindir))
            self.env_info.PATH.append(bindir)
