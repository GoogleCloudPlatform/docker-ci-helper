#!/usr/bin/env python
# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import subprocess
import tempfile

def test_docker():
    """A test for Docker commands."""
    docker_build_command = [
        'docker', 'build', '-t', 'python-test', '-f', 'testdata/Dockerfile', '.'
    ]
    result = subprocess.run(docker_build_command)
    assert result.returncode == 0

    # We need to use /tmp if we mount the file. Trampoline mounts
    # `/tmp` directory on the host at the same path. With Docker in
    # Docker, you have to use path under /tmp for the mount feature to
    # work correctly.
    with tempfile.NamedTemporaryFile(mode='w', dir='/tmp', delete=True) as f:
        f.write('words of wisdom')
        f.seek(0)
        docker_run_command = [
            'docker', 'run', '-v', f'{f.name}:{f.name}', 'python-test', 'cat',
            f'{f.name}'
        ]
        result = subprocess.run(docker_run_command, stdout=subprocess.PIPE)
        assert result.returncode == 0
        assert 'words of wisdom' == result.stdout.decode('utf-8')
