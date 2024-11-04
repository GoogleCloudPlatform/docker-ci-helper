# Changelog

## [2.1.1](https://github.com/GoogleCloudPlatform/docker-ci-helper/compare/v2.1.0...v2.1.1) (2024-11-04)


### Bug Fixes

* add KOKORO_ARTIFACTS_DIR to the default list of env vars ([#58](https://github.com/GoogleCloudPlatform/docker-ci-helper/issues/58)) ([e68e88a](https://github.com/GoogleCloudPlatform/docker-ci-helper/commit/e68e88ae6980b60fdda724b398596dea805afd02))

## [2.1.0](https://github.com/GoogleCloudPlatform/docker-ci-helper/compare/v2.0.11...v2.1.0) (2024-11-04)


### Features

* allow skipping user/group override ([#55](https://github.com/GoogleCloudPlatform/docker-ci-helper/issues/55)) ([3de17dd](https://github.com/GoogleCloudPlatform/docker-ci-helper/commit/3de17ddbf47e596c34fc751669843c66b4f884dd))
* load additional .trampolinerc file next to trampoline_v2.sh file if present ([#57](https://github.com/GoogleCloudPlatform/docker-ci-helper/issues/57)) ([c9e4131](https://github.com/GoogleCloudPlatform/docker-ci-helper/commit/c9e4131267db44181330c0a02320bd9da2f6369e))

## [2.0.11](https://github.com/GoogleCloudPlatform/docker-ci-helper/compare/v2.0.10...v2.0.11) (2024-08-22)


### Bug Fixes

* update main script with lint fixes ([#50](https://github.com/GoogleCloudPlatform/docker-ci-helper/issues/50)) ([1497d14](https://github.com/GoogleCloudPlatform/docker-ci-helper/commit/1497d148d9300a659eaab08bcf7f92183d6377ab))

* 2.0.0
  initial release

* 2.0.1
  support legacy service account [#22](https://github.com/GoogleCloudPlatform/docker-ci-helper/pull/22)

* 2.0.2
  flexible PROJECT_ROOT detection [#25](https://github.com/GoogleCloudPlatform/docker-ci-helper/pull/25)

* 2.0.3
  remove TRAMPOLINE_SKIP_DOWNLOAD_IMAGE envvar [#27](https://github.com/GoogleCloudPlatform/docker-ci-helper/pull/27)

* 2.0.4
  support relative path for TRAMPOLINE_SERVICE_ACCOUNT envvar [#29](https://github.com/GoogleCloudPlatform/docker-ci-helper/pull/29)

* 2.0.5
  support legacy style TRAMPOLINE_BUILD_FILE [#30](https://github.com/GoogleCloudPlatform/docker-ci-helper/pull/30)

* 2.0.6
  fix the docker image detection logic [#35](https://github.com/GoogleCloudPlatform/docker-ci-helper/pull/35)

* 2.0.7
  add a comment about the github repo [#38](https://github.com/GoogleCloudPlatform/docker-ci-helper/pull/38)

* 2.0.8
  add `KOKORO_BUILD_ARTIFACTS_SUBDIR` [#42](https://github.com/GoogleCloudPlatform/docker-ci-helper/pull/42)

* 2.0.9
  Comment update for Flaky Bot [#43](https://github.com/GoogleCloudPlatform/docker-ci-helper/pull/43)

* 2.0.10
  Correct verion string [#44](https://github.com/GoogleCloudPlatform/docker-ci-helper/pull/44)
