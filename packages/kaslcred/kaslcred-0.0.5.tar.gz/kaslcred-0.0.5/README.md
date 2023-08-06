# KASL : KERI and ACDC Schema Linker
Computes self addressing identifiers (SAIDs) for KERI and ACDC schema parts and links them together by SAID.

## Usage

``` shell
kasl [schema_dir] [output_dir] [schema_map_file.json]

# Example:
# Requires having pre-written and pre-copied all of the schema files into ${KASL_HOME}/schemas
export KASL_HOME=${HOME}/.kasl
kasl ${KASL_HOME}/schemas ${KASL_HOME}/results ${KASL_HOME}/schemas/schema_map.json
```

## Installation

### Dependencies
Rust toolchain (for Blake3 dependency)
Libsodium
KERI


## Development
Building

``` shell
python3 -m build

python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps kaslcred
```
