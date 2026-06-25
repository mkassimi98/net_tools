# Python VHS GIF Recordings Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the existing VHS automation reliably produce correctly named GIF recordings for all 30 Python workshop demos.

**Architecture:** Keep the manifest as the recording inventory and generate temporary VHS tapes from it. Add a shell test harness around the renderer so manifest validation, CLI behavior, GIF defaults, and tape generation can be exercised without running privileged network demos.

**Tech Stack:** Bash, VHS, shell assertions, existing pipe-delimited manifest, Markdown documentation.

---

## File structure

- Create `tools/vhs/test_render_python_videos.sh`: isolated behavior tests using a
  temporary repository copy and a fake VHS executable.
- Modify `tools/vhs/render_python_videos.sh`: GIF default, manifest validation,
  safer CLI parsing, testable tape generation, and accurate messages.
- Modify `python-video-recording-runbook.md`: replace MP4 naming and output
  guidance with GIF guidance and document validation.
- Modify `README.md`: describe the VHS GIF workflow and generated output.

### Task 1: Capture expected renderer behavior in tests

**Files:**
- Create: `tools/vhs/test_render_python_videos.sh`
- Test: `tools/vhs/test_render_python_videos.sh`

- [ ] **Step 1: Write tests for GIF output, inventory, and validation**

Create a Bash test harness that copies the renderer and manifest into a temporary
fixture, supplies a fake `vhs` binary, and checks:

```bash
assert_contains "$("$RENDERER" --list)" "S03_01_interfaces"
assert_file "$FIXTURE_ROOT/captures/videos/python/S03_01_interfaces.gif"
assert_contains "$(cat "$FAKE_VHS_CAPTURE")" \
  'Output "'"$FIXTURE_ROOT"'/captures/videos/python/S03_01_interfaces.gif"'
assert_failure_with "Duplicate video key" "$RENDERER" --validate
assert_failure_with "Python script not found" "$RENDERER" --validate
```

The fake VHS executable records the supplied tape and touches the tape's output
path, allowing the test to verify generated filenames without launching a
terminal or network command.

- [ ] **Step 2: Run the tests and verify RED**

Run:

```bash
bash tools/vhs/test_render_python_videos.sh
```

Expected: FAIL because the current default is MP4 and `--validate` does not
exist.

- [ ] **Step 3: Commit the failing test**

```bash
git add tools/vhs/test_render_python_videos.sh
git commit -m "test: define VHS GIF renderer behavior"
```

### Task 2: Implement GIF rendering and manifest validation

**Files:**
- Modify: `tools/vhs/render_python_videos.sh`
- Test: `tools/vhs/test_render_python_videos.sh`

- [ ] **Step 1: Add manifest validation**

Implement `validate_manifest` so every non-empty, non-comment line:

- has a non-empty key and command separated by `|`;
- uses a key containing only letters, digits, `_`, `.` or `-`;
- has a unique key;
- invokes a Python path below the repository;
- points to an existing `.py` file.

Add `--validate` to run this check without requiring VHS dependencies.

- [ ] **Step 2: Make GIF the default and harden argument parsing**

Set:

```bash
VHS_OUTPUT_FORMAT="${VHS_OUTPUT_FORMAT:-gif}"
```

Reject missing `--one` arguments cleanly, validate the manifest before list or
render operations, and update usage examples to show GIF as the default.

- [ ] **Step 3: Preserve generated tape behavior**

Keep temporary tapes at:

```text
captures/vhs-tapes/<key>.tape
```

and write recordings to:

```text
captures/videos/python/<key>.<format>
```

Continue supporting `VHS_OUTPUT_FORMAT` as an intentional override.

- [ ] **Step 4: Run the focused tests and verify GREEN**

Run:

```bash
bash tools/vhs/test_render_python_videos.sh
```

Expected: all renderer behavior tests pass.

- [ ] **Step 5: Run static shell checks**

Run:

```bash
bash -n tools/vhs/render_python_videos.sh
bash -n tools/vhs/setup_vhs_ubuntu.sh
bash -n tools/vhs/test_render_python_videos.sh
```

Expected: all commands exit zero with no output.

- [ ] **Step 6: Commit implementation and tests**

```bash
git add tools/vhs/render_python_videos.sh tools/vhs/test_render_python_videos.sh
git commit -m "feat: render Python workshop recordings as GIF"
```

### Task 3: Correct recording documentation

**Files:**
- Modify: `python-video-recording-runbook.md`
- Modify: `README.md`

- [ ] **Step 1: Update the runbook**

Change the naming convention to:

```text
S<SECTION>_<STEP>_<topic>.gif
```

Change all 30 suggested filenames from `.mp4` to `.gif`, describe GIF as the
default output, add the `--validate` command, and retain an example showing how
to opt into another supported VHS output format.

- [ ] **Step 2: Update README recording guidance**

Replace the asciinema-first recommendation for these Python demos with the
repository's VHS workflow:

```bash
./tools/vhs/render_python_videos.sh --validate
./tools/vhs/render_python_videos.sh --one S03_01_interfaces
./tools/vhs/render_python_videos.sh --all
```

State that generated GIFs are written below `captures/videos/python/`.

- [ ] **Step 3: Verify documentation consistency**

Run:

```bash
if rg -n '\.mp4|VHS_OUTPUT_FORMAT=mp4' \
  python-video-recording-runbook.md README.md; then
  exit 1
fi
```

Expected: no matches and exit zero.

- [ ] **Step 4: Commit documentation**

```bash
git add python-video-recording-runbook.md README.md
git commit -m "docs: document Python VHS GIF recordings"
```

### Task 4: Verify the complete inventory and a real GIF render

**Files:**
- Verify: `tools/vhs/python-videos.manifest`
- Verify: `tools/vhs/render_python_videos.sh`
- Verify: `captures/videos/python/S03_04_hostname_ip_summary.gif`

- [ ] **Step 1: Verify manifest coverage**

Run:

```bash
python_count="$(
  find scripts -path '*/python/*.py' ! -name '_config.py' | wc -l
)"
manifest_count="$(
  awk -F'|' 'NF >= 2 && $1 !~ /^[[:space:]]*#/ { count++ } END { print count+0 }' \
    tools/vhs/python-videos.manifest
)"
test "$python_count" -eq "$manifest_count"
test "$manifest_count" -eq 30
./tools/vhs/render_python_videos.sh --validate
```

Expected: both counts are 30 and validation succeeds.

- [ ] **Step 2: Render one safe representative GIF**

Run:

```bash
./tools/vhs/render_python_videos.sh --one S03_04_hostname_ip_summary
```

Expected: VHS exits zero and creates a non-empty
`captures/videos/python/S03_04_hostname_ip_summary.gif`.

- [ ] **Step 3: Verify the GIF file signature**

Run:

```bash
file captures/videos/python/S03_04_hostname_ip_summary.gif
test -s captures/videos/python/S03_04_hostname_ip_summary.gif
```

Expected: `file` identifies GIF image data and the size check succeeds.

- [ ] **Step 4: Run the full regression verification**

Run:

```bash
bash tools/vhs/test_render_python_videos.sh
bash -n tools/vhs/render_python_videos.sh
./tools/vhs/render_python_videos.sh --validate
git diff --check
```

Expected: every command exits zero.
