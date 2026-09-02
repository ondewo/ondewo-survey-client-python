# Release History

*****************

## Release ONDEWO Survey Python Client 2.0.2

### Bug Fixes

* [[OND221-2830]](https://ondewo.atlassian.net/browse/OND221-2830) Regenerated with [ondewo-proto-compiler 5.13.0](https://github.com/ondewo/ondewo-proto-compiler/releases/tag/5.13.0).
* [[OND221-2830]](https://ondewo.atlassian.net/browse/OND221-2830) Tooling: `conventional-pre-commit` now runs before `giticket` at the commit-msg stage - with giticket first, its `[OND221-2830] fix: ...` rewrite was no longer valid Conventional Commits and every commit on a ticket branch failed. `README.md` is prettier-ignored where `.prettierrc` sets `useTabs` and markdownlint's MD010 de-tabs the same blocks, and the codegen `docker run` invocations no longer pass `-it`, which fails outside a TTY.

*****************

## Release ONDEWO Survey Python Client 2.0.1

### Improvements

* Added functionality to pass grpc options to grpc clients based on [ONDEWO CLIENT UTILS PYTHON 2.0.0](https://github.com/ondewo/ondewo-client-utils-python/releases/tag/2.0.0)

*****************

## Release ONDEWO Survey Python Client 2.0.0

### Improvements

* Tracking API Version [2.0.0](https://github.com/ondewo/ondewo-survey-api/releases/tag/2.0.0) ( [Documentation](https://ondewo.github.io/ondewo-survey-api/) )

*****************

## Release ONDEWO Survey Python Client 1.1.0

### Improvements

* [[OND211-2039]](https://ondewo.atlassian.net/browse/OND211-2039) - Added pre-commit hooks and adjusted files to them
* Updated API to 1.1.0

*****************

## Release ONDEWO Survey Python Client 1.0.1

### Bug fixes

* Relaxed requirements to ondewo-client-utils>=0.1.0

*****************

## Release ONDEWO Survey Python Client 1.0.0

### New Features

* [[OND211-2039]](https://ondewo.atlassian.net/browse/OND211-2039) - Automated Release Process

*****************

## Release ONDEWO Survey Python Client 0.6.0

### New Features

* Extension of the API to support the FHIR format

*****************

## Release ONDEWO Survey Python Client 0.5.1

### Bug Fixes

* Addition of a missing init file that prevented the installation through PyPi

*****************

## Release ONDEWO Survey Python Client 0.5.0

### New Features

* Adapted to support the Survey API 0.5.0

*****************

## Release ONDEWO Survey Python Client 0.4.0

### Bug Fixes

* Correct release version from 0.1.0 to 0.4.0

### New Features

* [[OND212-33]](https://ondewo.atlassian.net/browse/OND212-33) - Initialise repository for the Survey Server Python client
