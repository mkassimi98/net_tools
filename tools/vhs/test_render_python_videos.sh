#!/usr/bin/env bash
set -euo pipefail

TEST_DIR="$(mktemp -d)"
trap 'rm -rf "$TEST_DIR"' EXIT

FIXTURE_ROOT="$TEST_DIR/repo"
FIXTURE_VHS_DIR="$FIXTURE_ROOT/tools/vhs"
FIXTURE_BIN="$TEST_DIR/bin"
RENDERER="$FIXTURE_VHS_DIR/render_python_videos.sh"
MANIFEST="$FIXTURE_VHS_DIR/python-videos.manifest"
FAKE_VHS_CAPTURE="$TEST_DIR/rendered.tape"
FAKE_VHS_CALLS="$TEST_DIR/vhs-calls.log"

mkdir -p "$FIXTURE_VHS_DIR" "$FIXTURE_BIN"
cp "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/render_python_videos.sh" "$RENDERER"
cp "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/python-videos.manifest" "$MANIFEST"
chmod +x "$RENDERER"

while IFS='|' read -r key command extra; do
  [[ -z "${key//[[:space:]]/}" || "$key" =~ ^[[:space:]]*# ]] && continue
  read -r _ script_path _ <<<"$command"
  mkdir -p "$FIXTURE_ROOT/$(dirname "$script_path")"
  printf '%s\n' 'print("fixture")' >"$FIXTURE_ROOT/$script_path"
done <"$MANIFEST"

cat >"$FIXTURE_BIN/vhs" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
tape="$1"
printf '%s\n' "$tape" >>"$FAKE_VHS_CALLS"
cp "$tape" "$FAKE_VHS_CAPTURE"
output="$(
  sed -n 's/^Output "\(.*\)"$/\1/p' "$tape" | head -n 1
)"
if [[ "${FAKE_VHS_SKIP_OUTPUT:-0}" == "1" ]]; then
  exit 0
fi
mkdir -p "$(dirname "$output")"
printf 'GIF89a' >"$output"
EOF

for dependency in ttyd ffmpeg; do
  cat >"$FIXTURE_BIN/$dependency" <<'EOF'
#!/usr/bin/env bash
exit 0
EOF
done
chmod +x "$FIXTURE_BIN/"*

export PATH="$FIXTURE_BIN:$PATH"
export FAKE_VHS_CAPTURE FAKE_VHS_CALLS

fail() {
  printf 'FAIL: %s\n' "$*" >&2
  exit 1
}

assert_contains() {
  local output="$1"
  local expected="$2"
  [[ "$output" == *"$expected"* ]] ||
    fail "expected output to contain: $expected"
}

assert_file() {
  local path="$1"
  [[ -f "$path" ]] || fail "expected file to exist: $path"
}

assert_not_file() {
  local path="$1"
  [[ ! -e "$path" ]] || fail "expected file not to exist: $path"
}

assert_failure_with() {
  local expected="$1"
  shift
  local output
  local status

  set +e
  output="$("$@" 2>&1)"
  status=$?
  set -e

  [[ "$status" -ne 0 ]] || fail "expected command to fail: $*"
  assert_contains "$output" "$expected"
}

assert_contains "$("$RENDERER" --list)" "S03_01_interfaces"
assert_contains "$("$RENDERER" --validate)" "Manifest valid: 30 recordings"

"$RENDERER" --one S03_01_interfaces >/dev/null
GIF_OUTPUT="$FIXTURE_ROOT/captures/videos/python/S03_01_interfaces.gif"
MP4_OUTPUT="$FIXTURE_ROOT/captures/videos/python/S03_01_interfaces.mp4"
GIF_STATE="$FIXTURE_ROOT/captures/videos/python/.S03_01_interfaces.gif.sha256"
assert_file "$GIF_OUTPUT"
assert_file "$GIF_STATE"
assert_not_file "$MP4_OUTPUT"
GENERATED_TAPE="$(cat "$FAKE_VHS_CAPTURE")"
assert_contains "$GENERATED_TAPE" "Output \"$GIF_OUTPUT\""
assert_contains "$GENERATED_TAPE" "Set WaitTimeout 10m"
assert_contains "$GENERATED_TAPE" "Type \"export PS1='net-tools> '\""

wait_count="$(
  grep -Fxc 'Wait+Line /net-tools>$/' "$FAKE_VHS_CAPTURE"
)"
[[ "$wait_count" -eq 2 ]] ||
  fail "expected two prompt waits, got: $wait_count"

command_enter_line="$(
  grep -nF 'Type "python3 scripts/interface-inspection/python/interfaces.py"' \
    "$FAKE_VHS_CAPTURE" | cut -d: -f1
)"
final_wait_line="$(
  grep -nF 'Wait+Line /net-tools>$/' "$FAKE_VHS_CAPTURE" | tail -n 1 | cut -d: -f1
)"
final_sleep_line="$(
  grep -nF 'Sleep 2s' "$FAKE_VHS_CAPTURE" | cut -d: -f1
)"
[[ "$command_enter_line" -lt "$final_wait_line" ]] ||
  fail "expected prompt wait after the Python command"
[[ "$final_wait_line" -lt "$final_sleep_line" ]] ||
  fail "expected final sleep after the command-completion wait"

calls_before_skip="$(wc -l <"$FAKE_VHS_CALLS")"
skip_output="$("$RENDERER" --one S03_01_interfaces)"
calls_after_skip="$(wc -l <"$FAKE_VHS_CALLS")"
assert_contains "$skip_output" "Skipping S03_01_interfaces (up to date:"
[[ "$calls_before_skip" -eq "$calls_after_skip" ]] ||
  fail "expected an existing GIF to skip VHS"

printf '%s\n' '# source changed' \
  >>"$FIXTURE_ROOT/scripts/interface-inspection/python/interfaces.py"
stale_output="$("$RENDERER" --one S03_01_interfaces)"
calls_after_stale="$(wc -l <"$FAKE_VHS_CALLS")"
assert_contains "$stale_output" "Rendering S03_01_interfaces (stale recording)"
[[ "$calls_after_stale" -eq $((calls_after_skip + 1)) ]] ||
  fail "expected a changed source script to regenerate its GIF"

force_output="$("$RENDERER" --force --one S03_01_interfaces)"
calls_after_force="$(wc -l <"$FAKE_VHS_CALLS")"
assert_contains "$force_output" "Rendering S03_01_interfaces"
[[ "$calls_after_force" -eq $((calls_after_stale + 1)) ]] ||
  fail "expected --force to render an existing GIF"

REALTIME_OUTPUT="$FIXTURE_ROOT/captures/videos/python/S07_08_realtime_traffic_iftop_nethogs_bmon.gif"
rm -f "$REALTIME_OUTPUT"
"$RENDERER" --one S07_08_realtime_traffic_iftop_nethogs_bmon >/dev/null
assert_contains \
  "$(cat "$FAKE_VHS_CAPTURE")" \
  'Type "python3 scripts/traffic-capture-analysis/python/realtime_traffic.py -a"'

while IFS='|' read -r key command extra; do
  [[ -z "${key//[[:space:]]/}" || "$key" =~ ^[[:space:]]*# ]] && continue
  printf 'GIF89a' >"$FIXTURE_ROOT/captures/videos/python/${key}.gif"
done <"$MANIFEST"

rm -f "$FIXTURE_ROOT/captures/videos/python/.S03_02_routes_and_route_get.gif.sha256"
calls_before_missing_state="$(wc -l <"$FAKE_VHS_CALLS")"
missing_state_output="$("$RENDERER" --one S03_02_routes_and_route_get)"
calls_after_missing_state="$(wc -l <"$FAKE_VHS_CALLS")"
assert_contains "$missing_state_output" "Rendering S03_02_routes_and_route_get (stale recording)"
[[ "$calls_after_missing_state" -eq $((calls_before_missing_state + 1)) ]] ||
  fail "expected a GIF without state metadata to regenerate"

rm -f "$GIF_OUTPUT"
assert_failure_with "VHS did not create a non-empty output file: $GIF_OUTPUT" \
  env FAKE_VHS_SKIP_OUTPUT=1 "$RENDERER" --one S03_01_interfaces

cp "$MANIFEST" "$TEST_DIR/valid.manifest"
printf '%s\n' \
  'S03_01_interfaces|python3 scripts/interface-inspection/python/interfaces.py' \
  >>"$MANIFEST"
assert_failure_with "Duplicate video key at line 31: S03_01_interfaces" \
  "$RENDERER" --validate

cp "$TEST_DIR/valid.manifest" "$MANIFEST"
printf '%s\n' \
  'S99_01_missing|python3 scripts/missing/python/nope.py' \
  >>"$MANIFEST"
assert_failure_with \
  "Python script not found at line 31: scripts/missing/python/nope.py" \
  "$RENDERER" --validate

cp "$TEST_DIR/valid.manifest" "$MANIFEST"
printf '%s\n' 'bad key|python3 scripts/interface-inspection/python/interfaces.py' \
  >>"$MANIFEST"
assert_failure_with "Invalid video key at line 31: bad key" \
  "$RENDERER" --validate

cp "$TEST_DIR/valid.manifest" "$MANIFEST"
assert_failure_with "Missing key for --one" "$RENDERER" --one
assert_failure_with "Video key not found: unknown" "$RENDERER" --one unknown

printf '%s\n' "PASS: VHS Python recording renderer"
