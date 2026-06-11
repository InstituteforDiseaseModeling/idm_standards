# wavetool

Utilities for analyzing damped harmonic oscillators.

## Installation

```bash
pip install wavetool
```

## Usage

```python
import wavetool as wt
t, x = wt.simulate(omega=2.0, zeta=0.1, x0=1.0, duration=10.0)
freq = wt.peak_frequency(t, x)
```

## Project structure

- `wavetool/` — the library (`core.py` holds the public API)
- `tests/` — pytest test suite

## Contributing

Pull requests welcome; please add a test for any change in behavior.
