# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.4] - 2021-03-30
### Fixed
- Bug with `/healthz` endpoint
- Bug related to custom "actions" folder locations

## [1.0.0] - 2021-03-17
- Move to version 1.0.0
### Added
- Added graceful shutdown to play nicely with Kubernetes and other container managers
- Added automatic `/healthz` endpoint

## [0.1.5] - 2020-08-06
### Changed
- Improved Pantam logger to make it work better with other loggers (e.g. uvicorn)

## [0.1.4] - 2020-08-06
### Fixed
- Bug in Pantam logger

## [0.1.3] - 2020-08-06
### Changed
- Make use of built in logging module via Pantam logger

## [0.1.2] - 2020-08-05
### Changed
- Replaced PyInquirer in favour of prompt_toolkit

## [0.1.1] - 2020-08-04
### Changed
- Included standard Starlette response in Pantam responses

## [0.1.0] - 2020-08-04
### Added
- New custom method "do"

## [0.0.1] - 2020-08-03
- Launched first version of Pantam
