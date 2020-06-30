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
# nlimitations under the License.

import os


def test_envvar():
    assert 'TRAMPOLINE_VERSION' in os.environ
    assert os.environ['TRAMPOLINE_VERSION'][0] == '2'
    assert 'RUNNING_IN_CI' in os.environ
    if os.environ['RUNNING_IN_CI'] == 'true':
        assert 'TRAMPOLINE_CI' in os.environ
        # This is set in .travis.yml
        assert os.environ.get('TEST_ENV') == 'test'
    # Travis
    if 'TRAVIS' in os.environ:
        assert "TRAVIS_BRANCH" in os.environ
        assert "TRAVIS_BUILD_ID" in os.environ
        assert "TRAVIS_BUILD_NUMBER" in os.environ
        assert "TRAVIS_BUILD_WEB_URL" in os.environ
        assert "TRAVIS_COMMIT" in os.environ
        assert "TRAVIS_COMMIT_MESSAGE" in os.environ
        assert "TRAVIS_COMMIT_RANGE" in os.environ
        assert "TRAVIS_JOB_NAME" in os.environ
        assert "TRAVIS_JOB_NUMBER" in os.environ
        assert "TRAVIS_JOB_WEB_URL" in os.environ
        assert "TRAVIS_REPO_SLUG" in os.environ
        assert "TRAVIS_SECURE_ENV_VARS" in os.environ
