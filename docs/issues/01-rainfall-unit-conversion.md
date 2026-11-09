# Issue #1 — Rainfall unit conversion error (Easy)
# Bug: Rainfall measured in cm is interpreted as mm

- **Difficulty:** Easy
- **Affected file:** `src/mazhai/data_loader.py` (`_to_mm`)
- **Relevant public test:** `tests/test_data_loader.py::test_cm_converted_to_mm`

## Problem description
Rows with `rainfall_unit=cm` (e.g. 2.5 cm = 25 mm) are read as 2.5 mm,
so genuine trigger events in cm-reporting gauges are missed.

## Expected behaviour
`convert(value, "cm") == value * 10`; mm passes through unchanged.

## Acceptance criteria
- [ ] cm rows convert at 10x.
- [ ] mm rows unchanged; explicit 0.0 still means dry.
- [ ] `test_cm_converted_to_mm` passes; other loader tests stay green.

## Reproduction steps
1. `pytest tests/test_data_loader.py::test_cm_converted_to_mm -v`
2. Observe 2.5 returned instead of 25.0.
