"""Tests for wavetool.core."""

import numpy as np
import pytest
import wavetool as wt


def test_simulate_decays():
    """A damped oscillator's envelope should decay over time."""
    t, x = wt.simulate(omega=2.0, zeta=0.2, x0=1.0, duration=20.0)
    assert abs(x[-1]) < 0.01 * abs(x[0])


def test_peak_frequency():
    """Recovered frequency should match the damped frequency."""
    omega, zeta = 2 * np.pi, 0.05
    t, x = wt.simulate(omega=omega, zeta=zeta, duration=50.0)
    expected = omega * np.sqrt(1 - zeta**2) / (2 * np.pi)
    assert wt.peak_frequency(t, x) == pytest.approx(expected, rel=0.05)


def test_damping_ratio_roundtrip():
    """Estimated damping ratio should match the simulated one."""
    zeta = 0.1
    _, x = wt.simulate(omega=2 * np.pi, zeta=zeta, duration=20.0)
    assert wt.damping_ratio(x) == pytest.approx(zeta, rel=0.1)


def test_invalid_zeta_raises():
    """Out-of-range damping ratios should raise a clear error."""
    with pytest.raises(ValueError):
        wt.simulate(zeta=1.5)


if __name__ == '__main__':
    pytest.main(['-x', '-v', __file__])
