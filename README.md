# docker-ci-helper

This repository contains `trampoline_v2.sh`, a shell script for
running another script in a Docker container. The primary use case of
this shell script is to use it as a test driver on various CI
systems.

You provide a Docker image and a build script. Trampoline V2 will run
the Docker image, mounting the source files and the build script, then
run the build script in the Docker container.

This way, your tests are always executed in the same Docker image. It
will allow you to run the tests in various environments including any
CI systems, as well as on your local workstation without worrying
about installing the test dependencies.

Note: If you want to migrate your builds from Trampoline V1 to
Trampoline V2, also read
[`MIGRATING_FROM_V1.md`](https://github.com/GoogleCloudPlatform/docker-ci-helper/blob/master/MIGRATING_FROM_V1.md).

## trampoline_v2.sh

This script does 3 things.

1. Prepare the Docker image for the test.
2. Run Docker with appropriate flags to run the test.
3. Upload the newly built Docker image.

We'll discuss each steps in detail.

### Prepare the Docker image

1. Try to download a Docker image specified by `TRAMPOLINE_IMAGE`
   environment variable in CI builds.
2. If `TRAMPOLINE_DOCKERFILE` environment variable is specified, it
   will build the Docker image from that Dockerfile. If there's a
   downloaded Docker image, Trampoline V2 uses the downloaded image as
   a cache.

We recomnend you have the Dockerfile in the same repository as your
build file and your tests, then specify `TRAMPOLINE_DOCKERFILE`. This
will allow you to create a single pull request containing changes in
tests as well as changes in the Dockerfile.

### Run Docker with appropriate flags to run the test

* Trampoline V2 will mount the project source code at /workspace (it
  assumes the upward closest git root as the project root).
* Trampoline V2 will add appropriate environment variables.
* Trampoline V2 will use invoker's uid and the Docker gid on the host.
* Trampoline V2 will run a command specified by
  `TRAMPOLINE_BUILD_FILE` environment variable.
* Trampoline V2 will exit with the same exit code as the build file.

#### Environment variables which will be passed down into the container

The following environment variables are passed down into the container.

| envvar name                         | Description                                                  |
| ----------------------------------  | ----------------------------------------                     |
| `RUNNING_IN_CI`                     | Tells scripts whether they are running as part of CI or not. |
| `TRAMPOLINE_CI`                     | Indicates which CI system we're in.                          |
| `TRAMPOLINE_VERSION`                | Indicates the version of the script.                         |

The following environment variables are passed down into the container
in Kokoro builds:

* `KOKORO_BUILD_NUMBER`
* `KOKORO_BUILD_ID`
* `KOKORO_JOB_NAME`
* `KOKORO_GIT_COMMIT`
* `KOKORO_GITHUB_COMMIT`
* `KOKORO_GITHUB_PULL_REQUEST_NUMBER`
* `KOKORO_GITHUB_PULL_REQUEST_COMMIT`
* `KOKORO_GITHUB_COMMIT_URL`
* `KOKORO_GITHUB_PULL_REQUEST_URL`

The following environment variables are passed down into the container
in travis builds:

* `TRAVIS_BRANCH`
* `TRAVIS_BUILD_ID`
* `TRAVIS_BUILD_NUMBER`
* `TRAVIS_BUILD_WEB_URL`
* `TRAVIS_COMMIT`
* `TRAVIS_COMMIT_MESSAGE`
* `TRAVIS_COMMIT_RANGE`
* `TRAVIS_JOB_NAME`
* `TRAVIS_JOB_NUMBER`
* `TRAVIS_JOB_WEB_URL`
* `TRAVIS_PULL_REQUEST`
* `TRAVIS_PULL_REQUEST_BRANCH`
* `TRAVIS_PULL_REQUEST_SHA`
* `TRAVIS_PULL_REQUEST_SLUG`
* `TRAVIS_REPO_SLUG`
* `TRAVIS_SECURE_ENV_VARS`
* `TRAVIS_TAG`

The following environment variables are passed down into the container
in github workflow builds:

* `GITHUB_WORKFLOW`
* `GITHUB_RUN_ID`
* `GITHUB_RUN_NUMBER`
* `GITHUB_ACTION`
* `GITHUB_ACTIONS`
* `GITHUB_ACTOR`
* `GITHUB_REPOSITORY`
* `GITHUB_EVENT_NAME`
* `GITHUB_EVENT_PATH`
* `GITHUB_SHA`
* `GITHUB_REF`
* `GITHUB_HEAD_REF`
* `GITHUB_BASE_REF`

The following environment variables are passed down into the container
in circleci builds:

* `CIRCLE_BRANCH`
* `CIRCLE_BUILD_NUM`
* `CIRCLE_BUILD_URL`
* `CIRCLE_COMPARE_URL`
* `CIRCLE_JOB`
* `CIRCLE_NODE_INDEX`
* `CIRCLE_NODE_TOTAL`
* `CIRCLE_PREVIOUS_BUILD_NUM`
* `CIRCLE_PROJECT_REPONAME`
* `CIRCLE_PROJECT_USERNAME`
* `CIRCLE_REPOSITORY_URL`
* `CIRCLE_SHA1`
* `CIRCLE_STAGE`
* `CIRCLE_USERNAME`
* `CIRCLE_WORKFLOW_ID`
* `CIRCLE_WORKFLOW_JOB_ID`
* `CIRCLE_WORKFLOW_UPSTREAM_JOB_IDS`
* `CIRCLE_WORKFLOW_WORKSPACE_ID`

### Upload the newly built Docker image

If `TRAMPOLINE_IMAGE_UPLOAD` environment variable is set to `true`,
Trampoline V2 will try to upload the newly built image to
`TRAMPOLINE_IMAGE` after the successful build.

This optional step allows you to upload the built image only after a
full build succeeds. To make this step work, you need to set up
authentication.

### Authentication

To set up authentication on Kokoro (Google internal CI system), we
recommend that you attach a service account to your VM instance and
add appropriate permissions.

On other CI systems, you need to securely pass a service account json
file and set `TRAMPOLINE_SERVICE_ACCOUNT` environment variable
pointing to that file. An example is available in our travis
builds([.travis.yml](https://github.com/GoogleCloudPlatform/docker-ci-helper/blob/master/.travis.yml)).
See also
[the Travis documentation](https://docs.travis-ci.com/user/encrypting-files/).

In either case, you need at least read permission on the Google
Container Registry artifact bucket. You also need write permission on
the bucket if you use the uploading feature.

### Environment variables

By design, all the parameters to Trampoline V2 are passed by
environment variables.

There are two required environment variables:
* `TRAMPOLINE_IMAGE`: The docker image to use. You can use Docker
  image URL on anywhere, but if you also want to upload the docker
  image, use an URL on Google Container Registry
  (gcr.io/PROJ/IMAGE_NAME).
* `TRAMPOLINE_BUILD_FILE`: The script to run in the docker
  container. It should be a relative path from the git root.

Optional environment variables:
* `TRAMPOLINE_DOCKERFILE`: The location of the Dockerfile. If
  specified, the script will start building a docker image from the
  Dockerfile.
* `TRAMPOLINE_IMAGE_UPLOAD`: (true|false): Whether to upload the
  Docker image after the successful builds.
* `TRAMPOLINE_WORKSPACE`: The workspace path in the docker container.
  Defaults to /workspace.
* `TRAMPOLINE_SERVICE_ACCOUNT`: A service account json file for
  authentication.

## Installation

Please copy the `trampoline_v2.sh` to your repository (
[example in python-docs-samples](https://github.com/GoogleCloudPlatform/python-docs-samples/blob/main/.kokoro/trampoline_v2.sh)
) and set `build_file` in your Kokoro build configuration to the
file ([example in python-docs-samples's python3.9 jobs](
https://github.com/GoogleCloudPlatform/python-docs-samples/blob/6d2cb2fae50370b3f6b9ba17c48fa137ce7f3f5b/.kokoro/python3.9/common.cfg#L29)).



## Customization

You can add repo specific configuration by having `.trampolinerc` at
the root of your git repository. You may want to copy
`.trampolinerc_template` from this repository and edit that file.

In this file, you can do:

* Set default values of some environment variables for your repository.
* Add elements to `required_envvars` and `pass_down_envvars`
  * `required_envvars` is the list of required environment
    variables. If any of these environment variables is not set, the
    script will abort with a message.
  * `pass_down_envvars` is the list of environment variables which are
    passed down into the container when the script invoke the Docker
    container.

## How to use `sudo` in the container

Trampoline V2 will run the Docker container with the user id who runs
the script. This means that you don't have root permission in the
container.

If you need to have the root permission, install `sudo` package in the
Docker image and add the following piece to your `Dockerfile`.

```Dockerfile
# Create a user and allow sudo
ARG UID
ARG USERNAME

# Add a new user with the caller's uid and the username. This is
# needed for ssh and sudo access.
RUN useradd -d /h -u ${UID} ${USERNAME}

# Allow nopasswd sudo
RUN echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
```

Trampoline V2 uses appropriate `UID` and `USERNAME` buildargs. You can
then use `sudo` command for whatever task that needs the root
permission. Look at the `tests/python/test_sudo.py` for a working
example.

## Examples

### Hello World!

Here is a minimum example of the usage.

```sh
$ mkdir tmp
$ echo '#!/bin/sh' > tmp/hello.sh
$ echo 'echo "Hello World!"' >> tmp/hello.sh
$ chmod +x tmp/hello.sh
$ TRAMPOLINE_IMAGE=bash TRAMPOLINE_BUILD_FILE=tmp/hello.sh ./trampoline_v2.sh
```

If you see "Hello World!", it's working.

### Real world examples

* `tests/python` directory has example tests and a build script. Currently it runs on travis. See `.travis.yml` file for configuration.
* [python-docs-samples
  repo](https://github.com/GoogleCloudPlatform/python-docs-samples)
  is using Trampoline V2 for running tests.
