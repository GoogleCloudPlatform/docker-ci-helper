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

# On Travis, gcloud sdk does not come with docker credential helper
# and also does not allow `gcloud components install` command. We need
# to install it manually for running `gcloud auth configure-docker`

set -e

CLOUD_SDK_VERSION=300.0.0

wget https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz \
     -O /tmp/google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz

cd /tmp
tar xzf google-cloud-sdk-${CLOUD_SDK_VERSION}-linux-x86_64.tar.gz
/tmp/google-cloud-sdk/install.sh
/tmp/google-cloud-sdk/bin/gcloud components install docker-credential-gcr
