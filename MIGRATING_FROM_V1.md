# Migration guide from Trampoline V1 script

This guide is solely for migrating from Trampoline V1 script. We
recommend that you read README.md before diving into this guide.

In this guide, we'll use
[getting-started-python](https://github.com/GoogleCloudPlatform/getting-started-python)
as an example repository.

## The first step - local run

The first step of the migration is to run the tests locally with
Trampoline V2 script. Copy trampoline_v2.sh into your repository. A
natural choice is to place the script alongside with the
`trampoline.sh`.

Here is an exmaple with our example repo. Make sure it has an
executable bit.

```sh
$ git clone git@github.com:GoogleCloudPlatform/getting-started-python.git
$ cd getting-started-python
$ cp ../docker-ci-helper/trampoline_v2.sh .kokoro
$ ls -al .kokoro/trampoline_v2.sh
-rwxr-x--- 1 user group 14591 Jul  9 20:28 .kokoro/trampoline_v2.sh
```

Then you will need to set some environment variables. We can mostly
reuse the current settings modulo small changes. Note we can omit the
`github/getting-started-python` part from `TRAMPOLINE_BUILD_FILE`. In
our example repo, you can see the current settings in
`.kokoro/common.cfg`.

Here we set mandatory environment variables `TRAMPOLINE_IMAGE` and
`TRAMPOLINE_BUILD_FILE`, as well as optional `TRAMPOLINE_VERBOSE` for
easier debugging.

```sh
export TRAMPOLINE_IMAGE=gcr.io/cloud-devrel-kokoro-resources/python@sha256:4b6ba8c199e96248980db4538065cddeea594138b9b9fb2d0388603922087747
export TRAMPOLINE_BUILD_FILE=.kokoro/system_tests.sh
export TRAMPOLINE_VERBOSE=true
```

Download the docker image locally.

```sh
docker pull "${TRAMPOLINE_IMAGE}"
```

Then run the script.

```sh
.kokoro/trampoline_v2.sh
```

The first run will likely fail, but make sure to see outputs like this:

```
2020-07-09T20:40:24Z: Running the tests in a Docker container.
================================================================
docker run ...
```

At least, it successfully run the container. The test likely fails due
to some differences between Trampoline V1 and V2. We'll fix the build
script in the next section.

## Modify the build script

Our first run failed with the following message:

```
.kokoro/system_tests.sh: line 21: cd: github/getting-started-python: No such file or directory
```

We can modify this line:

```
cd github/getting-started-python
```

to the following code:

```
cd "${PROJECT_ROOT:-github/getting-started-python}"
```

This change allows the build file compatible with both Trampoline V1
and V2.

The test still fails due to lack of secret file. We'll add secrets in
the next section.

## Add secrets for local run

Some tests need access to secret. On Kokoro, there are several ways to
do it.

* Using Secret Manager
* Using files in `KOKORO_GFILE_DIR` or `KOKORO_KEYSTORE_DIR`


Secret Manager is the recommended way. If you're using Secret Manager,
only you need to do is to setup right permission to use Secret
Manager.

If you use files in `KOKORO_GFILE_DIR` or `KOKORO_KEYSTORE_DIR`, we
can emulate it locally as follows.

On linux machines, you can download the required files into
`/dev/shm`. The files in `/dev/shm` are automatically available within
the container. Trampoline V2 script will pass down `KOKORO_GFILE_DIR`
and `KOKORO_KEYSTORE_DIR` environment variables into the container.

For example, for our example repo, we needed to do the following:

```sh
# Download the secret password into /dev/shm
$ gsutil cp gs://cloud-devrel-kokoro-resources/getting-started-python/secrets-password.txt /dev/shm
```

Then run the script:

```sh
$ .kokoro/trampoline_v2.sh
```

Now we get the following error:

```
.kokoro/system_tests.sh: line 32: nox: command not found
```

The docker image has `nox` intalled in `/root/.local/bin`, but it's
not available because Trampoline v2 runs the container as a normal
user.

Note: this is a bad practice. It is much better if you install
software available for normal users, instead of installing it into
root's home directory.

In a long run, we want to fix the Docker image itself, but now we have
a quick hack with the following code in the build file:

```sh
# This block is executed only with Trampoline V2.
if [[ -n "${TRAMPOLINE_VERSION:-}" ]]; then
    # Install nox as a user and add it to the PATH.
	python3 -m pip install --user nox
	export PATH="${PATH}:${HOME}/.local/bin"
fi
```

Now the test passes locally! We'll modify the Kokoro configurations in
the next section.

# Modify the Kokoro configuration files

## Kokoro job config change

### Permission to download the Docker image

On Kokoro, we need to have a permission to download the Docker image
from the Container Registry.

There are two ways to do this:

1. Attach a service account to the Kokoro VM
2. Use the Trampoline service account in the `trampoline` GCS bucket.

While it is recommended to use the first option, many Kokoro builds
with Trampoline V1 rely on a Trampoline service account stored in the
`trampoline` GCS bucket.

Trampoline supports both use cases.

If you want to rely on the legacy Trampoline service account, you need
to add `TRAMPOLINE_USE_LEGACY_SERVICE_ACCOUNT` to the environment
allow list in the Kokoro job config as follows:

```
# Use the legacy Trampoline service account in the bucket.
allowed_env_vars: {
  key: "TRAMPOLINE_USE_LEGACY_SERVICE_ACCOUNT"
  value: "(true|false)"
}
```

### Allow TRAMPOLINE_BUILD_FILE for V1 and V2

With Trampoline V1, `TRAMPOLINE_BUILD_FILE` is in the form of
`github/getting-started-python/.kokoro/.*`, but with Trampoline V2,
you can not have `github/getting-started-python` part.

So you may need to relax the regex if you have a strict one.

For example, this is the original configuration in our example repo:

```
# Allow configuring the trampoline build file.
allowed_env_vars: {
  key: "TRAMPOLINE_BUILD_FILE"
  value: "github/getting-started-python/.kokoro/.*"
}
```

We want to change it to allow both cases(so that the change is not
desruptive):

```# Allow configuring the trampoline build file.
allowed_env_vars: {
  key: "TRAMPOLINE_BUILD_FILE"
  value: "(github/getting-started-python/.kokoro/.*)|(.kokoro/.*)"
}
```

Here is the [actual change](http://cr320490275) for
the `getting-started-python` repo.

## Kokoro build config changes

Once you submit the Kokoro job configs, make a change in the Kokoro
build config files.

```
build_file: "getting-started-python/.kokoro/trampoline_v2.sh"

# Tell the trampoline which build file to use.
env_vars: {
    key: "TRAMPOLINE_BUILD_FILE"
    value: ".kokoro/system_tests.sh"
}

# We still rely on the legacy service account.
env_vars: {
    key: "TRAMPOLINE_USE_LEGACY_SERVICE_ACCOUNT"
    value: "true"
}
```

Now you can create a PR for migration.

Here is the [actual PR](https://github.com/GoogleCloudPlatform/getting-started-python/pull/271) for the `getting-started-python` repo.

## Appendix

### Difference between Trampoline V1 and V2

* Initial directory.
  With Trampoline V2, you're already in the project root. There is
  also an environment variable `PROJECT_ROOT`, whereas you need to do
  something like `cd github/repo-name` with Trampoline v1.

* Which environment variables are passed down into the container.
  Trampoline V1 passes down all the environment variables into the
  container. However, Trampoline V2 has an allowlist
  `pass_down_envvars`. You can modify this allowlist by having your
  own `.trampolinerc`.

* User id is different.
  Trampoline V1 runs the container as `root`. Trampoline V2 runs the
  container as a normal user.
