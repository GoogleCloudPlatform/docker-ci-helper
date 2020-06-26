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

## trampoline_v2.sh

This script does 3 things.

1. Prepare the Docker image for the test.
2. Run Docker with appropriate flags to run the test.
3. Upload the newly built Docker image.

We'll discuss each steps in detail.

### Prepare the Docker image

1. Try to download a Docker image specified by `TRAMPOLINE_IMAGE`
   environment variable.
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

The following environment variables are passed down into the container in Kokoro build.

* `KOKORO_BUILD_NUMBER`
* `KOKORO_BUILD_ID`
* `KOKORO_JOB_NAME`
* `KOKORO_GIT_COMMIT`
* `KOKORO_GITHUB_COMMIT`
* `KOKORO_GITHUB_PULL_REQUEST_NUMBER`
* `KOKORO_GITHUB_PULL_REQUEST_COMMIT`
* `KOKORO_GITHUB_COMMIT_URL`
* `KOKORO_GITHUB_PULL_REQUEST_URL`

The following environment variables are passed down into the container in travis build.

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
pointing to that file.

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
* `TRAMPOLINE_SKIP_DOWNLOAD_IMAGE`: Skip downloading the image when
  you know you have the image locally.
* `TRAMPOLINE_SERVICE_ACCOUNT`: A service account json file for
  authentication.

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
