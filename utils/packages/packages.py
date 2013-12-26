"""
Classes for working with the Ultros-contrib repository

These can be used within a plugin, but they're mostly used by the package
management script.
"""

__author__ = 'Gareth Coles'

import os
import pip
import shutil
import urllib
import urllib2
import yaml

from utils.data import YamlData


class Packages(object):

    """
    Class responsible for loading up plugin info, retrieving files
    and generally handling GitHub and the filesystem.

    I was a little lazy in writing this - but plugins aren't really supposed
    to use this anyway. Of course, that doesn't mean they can't!
    """

    data = {}
    packages = []
    config = None

    base_file_url = "https://raw.github.com/McBlockitHelpbot/Ultros-contrib/" \
                    "master/"

    info_file = "packages.yml"
    package_info_file = "package.yml"
    package_versions_file = "versions.yml"

    def __init__(self):
        info_url = self.base_file_url + self.info_file
        response = urllib2.urlopen(info_url)
        data = response.read()

        self.config = YamlData("packages.yml")
        if len(self.config) == 0:
            self.config["installed"] = {}

        self.data = yaml.load(data)
        self.packages = sorted(self.data.keys())

    def _get_file(self, base_path, path):
        if os.path.exists(path):
            raise ValueError("A file at `%s` already exists" % path)

        constructed_path = self.base_file_url + base_path + path
        urllib.urlretrieve(constructed_path, path)

    def get_package_info(self, package):
        if package in self.packages:
            url = self.base_file_url + package + "/" \
                                     + self.package_info_file

            response = urllib2.urlopen(url)
            data = response.read()

            return yaml.load(data)
        return None

    def get_package_versions(self, package):
        if package in self.packages:
            url = self.base_file_url + package + "/" \
                                     + self.package_versions_file

            response = urllib2.urlopen(url)
            data = response.read()

            return yaml.load(data)
        return None

    def package_installed(self, package):
        return package in self.config["installed"]

    def install_package(self, package):
        if self.package_installed(package):
            raise ValueError("Package '%s' is already installed"
                             % package)
        info = self.get_package_info(package)
        files = info["files"]

        conflicts = {"files": [], "folders": []}

        for _file in files:
            if _file[-1] == "/":
                if not os.path.exists(_file):
                    os.mkdir(_file)
                else:
                    path = _file
                    conflicts["folders"].append(path)
            else:
                if not os.path.exists(_file):
                    self._get_file(package + "/", _file)
                else:
                    path = _file
                    conflicts["files"].append(path)

        requirements = info["requires"]
        for module in requirements["modules"]:
            try:
                __import__(module)
            except ImportError:
                pip.main(["install", module])

        for new_package in requirements["packages"]:
            if not self.package_installed(new_package):
                self.install_package(new_package)

        with self.config:
            self.config["installed"][package] =\
                info["current_version"]["number"]

        return conflicts

    def update_package(self, package):
        if not self.package_installed(package):
            raise ValueError("Package '%s' is not installed"
                             % package)

        self.uninstall_package(package)
        self.install_package(package)

    def uninstall_package(self, package):
        if not self.package_installed(package):
            raise ValueError("Package '%s' is not installed"
                             % package)

        info = self.get_package_info(package)
        files = info["files"]
        files.reverse()

        for _file in files:
            if os.path.exists(_file):
                if os.path.isdir(_file):
                    shutil.rmtree(_file)
                else:
                    os.remove(_file)

        with self.config:
            del self.config["installed"][package]

    def __len__(self):
        return len(self.data)
