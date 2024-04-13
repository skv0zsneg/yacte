# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]

### Changed

- Program entry point.
- Entities (now models - Terminal, Symbols and Cursor).
- File manager (now file_reader).
- Display managers (now displayers).

### Added

- Tests for Terminal entity.
- Text file for manual tests.
- Module repository for hight level logic.

### Removed

- All old code.


## [0.0.1] - 2024.04.12

### Added

- Argparse for file path getting.
- Entities for file inputs and window displaying.
- Filemanager to read file.
- Visualize the file input on console with curse lib by display manager.
- Base handlers for keys up, down, left, right, backspace, etc.
- Test text files.
- Change log.
- License.