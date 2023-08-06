# Copyright (C) 2021-2022 Greenbone Networks GmbH
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
from pathlib import Path
from typing import Literal, Union

from .errors import VersionError
from .helper import get_last_release_version
from .version import Version, VersionCommand, VersionUpdate, parse_version

VERSION_MATCH = r'var [Vv]ersion = "([abcderv0-9.+]+)"'
TEMPLATE = """package main

// THIS IS AN AUTOGENERATED FILE. DO NOT TOUCH!

var version = "{}"
\n"""


# This class is used for Go Version command(s)
class GoVersionCommand(VersionCommand):
    project_file_name = "go.mod"
    version_file_path = Path("version.go")

    def _update_version_file(self, new_version: Version) -> None:
        """
        Update the version file with the new version
        """
        if self.version_file_path.exists():
            version = self.get_current_version()
            template = self.version_file_path.read_text(
                encoding="utf-8"
            ).replace(str(version), str(new_version))
        else:
            template = TEMPLATE.format(str(new_version))
        self.version_file_path.write_text(template, encoding="utf-8")

    def get_current_version(self) -> Version:
        """Get the current version of this project
        In go the version is only defined within the repository
        tags, thus we need to check git, what tag is the latest"""
        if self.version_file_path.exists():
            version_file_text = self.version_file_path.read_text(
                encoding="utf-8"
            )
            match = re.search(VERSION_MATCH, version_file_text)
            if match:
                return parse_version(match.group(1))
            else:
                raise VersionError(
                    f"No version found in the {self.version_file_path} file."
                )
        else:
            raise VersionError(
                f"No {self.version_file_path} file found. "
                "This file is required for pontos"
            )

    def verify_version(
        self, version: Union[Literal["current"], Version]
    ) -> None:
        """Verify the current version of this project"""
        current_version = self.get_current_version()
        if current_version != version:
            raise VersionError(
                f"Provided version {version} does not match the "
                f"current version {current_version}."
            )

    def update_version(
        self, new_version: Version, *, force: bool = False
    ) -> VersionUpdate:
        """Update the current version of this project"""
        try:
            current_version = self.get_current_version()
        except VersionError:
            current_version = get_last_release_version("v")

        if not force and new_version == current_version:
            return VersionUpdate(previous=current_version, new=new_version)

        self._update_version_file(new_version=new_version)

        return VersionUpdate(
            previous=current_version,
            new=new_version,
            changed_files=[self.version_file_path],
        )
