# AGENTS.md

## Project Overview

`netengine` is the Python library that provides a common interface for
collecting network-device information, including SNMP-backed AirOS and OpenWRT
monitoring data.

Core code lives in `netengine/`:

- `backends/` implements backend-specific data collection and serialization.
- `backends/snmp/` contains the shared SNMP layer and device backends.
- `backends/schema.py` defines the NetJSON DeviceMonitoring schema used in tests.
- Tests and SNMP fixtures live in `tests/`.

## Source of Truth

- Use `README.rst` and `docs/` for setup, package usage, and baseline commands.
- Use `.github/workflows/ci.yml` for CI-tested dependencies, QA commands, and
  supported Python versions.
- Use GitHub issue and pull request templates when asked to open issues or PRs.

If instructions conflict, repository configuration and CI workflows win first,
official documentation next, and this file is supplemental.

## Development Notes

- Keep changes focused. Avoid unrelated refactors and formatting churn.
- Preserve public APIs, NetJSON output formats, schema validation, SNMP dump
  behavior, and backend compatibility unless explicitly required.
- Place imports at the top of the file. Defer imports only when necessary.
- Avoid unnecessary blank lines inside function and method bodies.
- Keep test method names concise. Add a docstring when the short name does not
  explain the behavior being tested.
- Update docs when behavior, public APIs, setup steps, or supported versions change.

## Testing and QA

- Add or update tests for every behavior change.
- For bug fixes, write a regression test first, run it against the unfixed code,
  and confirm it fails for the expected reason before implementing the fix.
- Use targeted tests while iterating. Run `./runtests.py` before considering a
  change complete.
- This repository has no Selenium tests. Do not set Selenium environment variables.
- Run `openwisp-qa-format` after editing when available.
- Run `./run-qa-checks` when present. Treat failures as blocking unless confirmed
  unrelated and reported.
- Prefer in-process tests so coverage tools can measure changed code.

## Security Notes

- Watch for malformed NetJSON output, unsafe host or port handling, invalid OIDs,
  SNMP dump inconsistencies, and secrets in device configuration.
- Preserve validation around device monitoring output, interface data, resource
  metrics, and vendor-specific SNMP values.
- Write comments and docstrings only when they explain why code is shaped a
  particular way. Put comments before the relevant code block.

## Troubleshooting

- If setup, QA, or tests fail, check docs first, then compare with CI. If commands
  diverge, follow CI.
