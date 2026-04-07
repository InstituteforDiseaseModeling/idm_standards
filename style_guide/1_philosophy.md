# IDM design philosophy

IDM's overall design philosophy is "**Common tasks should be simple**, while uncommon tasks can't always be simple, but still should be possible".

## Writing for the right audience

The audience for IDM is *scientists*, not software developers. Assume that the average IDM user dislikes coding and wants something that *just works*. Implications of this include:

- Commands should be short, simple, and obvious, e.g. `cv.Sim().run().plot()`.
- Be as flexible as possible with user inputs. If a user could only mean one thing, do that. If the user provides `[0, 7, 14]` but the function needs an array instead of a list, convert the list to an array automatically (`sc.toarray()` exists for exactly this reason).
- If there's a "sensible" default value for something, use it. Users shouldn't *have* to think about false positivity rate or influenza-like illness prevalence if they just want to quickly add testing to their simulation via `cv.test_prob(0.1)`.
- However, hard-code as little as possible. For example, rather than defining a variable at the top of the function, make it a keyword argument with a default value so the user can modify it if needed. As another example, pass keyword arguments where possible -- e.g., `to_json(..., **kwargs)` can pass arbitrary extra arguments via `json.dump(**kwargs)`.
- Ensure the logic, especially the scientific logic, of the code is as clear as possible. If something is "bad" coding style but good science, you should probably do it anyway.

## Workload considerations

The total work your code creates is:

*W* = Σ(*u + n×r + m×e*)

where:

- *W* is the total work
- Σ is a sum over each person *p*
- *u* is the ramp-up time
- *n* is the number of reads
- *r* is the time per read
- *m* is the number of edits
- *e* is the time per edit

Implications of this include:

- Common mistakes are to overemphasize *p* = 0 (you) over *p* > 0, and *e* (edit time) over *u* (ramp-up time) and *r* (read time).
- Assume people of different backgrounds and skill levels will be using/interacting with this code. You might be comfortable with lambda functions and overriding dunder methods, but assume others are not. Use these "advanced features" only as a last resort.
- Similarly, try to avoid complex dependencies (e.g. nested class inheritance) as they increase ramp-up time, and make it more likely something will break. (But equally, don't repeat yourself -- it's a tradeoff.)
- Err on the side of more comments, including line comments. Logic that is clear to you now might not be clear to anyone else (or yourself 3 months from now). If you use a number that came from a scientific paper, please for the love of all that is precious put a link to that paper in a comment.