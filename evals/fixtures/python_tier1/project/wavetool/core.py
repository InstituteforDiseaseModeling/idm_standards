"""Core routines for simulating and analyzing damped harmonic oscillators."""

import numpy as np


def simulate(omega=1.0, zeta=0.05, x0=1.0, duration=10.0, dt=0.001):
    """ Simulate a damped harmonic oscillator.

    Args:
        omega (float): Undamped angular frequency (rad/s).
        zeta (float): Damping ratio (dimensionless, 0 <= zeta < 1).
        x0 (float): Initial displacement.
        duration (float): Total simulated time (s).
        dt (float): Time step (s).

    Returns:
        tuple: Arrays (t, x) of time points and displacements.

    **Example**:

        t, x = simulate(omega=2.0, zeta=0.1)
    """
    if not 0 <= zeta < 1:
        raise ValueError(f'zeta must be in [0, 1) for an underdamped oscillator, not {zeta}')
    t = np.arange(0, duration, dt)
    omega_d = omega * np.sqrt(1 - zeta**2)
    x = x0 * np.exp(-zeta * omega * t) * np.cos(omega_d * t)
    return t, x


def peak_frequency(t, x):
    """ Estimate the dominant frequency of a signal via FFT.

    Args:
        t (array): Time points (must be evenly spaced).
        x (array): Signal values.

    Returns:
        float: Dominant frequency in Hz.

    **Example**:

        freq = peak_frequency(t, x)
    """
    dt = t[1] - t[0]
    spectrum = np.abs(np.fft.rfft(x))
    freqs = np.fft.rfftfreq(len(x), dt)
    return freqs[np.argmax(spectrum[1:]) + 1]  # skip the DC component


def damping_ratio(x):
    """ Estimate the damping ratio from successive peaks (logarithmic decrement).

    Args:
        x (array): Displacement signal of an underdamped oscillator.

    Returns:
        float: Estimated damping ratio.

    **Example**:

        zeta = damping_ratio(x)
    """
    peaks = []
    for i in range(1, len(x) - 1):
        if x[i] > x[i - 1] and x[i] > x[i + 1] and x[i] > 0:
            peaks.append(x[i])
    if len(peaks) < 2:
        raise ValueError('Need at least two positive peaks to estimate damping')
    delta = np.log(peaks[0] / peaks[1])
    return delta / np.sqrt(4 * np.pi**2 + delta**2)
