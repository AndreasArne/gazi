# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Available types:

- `Added` for new features.
- `Changed` for changes in existing functionality.
- `Deprecated` for soon-to-be removed features.
- `Removed` for now removed features.
- `Fixed` for any bug fixes.
- `Security` in case of vulnerabilities.

## [Unreleased]

## [1.0.1] - 2023-03-17
### Fixed
- Now uses parsers to remove non allowed chars from students code.

## [1.0.0] - 2023-03-14
### Changed
- From CodeGrade jplag to JPlag jplag v4.2.0
- Only deletes specific kmom dir in submissions, not all.
### Added
- JPlag's report-viewer in Docker to view result
- Option to create courses directory structure.
### Removed
- StarskyAndHutch - JPlags version is better


## [0.2.0] - 2022-11-04
### Added
- Supports wildcard in moss file for files to copy (with `*`).
- When copying with wildcard, can exclude files (with `!`).


### Fixed
- Gazi looked for `.jplag.cfg` instead of `jplag.cfg`.

## [0.1.0] - 2021-10-12
### Added
- starskyandhutch running from gazi.
- starskyandhutch is included in docker image



## [0.0.1] - 2021-03-19
### Added
- Initial release

