# Poetry CDK plugin
# Copyright (C) 2023-present  Olivier Schmitt
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
import os
import subprocess

from cleo.io.io import IO
from poetry.console.commands.env_command import EnvCommand


class BaseCDKCommand(EnvCommand):
    def handle(self) -> None:
        pass  # Nothing to do

    @property
    def cdk_cli_args(self) -> [str]:
        return []

    def execute(self, io: IO) -> int:
        venv_error = (
            f"Can not execute {self.cdk_cli_args} because command can not run in"
            " virtual env"
        )
        command = ["cdk"] + self.cdk_cli_args
        try:
            if self.env.is_venv():
                # Is supposed to be a VirtualEnv
                env = dict(self.env.get_temp_environ())
                exe = subprocess.Popen(command, env=env, cwd=os.getcwd())
                exe.communicate()
                return exe.returncode
            else:
                io.write_error_line(venv_error)
                return -1
        except NotImplementedError:
            io.write_error_line(venv_error)


class SynthCommand(BaseCDKCommand):
    name = "cdk synth"
    description = "Synth a CDK application"

    @property
    def cdk_cli_args(self) -> [str]:
        return ["synth"]


class DeployCommand(BaseCDKCommand):
    name = "cdk deploy"
    description = "Deploy a CDK application"

    @property
    def cdk_cli_args(self) -> [str]:
        return 'deploy "*" --require-approval never'.split()


class DestroyCommand(BaseCDKCommand):
    name = "cdk destroy"
    description = "Destroy a CDK application"

    @property
    def cdk_cli_args(self) -> [str]:
        return 'destroy "*" --force'.split()
