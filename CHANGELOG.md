# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0rc5] - 2025-06-04

### Added

- Include edges to imported modules' attributes when dependency analysis is disabled (https://github.com/nuanced-dev/jarviscg/pull/35)

### Fixed

### Changed

### Removed

## [0.1.0rc4] - 2025-05-01

### Added

### Fixed

### Changed

- Expose absolute instead of relative file paths in output (https://github.com/nuanced-dev/jarviscg/pull/32)

### Removed

## [0.1.0rc3] - 2025-04-25

### Added

### Fixed

- Ensure modules are analyzed in the same order as files, depth-first by directory/module, instead of in random order (https://github.com/nuanced-dev/jarviscg/pull/27)

### Changed

- Restore jarviscg's original handling of edges defined via aliases (https://github.com/nuanced-dev/jarviscg/pull/31)

### Removed

## [0.1.0rc2] - 2025-03-27

### Added

- `jarviscg.formats.Nuanced` call graph formatter exposes function start and end line numbers (https://github.com/nuanced-dev/jarviscg/pull/24)

### Fixed

### Changed

### Removed

## [0.1.0rc1] - 2025-03-04

### Added

- Include graph edges defined via module index (https://github.com/nuanced-dev/jarviscg/pull/18, https://github.com/nuanced-dev/jarviscg/pull/19)
- CallGraphGenerator orders entrypoints for depth-first traversal (https://github.com/nuanced-dev/jarviscg/pull/17)
- `jarviscg.formats.Nuanced` call graph formatter (https://github.com/nuanced-dev/jarviscg/pull/14)

### Fixed

- Update import statements for compatibility with Python 3.11 - 3.13 (https://github.com/nuanced-dev/jarviscg/pull/9)

### Changed

- Define jarviscg package (https://github.com/nuanced-dev/jarviscg/pull/12)

### Removed

- Don't print filenames while processing (https://github.com/nuanced-dev/jarviscg/pull/16)
