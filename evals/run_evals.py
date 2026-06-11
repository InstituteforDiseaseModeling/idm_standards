#!/usr/bin/env python3
"""Eval harness for the idm-standards plugin's audit/fix skills.

Each fixture under ``fixtures/<name>/`` ships a ``project/`` subdirectory (a small,
deliberately-flawed sample project) and an ``expected.yaml`` describing the behavior the
audit should exhibit. The harness copies each fixture's project to a temp directory, runs
the audit skill headlessly via the Claude CLI, parses the resulting ``code_audit.md``, and
asserts against the expectations.

Because the scorers are LLM-driven and nondeterministic, assertions are on *bounds* and
*presence/absence patterns*, never exact scores. Runs cost real tokens — this is an
on-demand harness (``./run_evals``), not a CI gate. See README.md for cost notes.

By default the harness streams a live, per-event activity log (tool calls, subagent
dispatches, elapsed time) from each headless CLI run, so you can see what it's doing
instead of waiting in silence. Pass ``--quiet`` to suppress it and print only phase results.

Usage:
    python run_evals.py                  # run all fixtures (audit only)
    python run_evals.py python_tier1     # run one fixture
    python run_evals.py --roundtrip      # also run the audit→fix→audit round-trip check
    python run_evals.py --quiet          # suppress the live activity log
    python run_evals.py --cli "claude"   # override the CLI command
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")

HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures"

# Skill invocation: R fixtures use audit-r-code; everything else uses audit-code (which
# would route to audit-r-code on its own, but invoking directly keeps the eval explicit).
AUDIT_SKILL = {"r": "audit-r-code"}


TIMEOUT = 1800


def _truncate(s, n=70):
    s = " ".join(str(s).split())
    return s if len(s) <= n else s[: n - 1] + "…"


def _format_event(evt):
    """Render one stream-json event as a short activity line, or None to skip it."""
    etype = evt.get("type")
    if etype == "assistant":
        lines = []
        for block in evt.get("message", {}).get("content", []):
            btype = block.get("type")
            if btype == "text" and block.get("text", "").strip():
                lines.append("💬 " + _truncate(block["text"]))
            elif btype == "tool_use":
                name = block.get("name", "?")
                inp = block.get("input", {})
                # Surface the most informative argument for common tools.
                hint = (inp.get("command") or inp.get("description")
                        or inp.get("subagent_type") or inp.get("file_path")
                        or inp.get("pattern") or inp.get("skill") or "")
                lines.append(f"🔧 {name}" + (f" — {_truncate(hint, 60)}" if hint else ""))
        return lines
    if etype == "result":
        dur = evt.get("duration_ms")
        suffix = f" ({dur/1000:.0f}s CLI)" if isinstance(dur, (int, float)) else ""
        return [f"✓ result{suffix}"]
    return None


def run_skill(cli, project_dir, prompt, label="", verbose=True):
    """Invoke a slash command headlessly, streaming a live activity log.

    Uses ``--output-format stream-json --verbose`` so the CLI emits events (tool
    calls, subagent dispatches, the final result) as they happen instead of going
    silent until completion. Each event is rendered as a short indented line.
    Returns the CLI's combined raw output.
    """
    cmd = [
        *cli.split(),
        "-p", prompt,
        "--permission-mode", "acceptEdits",
        "--add-dir", str(project_dir),
        "--output-format", "stream-json",
        "--verbose",
    ]
    start = time.monotonic()
    proc = subprocess.Popen(
        cmd, cwd=project_dir, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, text=True, bufsize=1,
    )
    timer = threading.Timer(TIMEOUT, proc.kill)
    timer.start()
    captured = []
    try:
        for line in proc.stdout:
            captured.append(line)
            line = line.strip()
            if not line:
                continue
            try:
                evt = json.loads(line)
            except json.JSONDecodeError:
                if verbose:
                    print(f"    | {_truncate(line, 100)}")
                continue
            rendered = _format_event(evt) if verbose else None
            for out in rendered or []:
                print(f"    | [{time.monotonic() - start:5.0f}s] {out}")
        proc.wait()
    finally:
        timer.cancel()
    print(f"    └─ {label or 'skill'} finished in {time.monotonic() - start:.0f}s")
    return "".join(captured)


def parse_report(report_path):
    """Parse code_audit.md into header fields, per-metric scores, and matchable text.

    ``text`` is the whole lowercased report (used by the round-trip check).
    ``rec_text`` is just the Recommendations + Proposed solutions sections (used by the
    must_appear / must_not_appear checks) — so a recommendation assertion isn't matched
    against the metric-table Notes, the Summary prose, or the Full Results YAML, where a
    correct report legitimately *mentions* a phrase (e.g. "no lock file needed") while
    not *recommending* it. The "Suppressed by config" section is also excluded: it
    intentionally quotes the suppressing directives, which would otherwise false-match a
    must_not_appear assertion for the very thing the config suppressed.
    """
    text = report_path.read_text()
    out = {"text": text.lower(), "metrics": {}, "overall": None, "version": ""}

    m = re.search(r"\*\*Overall Score\*\*:\s*(\d+)\s*/\s*100", text)
    if m:
        out["overall"] = int(m.group(1))

    m = re.search(r"\*\*Version\*\*:\s*(.+)", text)
    if m:
        out["version"] = m.group(1).strip()

    # Per-metric table rows: "| correct | 8/10 | ... |"
    for name, score in re.findall(r"\|\s*(\w+)\s*\|\s*(\d+)\s*/\s*10\s*\|", text):
        out["metrics"][name] = int(score)

    # Recommendations + Proposed solutions sections, each captured up to the next "## "
    # heading so the "Suppressed by config" section in between is excluded (it quotes the
    # suppressing directives). Fall back to the whole report if neither section is present.
    def section(title):
        mm = re.search(rf"##\s*{title}(.*?)(?:\n##\s|\Z)", text, re.S)
        return mm.group(1) if mm else ""

    rec = section("Recommendations") + "\n" + section("Proposed solutions")
    out["rec_text"] = (rec if rec.strip() else text).lower()
    return out


def check(expected, report, scope_key=None):
    """Assert a report against expectations; return (passed, [failure messages])."""
    failures = []
    exp = expected if scope_key is None else expected.get(scope_key, {})

    rng = expected.get("overall_score", {})
    if scope_key is None and report["overall"] is not None:
        if "min" in rng and report["overall"] < rng["min"]:
            failures.append(f"overall {report['overall']} < min {rng['min']}")
        if "max" in rng and report["overall"] > rng["max"]:
            failures.append(f"overall {report['overall']} > max {rng['max']}")

    if scope_key is None:
        for metric, bounds in expected.get("metrics", {}).items():
            score = report["metrics"].get(metric)
            if score is None:
                failures.append(f"metric '{metric}' missing from report")
                continue
            if "min" in bounds and score < bounds["min"]:
                failures.append(f"{metric} {score} < min {bounds['min']}")
            if "max" in bounds and score > bounds["max"]:
                failures.append(f"{metric} {score} > max {bounds['max']}")

        want_version = expected.get("report_version_contains")
        if want_version and want_version.lower() not in report["version"].lower():
            failures.append(f"report Version '{report['version']}' lacks '{want_version}'")

    # Recommendation assertions match against the Recommendations + Proposed solutions
    # sections only (see parse_report), matching the documented scope in README.md.
    rec_text = report.get("rec_text", report["text"])
    for needle in exp.get("must_appear", []):
        if needle.lower() not in rec_text:
            failures.append(f"expected to find '{needle}' in recommendations")
    for needle in exp.get("must_not_appear", []):
        if needle.lower() in rec_text:
            failures.append(f"did NOT expect '{needle}' in recommendations")

    return (not failures), failures


def run_fixture(name, cli, roundtrip, verbose=True):
    """Run one fixture; return True if all assertions pass."""
    fixture = FIXTURES / name
    expected = yaml.safe_load((fixture / "expected.yaml").read_text())
    src = fixture / expected["project_subdir"]
    tier = expected["tier"]
    strictness = expected.get("strictness", 1)
    skill = AUDIT_SKILL.get(expected["language"], "audit-code")

    all_ok = True
    with tempfile.TemporaryDirectory(prefix=f"eval-{name}-") as tmp:
        proj = Path(tmp) / "project"
        shutil.copytree(src, proj)
        subprocess.run(["git", "init", "-q"], cwd=proj)
        subprocess.run(["git", "add", "-A"], cwd=proj)
        subprocess.run(
            ["git", "-c", "user.email=eval@idm", "-c", "user.name=eval",
             "commit", "-q", "-m", "fixture"], cwd=proj,
        )

        # --- Primary audit ---
        print(f"[{name}] audit at tier {tier}, strictness {strictness} via {skill} ...")
        run_skill(cli, proj, f"/idm-standards:{skill} . {tier} {strictness}",
                  label="audit", verbose=verbose)
        report_path = proj / "code_audit.md"
        if not report_path.exists():
            print(f"  FAIL: {report_path.name} not written")
            return False
        report = parse_report(report_path)
        report1_text = report_path.read_text()  # strictness-1 report, for the round-trip baseline
        ok, failures = check(expected, report)
        all_ok &= ok
        _print_result(name, "audit", ok, failures)

        # --- Strictness-2 re-run (if specified) ---
        if "strictness2" in expected:
            s2 = expected["strictness2"]["strictness"]
            print(f"[{name}] re-audit at strictness {s2} ...")
            run_skill(cli, proj, f"/idm-standards:{skill} . {tier} {s2}",
                      label=f"strictness-{s2} audit", verbose=verbose)
            report2 = parse_report(report_path)
            ok2, failures2 = check(expected, report2, scope_key="strictness2")
            all_ok &= ok2
            _print_result(name, f"strictness-{s2}", ok2, failures2)

        # --- Round-trip: audit → fix → audit (CK's two acceptance criteria) ---
        if roundtrip:
            # A strictness-2 re-run above may have overwritten the report; restore the
            # strictness-1 report so the re-audit reconciles against the same baseline
            # the `before` metrics came from. (fix-code hasn't run yet, so the project
            # itself is still pristine.)
            report_path.write_text(report1_text)
            before = report["metrics"].copy()
            before_overall = report["overall"]
            print(f"[{name}] fix-code, then re-audit ...")
            run_skill(cli, proj, "/idm-standards:fix-code .",
                      label="fix-code", verbose=verbose)
            run_skill(cli, proj, f"/idm-standards:{skill} . {tier} {strictness}",
                      label="re-audit", verbose=verbose)
            after = parse_report(report_path)
            rt_failures = []
            # (a) overall score must not decrease
            if before_overall is not None and after["overall"] is not None:
                if after["overall"] < before_overall:
                    rt_failures.append(
                        f"overall dropped after fixes: {before_overall} → {after['overall']}"
                    )
            # (a') per-metric: no metric should drop after fixes without a recorded
            #      "Score changes since last run" justification
            for metric, prior in before.items():
                now = after["metrics"].get(metric)
                if now is not None and now < prior:
                    if "score changes since last run" not in after["text"]:
                        rt_failures.append(
                            f"{metric} dropped {prior} → {now} with no justification section"
                        )
            ok_rt = not rt_failures
            all_ok &= ok_rt
            _print_result(name, "round-trip", ok_rt, rt_failures)

    return all_ok


def _print_result(name, phase, ok, failures):
    status = "PASS" if ok else "FAIL"
    print(f"  [{name}] {phase}: {status}")
    for f in failures:
        print(f"    - {f}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("fixtures", nargs="*", help="fixture names (default: all)")
    ap.add_argument("--cli", default="claude", help="Claude CLI command (default: claude)")
    ap.add_argument("--roundtrip", action="store_true",
                    help="also run the audit→fix→audit round-trip check (slow, costly)")
    ap.add_argument("--quiet", action="store_true",
                    help="suppress the live per-event activity log (only print phase results)")
    args = ap.parse_args()

    names = args.fixtures or sorted(p.name for p in FIXTURES.iterdir() if p.is_dir())
    results = {
        n: run_fixture(n, args.cli, args.roundtrip, verbose=not args.quiet)
        for n in names
    }

    print("\n=== Summary ===")
    for n, ok in results.items():
        print(f"  {'PASS' if ok else 'FAIL'}  {n}")
    sys.exit(0 if all(results.values()) else 1)


if __name__ == "__main__":
    main()
