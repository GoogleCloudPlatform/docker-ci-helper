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
    assert 'PROJECT_ROOT' in os.environ
    # It's /workspace unless we customize.
    assert os.environ['PROJECT_ROOT'] == '/workspace'
    assert 'RUNNING_IN_CI' in os.environ
    # This is set in .travis.yml or .kokoro/python/common.cfg
    assert os.environ.get('TEST_ENV') == 'test'
    if os.environ['RUNNING_IN_CI'] == 'true':
        ci_envvars_tested = False
        assert 'TRAMPOLINE_CI' in os.environ
        # Travis
        if os.environ['TRAMPOLINE_CI'] == 'travis':
            assert 'TRAVIS_BRANCH' in os.environ
            assert 'TRAVIS_BUILD_ID' in os.environ
            assert 'TRAVIS_BUILD_NUMBER' in os.environ
            assert 'TRAVIS_BUILD_WEB_URL' in os.environ
            assert 'TRAVIS_COMMIT' in os.environ
            assert 'TRAVIS_COMMIT_MESSAGE' in os.environ
            assert 'TRAVIS_JOB_NUMBER' in os.environ
            assert 'TRAVIS_JOB_WEB_URL' in os.environ
            assert 'TRAVIS_REPO_SLUG' in os.environ
            assert 'TRAVIS_SECURE_ENV_VARS' in os.environ
            assert 'TRAVIS_PULL_REQUEST' in os.environ
            if os.environ['TRAVIS_PULL_REQUEST'] != 'false':
                assert 'TRAVIS_PULL_REQUEST_BRANCH' in os.environ
                assert 'TRAVIS_PULL_REQUEST_SHA' in os.environ
                assert 'TRAVIS_PULL_REQUEST_SLUG' in os.environ
            ci_envvars_tested = True
        # Kokoro
        elif os.environ['TRAMPOLINE_CI'] == 'kokoro':
            assert 'KOKORO_BUILD_NUMBER' in os.environ
            assert 'KOKORO_BUILD_ID' in os.environ
            assert 'KOKORO_JOB_NAME' in os.environ
            assert 'KOKORO_GIT_COMMIT' in os.environ
            if os.environ['KOKORO_JOB_NAME'].endswith('presubmit'):
                assert 'KOKORO_GITHUB_PULL_REQUEST_NUMBER' in os.environ
                assert 'KOKORO_GITHUB_PULL_REQUEST_COMMIT' in os.environ
                assert 'KOKORO_GITHUB_PULL_REQUEST_URL' in os.environ
            ci_envvars_tested = True
        # Github workflow
        elif os.environ['TRAMPOLINE_CI'] == 'github-workflow':
            assert 'GITHUB_WORKFLOW' in os.environ
            assert 'GITHUB_RUN_ID' in os.environ
            assert 'GITHUB_RUN_NUMBER' in os.environ
            assert 'GITHUB_ACTOR' in os.environ
            assert 'GITHUB_REPOSITORY' in os.environ
            assert 'GITHUB_EVENT_NAME' in os.environ
            assert 'GITHUB_EVENT_PATH' in os.environ
            assert 'GITHUB_SHA' in os.environ
            ci_envvars_tested = True

        # Make sure we test the ci specific env vars.
        assert ci_envvars_tested
