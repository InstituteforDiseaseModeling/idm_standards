# Python style guide

In general, IDM models follow Google's [style guide](https://google.github.io/styleguide/pyguide.html). If you simply follow that, you can't go too wrong. However, there are a few "house style" differences, which are described here.

**Note**: Although the examples given here refer to Covasim and mainly use Covasim examples, they apply to all IDM models.

IDM uses `pylint` to ensure style conventions. To check if your styles are compliant, run `./tests/check_style`.


## Google style guide summary

While we encourage you to read the whole Google style guide, here's the quick version (skipping points that are covered in more detail below):

- Avoid global state variables.
- Nested functions, list comprehensions, and lambda functions are fine, but use them sparingly.
- List comprehensions are also fine, but also use sparingly.
- Use implicit true/false where possible (e.g. `if n_tests` not `if n_tests > 0`); but always check for `None` explicitly (e.g. `if n_tests is None: n_tests = 0`, not `if not n_tests: n_tests = 0`).
- Use parentheses sparingly.
- Indent using 4 spaces.
- Do not use unnecessary whitespace.
- Docstrings:
  - Use module-level docstrings (a `"""` block at the very top of each Python file) that describes what this file does; it should not be more than a paragraph or two.
  - There should be a docstring for each function, class, and method (we'll just refer to these as "functions" for simplicity)
  - Short, obvious, and/or utility functions, e.g. `__len__` almost never needs a docstring; Google's exact advice is "Use docstrings for every function that is part of the public API, has nontrivial size, or non-obvious logic".
  - Docstrings should start with a one-line explanation of what the function does. Then, if needed, a longer explanation.
  - If the function takes arguments, these should be listed under "Args:", including types and defaults.
  - If the function outputs something important, you can optionally include a "Returns:" section.
  - If the function is an important user API, include at least one example under "**Examples**:".
- Do not use getters and setters unless necessary (if you don't know what this means, you're probably safe!).
- Prefer small and focused functions.
- Be consistent!


## House style

As noted above, IDM follows Google's style guide (GSG), **with these exceptions** (numbers refer to Google's style guide):

### 2.8 Default Iterators and Operators ([GSG28](https://google.github.io/styleguide/pyguide.html#28-default-iterators-and-operators))

**Difference**: It's fine to use `for key in obj.keys(): ...` instead of `for key in obj: ...`.

**Reason**: In larger functions with complex data types, it's not immediately obvious what type an object is. While `for key in obj: ...` is fine, especially if it's clear that `obj` is a dict, `for key in obj.keys(): ...` is also acceptable if it improves clarity.

### 2.12 Default Argument Values ([GSG212](https://google.github.io/styleguide/pyguide.html#212-default-argument-values))

**Difference**: Use keyword arguments with default values wherever possible.

**Reason**: The perfect function is one that does exactly what you want with no customization. For example, Matplotlib's `plt.figure()` opens up a figure. There are lots of things you could be asked to specify -- the background color, the backend to use, the figure size, etc -- but it just guesses these things (and most of the time, it's guesses are right or close enough). Keyword arguments with default values provide the most robust and user-friendly API, especially when a function has more than a couple arguments. Even with a small number of arguments, keyword arguments prevent silly mistakes like:

```python
def apply_interventions(self, screen_prob=0.0, treat_prob=0.0, vax_prob=0.0):
    self.apply_screening(screen_prob)
    self.apply_treatment(treat_prob)
    self.apply_vaccination(vax_prob)
```

In downstream code, if you see this:

```python
sim.apply_interventions(0.6, 0.4, 0.0)
```

that doesn't tell you much, and it's obviously extremely easy to misremember the order of the values (vaccination should be first, right?). Contrast that with:

```python
sim.apply_interventions(screen_prob=0.6, treat_prob=0.4)
```

### 2.20 Modern Python: from `__future__` imports ([GSG220](https://google.github.io/styleguide/pyguide.html#220-modern-python-from-__future__-imports))

**Difference**: Never use.

**Reason**: Nothing has been added to `__future__` since Python 3.7 (in 2018). We simply don't support Python versions that old.

### 2.21 Type Annotated Code ([GSG221](https://google.github.io/styleguide/pyguide.html#221-type-annotated-code))

**Difference**: Do *not* use type annotations (a.k.a. type hints) unless you have a good reason to.

**Reason**: Type hints are useful for ensuring that simple functions do exactly what they're supposed to as part of a complex whole. They prioritize consistency over convenience, which is the correct priority for low-level library functions, but not for functions and classes that aim to make it as easy as possible for the user.

For example, in Starsim, dates can be specified as strings (`'2024-04-04'`), date objects (`datetime.date(2024, 4, 4)`), or custom `date` objects (`ss.date('2024.04.04')`). Likewise, many quantities can be specified as a scalar, list, or array. If a function *usually* only needs a single input but can optionally operate on more than one, it adds burden on the user to require them to provide e.g. `np.array([0.3])` rather than just `0.3`. In addition, most functions have default arguments of `None`, in which case Starsim will use "sensible" defaults.

Attempting to apply type annotations to the flexibility Starsim gives to the user would result in monstrosities like:

```python
def count_days(self, start_day: typing.Union[None, str, ss.date, dt.date, dt.datetime],
               end_day: typing.Union[None, str, ss.date, dt.date, dt.datetime]) -> int:
    return self.day(end_day) - self.day(start_day)
```

If your function is written in such a way that type definitions would be helpful, consider if there is a way to rewrite it such that (a) it can accept a wider range of inputs, and/or (b) you can make it clearer what is allowed. For example, a variable called `values` should likely accept a list or array of any numeric type; a variable called `label` should be a single string; `labels` should be a list of strings.

Note that you *can* (and should) use type annotations in your docstrings. For example, the above method could be written as:

```python
def count_days(self, start_day, end_day):
    """ Count days between start and end relative to "sim time"

    Args:
        start_day (str/date): The day to start counting
        end_day   (str/date): The day to stop counting

    Returns:
        elapsed (int): Number of whole days between start and end

    **Example**::

        sim.count_days(45, '2022-02-02')
    """
    return self.day(end_day) - self.day(start_day)
```

See the "Naming" section below for another example of why type hints are not usually used.

#### Exceptions

If you're writing code like `count_days`, or standard Starsim modules (e.g. interventions), you shouldn't need type hints. However, there are many cases where type hints are very useful. If you are passing large numbers of simple objects between functions, type annotations tend not to help much (as in the examples above). However, if you're passing a small number of complex objects between functions, they can be very helpful, especially for code introspection. For example, if you're working with AI agents and you're passing in a `RequestContext` and expecting a `ResultMessage` back, type hints can be very helpful in specifying that the API must be _exactly_ this.

### 3.2 Line length ([GSG32](https://google.github.io/styleguide/pyguide.html#32-line-length))

**Difference**: Long lines are not *great*, but are justified in some circumstances.

**Reason**: Line lengths of 80 characters are due to [historical limitations](https://en.wikipedia.org/wiki/Characters_per_line). Think of lines >80 characters as bad, but breaking a line as being equally bad. Decide whether a long line would be better implemented some other way -- for example, rather than breaking a >80 character list comprehension over multiple lines, use a `for` loop instead. Always keep literal strings together (do not use implicit string concatenation).

Line comments are encouraged at IDM, and these can be as long as needed; they should not be broken over multiple lines to avoid breaking the flow of the code. A 50-character line with a 150 character line comment after it is completely fine. The rationale is that long line comments only need to be read very occasionally; if they are broken up over multiple lines, then they have to be scrolled past *every single time*. Since scrolling vertically is such a common task, it is important to minimize the amount of effort required (i.e., minimizing lines) while not sacrificing clarity. Vertically compact code also means more will fit on your screen (and thence your brain).

Examples:

```python
# Yes: it's a bit longer than 80 chars but not too bad
foo_bar(self, width, height, color='black', design=None, x='foo', emphasis=None)

# No: the cost of breaking the line is too high
foo_bar(self, width, height, color='black', design=None, x='foo',
        emphasis=None)

# No: line is needlessly long, rename variables to be more concise to avoid the need to break
foo_bar(self, object_width, object_height, text_color='black', text_design=None, x='foo', text_emphasis=None)

# No: line is too long
foo_bar(self, width, height, design=None, x='foo', emphasis=None, fg_color='black', bg_color='white', frame_color='orange')

# Yes: if you do need to break a line, try to break at a semantically meaningful point
foo_bar(self, width, height, design=None, x='foo', emphasis=None,
        fg_color='black', bg_color='white', frame_color='orange')

# Yes: long line comments are ok
foo_bar(self, width, height, color='black', design=None, x='foo') # Note the difference with bar_foo(), which does not perform the opposite operation
```

### 3.5 Blank Lines ([GSG35](https://google.github.io/styleguide/pyguide.html#35-blank-lines))

**Difference**: You *may* use one extra blank line between levels as within a level.

**Reason**: Google's recommendation (two blank lines between functions or classes, one blank line between methods) is appropriate for small-to-medium classes and methods. However, for large methods (e.g. >50 lines) with multiple blank lines within them, using only a single blank line can make it hard to tell where one method stops and the next one starts. THus, in cases where a class consists mostly of large methods that contains blank lines within themselves, you can use *two* blank lines between methods (and then do that consistently for the rest of the class). However, err on the side of using a single line between methods (and maybe try to refactor your overly-long methods into smaller, more modular ones).

While not explicitly covered by the Google style guide, `return` statements should be used at the end of each function and method, even if that block returns `None` (in which case use `return`, not `return None`). This helps delimit larger methods/functions. However, always ask whether a function/method *should* return `None`. Following the pandas convention, many Starsim methods return `self`, which is what enables "chaining" patterns such as `ss.Sim().run().plot()`.

### 3.6 Whitespace ([GSG36](https://google.github.io/styleguide/pyguide.html#36-whitespace))

**Difference**: You *may* use spaces to vertically align tokens when the content is semantically related, e.g. a list of parameter values.

**Reason**: This convention, which is a type of [semantic indenting](https://gist.github.com/androidfred/66873faf9f0b76f595b5e3ea3537a97c), can greatly increase readability of the code by drawing attention to the semantic similarities and differences between consecutive lines.

Consider how much harder it is to debug this code:

```python
# Perform updates
self.init_flows()
self.flows['new_infectious'] += self.check_infectious()
self.flows['new_symptomatic'] += self.check_symptomatic()
self.flows['new_severe'] += self.check_symptomatic()
self.flows['new_critical'] += self.check_critical()
self.flows['new_recoveries'] += self.check_recovery()
```

compared to this:

```python
# Perform updates
self.init_flows()
self.flows['new_infectious']  += self.check_infectious()
self.flows['new_symptomatic'] += self.check_symptomatic()
self.flows['new_severe']      += self.check_symptomatic()
self.flows['new_critical']    += self.check_critical()
self.flows['new_recoveries']  += self.check_recovery()
```

In the second case, the typo (repeated `check_symptomatic()`)  immediately jumps out, whereas in the first case, it requires careful scanning of each line.

Vertically aligned code blocks also make it easier to edit code using editors that allow multiline editing (e.g., [Sublime](https://www.sublimetext.com/)). However, use your judgement -- there are (many!) cases where it does more harm than good, especially if the block is small, or if egregious amounts of whitespace would need to be used to achieve alignment:

```python
# Yes -- makes it much easier to read
test_prob  = 0.1 # Per-day testing probability
vax_prob   = 0.3 # Per-campaign vaccination probability
trace_prob = 0.8 # Per-contact probability of being traced

# No -- needlessly hard to read
test_prob = 0.1 # Per-day testing probability
vax_prob = 0.3 # Per-campaign vaccination probability
trace_prob = 0.8 # Per-contact probability of being traced

# Yes -- two non-comparable variables, and of very different lengths
t = 0 # Start day
omicron_vax_prob = dict(low=0.05, high=0.1) # Per-day probability of receiving Omicron vaccine

# No -- impossible to read the first line
t                = 0                        # Start day
omicron_vax_prob = dict(low=0.05, high=0.1) # Per-day probability of receiving Omicron vaccine
```

### 3.8.5 Block and Inline Comments ([GSG385](https://google.github.io/styleguide/pyguide.html#385-block-and-inline-comments))

**Difference**: Use either one or two spaces between code and a line comment.

**Reason**: The advice "Use two spaces to improve readability" dates back to the era when most code was viewed as plain text. Now that virtually all editors have syntax highlighting, it's no longer really necessary. There's nothing *wrong* with two spaces, but if it's easier to type one space, do it.

### 3.10 Strings ([GSG310](https://google.github.io/styleguide/pyguide.html#310-strings))

**Difference**: Always use f-strings or addition.

**Reason**: It's just nicer. Compared to `'{}, {}'.format(first, second)` or `'%s, %s' % (first, second)`, the more modern `f'{first}, {second}'` is both shorter and clearer to read. However, use concatenation if it's simpler, e.g. `third = first + second` rather than `third = f'{first}{second}'` (because again, it's shorter and clearer).

### 3.13 Imports formatting ([GSG313](https://google.github.io/styleguide/pyguide.html#313-imports-formatting))

**Difference**: Imports should be ordered logically rather than alphabetically.

**Reason**: IDM modules shouldn't need a long list of imports. Sort imports as in Google's style guide (from most-generic to most-specific libraries), but second-order sorting should also be done logically, rather than alphabetically. For example:

```python
import os
import shutil
import numpy as np
import pandas as pd
import matpoltlib.pyplot as plt
import seaborn as sns
from .covasim import defaults as cvd
from .covasim import plotting as cvpl
```

Note the logical groupings -- standard library imports first, then numeric libraries, with NumPy coming before pandas since it's lower level (i.e., NumPy is a dependency of pandas); then external plotting libraries; and finally internal imports. (In this particular example, Google's import order would be identical, but for a different reason -- `numpy` would come before `seaborn` because it's first alphabetically, not because it's lower level.)

### 3.14 Statements ([GSG314](https://google.github.io/styleguide/pyguide.html#314-statements))

**Difference**: Multiline statements are *sometimes* OK.

**Reason**: Like with semantic indenting, sometimes it causes additional work to break up a simple block of logic vertically. However, use your judgement, and err on the side of Google's style guide. For example:

```python
# OK
if foo:
    bar(foo)

# Also OK
if foo: bar(foo)

# OK
if foo:
    bar(foo)
else:
    baz(foo)

# Also OK
if foo: bar(foo)
else:   baz(foo)

# Yes, but maybe rethink your life choices
if   foo == 0: bar(foo)
elif foo == 1: baz(foo)
elif foo == 2: bat(foo)
elif foo == 3: bam(foo)
elif foo == 4: bak(foo)
else:          zzz(foo)

# No: definitely rethink your life choices
if foo == 0:
    bar(foo)
elif foo == 1:
    baz(foo)
elif foo == 2:
    bat(foo)
elif foo == 3:
    bam(foo)
elif foo == 4:
    bak(foo)
else:
    zzz(foo)

# OK
try:
    bar(foo)
except:
    pass

# Also OK
try:    bar(foo)
except: pass

# No: too much whitespace and logic too hidden
try:               bar(foo)
except ValueError: baz(foo)
```

### 3.16 Naming ([GSG316](https://google.github.io/styleguide/pyguide.html#316-naming))

**Difference**: Names should be consistent with other libraries and with how the user interacts with the code.

**Reason**: IDM code interacts with other libraries, especially Numpy and Matplotlib, and should not redefine these libraries' names. For example, Google naming convention would prefer `fig_size` to `figsize`, but Matplotlib uses `figsize`, so this should also be the name preferred by IDM. (This applies if the variable name is *only* used by source libraries. If it's used by both, e.g. `start_day` used both directly by Covasim and by `sc.date()`, it's OK to use the Google style convention.)

If an object is technically a class but is used more like a function (e.g. `cv.change_beta()`), it should be named as if it were a function. A class is "used like a function" if the user is not expected to interact with it after creation, as is the case with most interventions. Thus `cv.BaseVaccinate` is a class that is intended to be used *as a class* (primarily for subclassing). `cv.vaccinate_prob()` is also a class, but intended to be used like a function; `cv.vaccinate()` is a function which returns an instance of `cv.vaccinate_prob` or `cv.vaccinate_num`. Because `cv.vaccinate()` and `cv.vaccinate_prob()` can be used interchangeably, they are named according to the same convention.

Names should be as short as they can be while being *memorable*. This is slightly less strict than being unambiguous. Think of it as: the meaning might not be clear solely from the variable name, but should be clear from the docstring and/or line comment, and from *that* point should be unambiguous. For example:

```python
# Yes
vax_prob = 0.3 # Per-campaign vaccination probability

# Also OK (but be consistent!)
vx_prob = 0.3 # Per-campaign vaccination probability

# No, too verbose; many more characters but not much more information
vaccination_probability = 0.3

# No, not enough information to figure out what this is
vp = 0.3
```

Underscores in variable names are generally preferred, but there are exceptions (e.g. `figsize` mentioned above). Always ask whether part of a multi-part name is providing necessary clarity (and if it's not, omit it). For example, if an intervention called `antigen_test()` uses a single variable for probability, call that variable `prob` rather than `test_prob`.

Why is it important to keep variable names short? Because it makes the code closer to math, which is how most IDM users think. Consider these two examples that both implement the same functionality:

```python
#%% Version 1 -- short, meaningful names
import numpy as np

def test_and_treat(uids, dx_prob=0.7, tx_prob=0.8, tx_eff=0.9):
    n = len(uids) # Number of agents
    rel_eff = np.zeros(n) # Relative efficacy (output)
    treated = (dx_prob > np.random.rand(n)) & (tx_prob > np.random.rand(n)) # Find who's treated
    rel_eff[treated] = tx_eff # Calculate per-agent treatment efficacy
    return rel_eff


#%% Version 2 -- long, very descriptive names -- find the three bugs!
import numpy as np
import numpy.typing as npt
import typing

def combined_testing_and_treatment_intervention(
        unique_agent_ids: typing.List[int] | npt.NDArray[np.int_],
        probability_of_diagnosis: float = 0.7,
        probability_of_treatment_following_diagnosis: float = 0.8,
        clinical_efficacy_of_treatment: float = 0.9
    )  -> npt.NDArray[np.int_]:
    number_of_agents = len(uids)
    per_agent_relative_efficacy_of_treatment = np.zeros(number_of_agents)
    agents_receiving treatment = \
        (probability_of_diagnosis > np.random.rand(number_of_agents)) & \
            (probability_of_treatment_following_diagnosis < \
             np.random.rand(number_of_agents))
    per_agent_relative_efficacy_of_treatment[agents_receiving_treatment] = clinical_efficacy_of_treatment
    return per_agent_relative_efficacy_of_treatment


#%% Test
uids = [1, 3, 5, 25, 58, 60, 78, 83, 92]
print(test_and_treat(uids))
print(combined_testing_and_treatment_intervention(uids))
```

Even for this quite simple example, the second one gets quite gnarly.


## Other conventions

This section covers additional topics not covered in the Google style guide.

### Managing Python dependencies

#### Package managers

We do not take a position on which Python package/environment manager you use. However:

- Your package should be installable with both `pip` and `uv`, if possible.
- You do not need to use an environment manager; however, if you do use one, we recommend `conda` or `uv`, not `venv`.
- In general, straightforward projects with simple dependencies should use `pip`, but more complex projects (e.g. AI workflows), or projects that need exact reproducibility on different environments (e.g., running across VMs), should use `uv`. Include a `uv.lock` file if it's helpful, but do not include one "just because".

#### Dependency pinning

Pinning dependencies (e.g. `numpy==1.23.0`) allows for exact reproducibility in the future. However, it also makes your code extremely brittle (if a single dependency of yours pins a shared dependency to a different version, there is a conflict).

Where possible, provide exact dependency _guidance_, not _requirements_. The dependencies in `pyproject.toml` should be as general as possible (e.g. `numpy`), with upward-pinned dependencies if and only if older versions really are guaranteed not to work (e.g. `pandas>=2.0.0`).

If you are building reusable library code where the functionality rather than the results matters (e.g., Starsim itself), this is usually enough. However, if your code produces numerical results where reproducibility matters (e.g., results for a publication), you _should_  provide pinned dependencies. In addition to the unpinned `pyproject.toml`, you have three options, from least to most strict:

- In `pyproject.toml`, under `[project.optional-dependencies]`, add a `lock` section with pinned dependencies based on the latest-tested version.
- You can export all the packages in your current environment with `pip freeze > requirements_locked.txt` (always include a suffix like "locked" or "frozen" to make it clear to users that these are not _necessary_ requirements).
- If you're using `conda`, you can export your current environment, e.g. `conda export > environment.yaml`.
- If you're using `uv`, you can use `uv lock --upgrade`.


## Parting words

If in doubt, ask! Slack, Teams, email, GitHub -- all work. And don't worry about getting it perfect; any issues with style should be corrected during code review and merge.

Finally, note that the aim is not to achieve complete stylistic uniformity. If it were, we'd just use the [Black](https://github.com/psf/black) code autoformatter, for example. Think of it like writing an academic paper: there are writing conventions in each academic subfield, and following these conventions improves clarity and understanding within that community. However, well-written papers don't sound like they were algorithmically generated; the author's unique voice should still shine through.
