# IDM testing style guide

It's very dull to write a test for a completed feature that you know will pass. So use test-driven development (TDD) instead: before you write the feature, start with the test and use it to brainstorm the feature's API. Then you can trick yourself that you're doing cool design architecture instead of writing a boring test. We're not militant about using TDD, but it really, truly is a good idea.

IDM uses `pytest` for its test suite, run in parallel via `pytest-xdist`. (Do not use `unittest` -- we have not found it to be particularly useful!) Tests live in the `tests/` folder and follow a consistent set of conventions described below. The overriding principle is: **tests should be runnable both by pytest and as standalone scripts**, so that developers can interactively explore and debug results. All tests should be run on GitHub Actions for every pull request, and PRs should only be merged if all tests pass.


## Philosophy

Before getting into the mechanics, here are the core principles that should guide how you write tests for IDM projects.

### Tests are examples

A test is often the first piece of working code that a new contributor (or user) will read. Write your tests as if they are **examples of how to interact with the models**. They should expose preferred pathways and APIs -- someone reading `test_sir()` should come away understanding the recommended way to set up and run an SIR simulation.

### Write for humans

While you definitely _should_ include `assert` statements in your tests, you should also include human-digestible output: summary results printed to the terminal, plots, or both. This is so the person running the test can notice things that would be impossible to write an `assert` statement for (e.g. "Huh, I don't remember the infections peak looking like that").


### Tests, not analyses

Sometimes a test can spin out into a full-blown analysis. If you want to test the end-to-end workflow of running an entire health-budget resource optimization for a country -- loading multiple data files, configuring models, post-processing outputs -- that belongs in a **separate analysis repo**. The tests in the main repo should be **minimal reproducible examples**: the smallest amount of code that exercises the feature and confirms it works.

### Modular and minimal

Each test should do one thing and do it clearly. If a test function is growing beyond ~30 lines, ask whether it's really testing one thing or several. Break it up. Keep setup code in helper functions so the test body itself reads like a recipe.

### Scientific correctness over mechanical coverage

It is always more relevant to focus on testing the **scientific validity of the outputs** than to write thousands of lines of tests that do things like change a dict entry and then assert the dict entry changed. Good tests confirm that the model *behaves as expected epidemiologically*: higher beta means higher prevalence; a vaccine reduces infections; treatment shortens duration of infection. These are the tests that catch real bugs.

### Keep it simple

Typically it is more than sufficient to run a test, assert something meaningful, and then either raise an error or print a success statement. If in doubt, less is better than more!


## File structure

Test files typically follow this skeleton:

```python
"""
Test <topic>
"""
import sciris as sc
import numpy as np
import starsim as ss
import matplotlib.pyplot as plt
import pytest

n_agents = 1_000
do_plot = False
sc.options(interactive=False) # Assume not running interactively


def make_sim():
    """ Helper to create a default sim for this test file """
    ...
    return sim


@sc.timer()
def test_feature(do_plot=do_plot):
    """ One-line description of what this test checks """
    sc.heading('Testing feature...')
    sim = make_sim()
    sim.run()
    something = sim.results.something

    # Print a meaningful summary of the test (optional, encouraged)
    print(f'Results summary:  {something.mean()}') 

     # Make an assertion about expected behavior -- the most important part
    assert something.max() > 0, f'Expected something to be positive, but {something.max()} <= 0'

    # Include a plot (optional, encouraged), but always have an option to turn it off
    if do_plot: 
        sim.plot()

    return sim


if __name__ == '__main__':
    do_plot = True
    sc.options(interactive=do_plot)
    T = sc.timer()

    sim = test_feature(do_plot=do_plot)

    T.toc()

    if do_plot:
        plt.show()
```

An example of a complete test:

```python
@sc.timer()
def test_simple_vax(do_plot=do_plot):
    """ Create and run a sim with vaccination """
    sc.heading('Testing simple vaccination...')
    pars = make_sim_pars()

    sim_base = ss.Sim(pars=pars).run()
    sim_intv = ss.Sim(pars=pars, interventions=intv).run()
    inf_base = sim_base.summary.sir_cum_infections
    inf_intv = sim_intv.summary.sir_cum_infections

    print(f'Infections without vaccine: {inf_base}')
    print(f'Infections with vaccine {inf_intv}')
    assert inf_intv < inf_base, 'Vaccine should avert infections'

    if do_plot:
        plt.figure()
        plt.plot(sim_base.timevec, sim_base.results.sir.prevalence, label='Baseline')
        plt.plot(sim_intv.timevec, sim_intv.results.sir.prevalence, label='Vax')
        plt.legend()

    return sim_base, sim_intv
```

Key elements, in order:

1. **Module docstring** -- a brief description of what the file tests.
2. **`sc.options(interactive=False)`** -- can set at module level so pytest doesn't open plot windows, to avoid the need for lots of `plot=False` arguments.
3. **Helper functions** (e.g. `make_sim()`, `make_sim_pars()`) -- shared setup logic used by multiple tests.
4. **Test functions** -- each decorated with `@sc.timer()` (showing how long it took) and named `test_*`.
5. **`if __name__ == '__main__':`** block -- enables standalone script execution with plotting.


## Module-level constants

Define constants at the top of the file so they can be easily tuned:

```python
n_agents = 1_000
do_plot = False
sc.options(interactive=False)
```

Use underscore separators for large numbers (`1_000`, `10_000`). Some files use named size tiers for clarity:

```python
small  = 100
medium = 1000
```

Use the smallest agent count that still produces meaningful test results. Integration tests (`test_baselines.py`) use larger populations (e.g. `10e3`); unit-level tests use `100`--`1000`.


## Test functions

### Naming

Name test functions `test_<feature>`, where `<feature>` is **lowercase** and **succinct**:

```python
def test_sir():         # Yes: short, clear
def test_immunity():    # Yes: names the concept being tested
def test_parallel():    # Yes: describes the capability
def test_sir_epi():     # Yes: a refinement within a file that has multiple SIR tests

def TestImmunityDynamicsWanesOverTime():  # No: not a test name, it's a novel title
def test_sir_model():                     # No: "model" adds nothing
def test_api():                           # No: too vague on its own
```

### Grouping

Group tests into files by topic. A test of SIR model dynamics goes in `test_diseases.py`; a test of network formation goes in `test_networks.py`; a test of calibration goes in `test_calibration.py`. Follow the naming convention `test_<topic>.py` for files:

```
tests/
    test_sim.py          # Core sim creation and running
    test_diseases.py     # Disease module dynamics
    test_networks.py     # Network formation and connectivity
    test_demographics.py # Birth, death, migration
    test_interventions.py # Vaccines, treatments, etc.
    test_calibration.py  # Calibration workflows
```

If a test is more of an exploratory dev test or a detailed investigation, it belongs in a `devtests/` subfolder rather than the main `tests/` directory. The main test suite should be the set of tests that run in CI and that every contributor is expected to keep passing.

### Decorators

Test functions are typically decorated with `@sc.timer()`:

```python
@sc.timer()
def test_demo(do_plot=do_plot):
    ...
```

This prints timing information, which is useful for catching performance regressions. Use `pytest.mark.skip(reason="...")` for tests that are temporarily disabled.

### Returns

Tests typically return "the most interesting" object they generate. If a sim is run, then typically they would return the sim. This allows the test file to be run as a script and the results inspected without needing to set breakpoints and use the debugger.

### Assertions

Always include a descriptive message in assertions. The message should say what was *expected*, not just what happened:

```python
# Yes
assert v0 <= v1, f'Expected prevalence to be lower with {par}={lo} than {par}={hi}, but {v0} > {v1}'
assert len(log) > 900, 'Expect almost everyone to be infected'

# No: no message
assert v0 <= v1
assert sim.results.n_alive[0] > 0
```

For float comparisons, use `np.isclose` or `np.allclose` with explicit tolerances:

```python
assert np.isclose(data.n_alive.values[-1], sim.results.n_alive[-1], rtol=0.05), 'Final pop not within 5% of data'
assert np.allclose(s1.summary[:], s2.summary[:], rtol=0, atol=0, equal_nan=True), "Sims don't match"
```

For testing expected exceptions, use `pytest.raises`:

```python
with pytest.raises(TypeError):
    sim = ss.Sim(diseases=True) # invalid type for diseases
    sim.init() # caught here
```

### Testing scientific correctness

Many IDM tests check that epi dynamics go in the expected direction. The key pattern is: vary one parameter and confirm the result changes as expected:

```python
par_effects = dict(
    beta     = [0.01, 0.99],
    dur_inf  = [1, 8],
    p_death  = [0.01, 0.1],
)

for par, par_val in par_effects.items():
    s0 = ss.Sim(pars0).run()
    s1 = ss.Sim(pars1).run()
    assert v0 <= v1, f'Expected higher {par} to increase prevalence'
```

Use generous tolerances (`rtol=0.05` or more) for stochastic comparisons to avoid flaky tests. Comment the tolerance choice:

```python
rtol = 0.2  # Generous to avoid random failures with small populations
```

## Test coverage

Test coverage should be checked periodically (e.g., after a major release), typically by a `check_coverage` script. We don't aim for 100% test coverage, but anything below 80% starts to get concerning. If a block of code is hard to cover in tests, ask yourself: do we really need to keep it?


## What NOT to test

Having more tests is not always better: they can be confusing, create technical debt, and slow down development. Here is guidance on what to avoid:

- **Mechanical getter/setter tests**: Don't write tests that just set a parameter and assert it was set. If `sim.pars.beta = 0.5` followed by `assert sim.pars.beta == 0.5` is your test, it's testing Python, not your model.
- **Exhaustive input permutations**: Don't test every possible combination of inputs. Test the important ones -- defaults, edge cases, and the cases your users will actually hit.
- **End-to-end country analyses**: If a test requires loading country-specific data files, configuring multiple diseases, running calibration, and post-processing results, it's an analysis, not a test. Move it to a separate repo.
- **Tests that require explanation**: If you need a paragraph of comments to explain what a test is doing, the test is too complex. Simplify it.


## Triple-mode execution

The most distinctive IDM testing convention is that every test file is designed to run as a GitHub action, as a pytest module, *and* as a standalone script.

### GitHub Actions mode

Always include a `.github/workflows/tests.yaml` file that runs the tests. The tests run on GitHub Actions should exactly match what's run locally by pytest.

### pytest mode

When run via pytest (`pytest test_*.py -n auto`), tests execute with `do_plot=False` and `sc.options(interactive=False)`. Functions are discovered by name (`test_*`). Plots are suppressed. For more complex projects, write a `run_tests` script to automatically run the tests in parallel (otherwise, just calling `pytest` is fine).

### Script mode

When run directly (`python test_sim.py`), the `__main__` block sets `do_plot=True`, runs all tests, and shows plots. This is important for catching things that might pass the assert statements, but look scientifically wrong.


## Plotting in tests

Plotting should always be conditional, unless the plot itself is being tested:

```python
@sc.timer()
def test_feature(do_plot=do_plot):
    ...
    if do_plot:
        sim.plot()
    return sim
```

Use `plt.figure()` before any manual plotting to avoid accidentally drawing on a previous test's figure. Always ensure `sc.options(interactive=False)` is set at the top of the file to prevent plot windows in CI.

The `SCIRIS_BACKEND=agg` environment variable is set in the test runner scripts (`run_tests`, `check_coverage`) to ensure no display backend is needed.


## Test infrastructure

### Running tests

- **`tests/run_tests`** -- runs all `test_*.py` files in parallel with timing.
- **`tests/check_coverage`** -- runs tests with coverage reporting and generates an HTML report.
- **`tests/check_style`** -- runs `pylint` on the main `starsim` package.

### Configuration files

- **`tests/pytest.ini`** -- typically required; silences unnecessary pytest warnings.
- **`tests/.coveragerc`** -- optional; used to fine-tune coverage reports.
. **`./.pylintrc`** -- implements the [IDM Python style guide](2_python.md) to silence unnecessary linting warnings.


## Parting words

Good tests should:

- **Be scientific**: test that the model behaves as epidemiologically expected, not just that code runs without errors.
- **Be examples**: a new user reading and running your test should learn the recommended way to use the API and what it does.
- **Be debuggable**: return objects, support plotting, and print informative output so failures can be investigated interactively.
- **Be stable**: use tolerances appropriate for stochastic models; a test that fails 1% of the time due to randomness is worse than no test.
- **Be fast**: use the smallest agent count that produces meaningful results; save large-scale tests for benchmarks.
- **Be minimal**: test one thing per function; keep the main test suite lean and move exploratory work to `devtests/`.