## jarviscg

Nuanced's fork of the [pythonJaRvis](https://github.com/pythonJaRvis/pythonJaRvis.github.io) Python call graph generator.

Note: The benchmarking and evaluation scripts in the `evaluation` directory have not been updated to run on this fork.

Prerequisites:

* Python >= 3.8
* uv

## Usage

jarviscg command-line usage:

```bash
% uv tool install git+https://github.com/nuanced-dev/jarviscg
% jarviscg -h
usage: jarviscg [-h] [--package PACKAGE] [--decy] [--precision] [--entry_point [ENTRY_POINT ...]] [-o OUTPUT] [module ...]

positional arguments:
  module                Modules to be processed

options:
  -h, --help            show this help message and exit
  --package PACKAGE     Package containing the code to be analyzed
  --decy                whether iterate the dependency
  --precision           whether flow-sensitive
  --entry_point [ENTRY_POINT ...]
                        Entry Points to be processed
  -o OUTPUT, --output OUTPUT
                        Output path
```

## Setup

```bash
% cd jarviscg
% uv venv
% source .venv/bin/activate
% uv sync
```

## Running pytest tests

```bash
% source .venv/bin/activate
% pytest tests/
```
