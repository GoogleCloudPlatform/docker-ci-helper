#!/usr/bin/env bash
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

# Shortcut to run the tests locally.

export TRAMPOLINE_BUILD_FILE=tests/python/run_tests.sh
export TRAMPOLINE_IMAGE=gcr.io/cloud-devrel-kokoro-resources/docker-ci-helper/python
export TRAMPOLINE_DOCKERFILE=docker/python/Dockerfile
export TEST_ENV=test

PROGRAM_PATH="$(realpath "$0")"
PROGRAM_DIR="$(dirname "${PROGRAM_PATH}")"
cd "${PROGRAM_DIR}"
./trampoline_v2.sh
