#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
MANIFEST="$SCRIPT_DIR/python-videos.manifest"
OUTPUT_DIR="$REPO_ROOT/captures/videos/python"
TMP_DIR="$REPO_ROOT/captures/vhs-tapes"

VHS_BIN="${VHS_BIN:-vhs}"
VHS_THEME="${VHS_THEME:-Catppuccin Frappe}"
VHS_WIDTH="${VHS_WIDTH:-1280}"
VHS_HEIGHT="${VHS_HEIGHT:-800}"
VHS_FONT_SIZE="${VHS_FONT_SIZE:-18}"
VHS_PADDING="${VHS_PADDING:-24}"
VHS_TYPING_SPEED="${VHS_TYPING_SPEED:-55ms}"
VHS_SLEEP_AFTER_COMMAND="${VHS_SLEEP_AFTER_COMMAND:-2s}"
VHS_WAIT_TIMEOUT="${VHS_WAIT_TIMEOUT:-10m}"
VHS_OUTPUT_FORMAT="${VHS_OUTPUT_FORMAT:-gif}"
FORCE_RENDER=0

usage() {
  cat <<'EOF'
Usage:
  tools/vhs/render_python_videos.sh --validate
  tools/vhs/render_python_videos.sh --list
  tools/vhs/render_python_videos.sh [--force] --one <video_key>
  tools/vhs/render_python_videos.sh [--force] --all

Examples:
  tools/vhs/render_python_videos.sh --validate
  tools/vhs/render_python_videos.sh --list
  tools/vhs/render_python_videos.sh --one S03_01_interfaces
  tools/vhs/render_python_videos.sh --all
  tools/vhs/render_python_videos.sh --force --one S03_01_interfaces
  VHS_OUTPUT_FORMAT=webm tools/vhs/render_python_videos.sh --one S03_01_interfaces
EOF
}

validate_manifest() {
  local line=""
  local key=""
  local cmd=""
  local script_path=""
  local line_number=0
  local entry_count=0
  local separators=""
  declare -A seen_keys=()

  if [[ ! -f "$MANIFEST" ]]; then
    echo "Manifest not found: $MANIFEST" >&2
    return 1
  fi

  while IFS= read -r line || [[ -n "$line" ]]; do
    ((line_number += 1))
    line="${line%$'\r'}"

    [[ -z "${line//[[:space:]]/}" ]] && continue
    [[ "$line" =~ ^[[:space:]]*# ]] && continue

    separators="${line//[^|]/}"
    if [[ ${#separators} -ne 1 ]]; then
      echo "Malformed manifest entry at line $line_number: expected key|command" >&2
      return 1
    fi

    IFS='|' read -r key cmd <<<"$line"
    if [[ -z "$key" || -z "$cmd" ]]; then
      echo "Malformed manifest entry at line $line_number: expected key|command" >&2
      return 1
    fi

    if [[ ! "$key" =~ ^[[:alnum:]_.-]+$ ]]; then
      echo "Invalid video key at line $line_number: $key" >&2
      return 1
    fi

    if [[ -n "${seen_keys[$key]+set}" ]]; then
      echo "Duplicate video key at line $line_number: $key" >&2
      return 1
    fi
    seen_keys["$key"]=1

    if [[ "$cmd" =~ ^python3[[:space:]]+([^[:space:]]+)([[:space:]].*)?$ ]]; then
      script_path="${BASH_REMATCH[1]}"
    else
      echo "Invalid Python command at line $line_number: $cmd" >&2
      return 1
    fi

    if [[ "$script_path" != scripts/*/python/*.py || "$script_path" == *".."* ]]; then
      echo "Python script must be under scripts/*/python at line $line_number: $script_path" >&2
      return 1
    fi

    if [[ ! -f "$REPO_ROOT/$script_path" ]]; then
      echo "Python script not found at line $line_number: $script_path" >&2
      return 1
    fi

    ((entry_count += 1))
  done <"$MANIFEST"

  if [[ "$entry_count" -eq 0 ]]; then
    echo "Manifest has no recording entries: $MANIFEST" >&2
    return 1
  fi

  echo "Manifest valid: $entry_count recordings"
}

require_deps() {
  if ! command -v "$VHS_BIN" >/dev/null 2>&1; then
    echo "vhs not found. Run tools/vhs/setup_vhs_ubuntu.sh first."
    exit 1
  fi
  if ! command -v ttyd >/dev/null 2>&1; then
    echo "ttyd not found. Run tools/vhs/setup_vhs_ubuntu.sh first."
    exit 1
  fi
  if ! command -v ffmpeg >/dev/null 2>&1; then
    echo "ffmpeg not found. Run tools/vhs/setup_vhs_ubuntu.sh first."
    exit 1
  fi
}

list_videos() {
  awk -F'|' '
    NF >= 2 && $0 !~ /^[[:space:]]*#/ {
      printf "%-45s %s\n", $1, $2
    }
  ' "$MANIFEST"
}

recording_fingerprint() {
  local cmd="$1"
  local script_path=""
  local category_dir=""
  local dependency=""

  if [[ "$cmd" =~ ^python3[[:space:]]+([^[:space:]]+) ]]; then
    script_path="${BASH_REMATCH[1]}"
  else
    return 1
  fi

  category_dir="$(dirname "$(dirname "$script_path")")"

  {
    printf '%s\0' \
      "$cmd" \
      "$VHS_OUTPUT_FORMAT" \
      "$VHS_THEME" \
      "$VHS_WIDTH" \
      "$VHS_HEIGHT" \
      "$VHS_FONT_SIZE" \
      "$VHS_PADDING" \
      "$VHS_TYPING_SPEED" \
      "$VHS_SLEEP_AFTER_COMMAND" \
      "$VHS_WAIT_TIMEOUT"

    for dependency in \
      "$SCRIPT_DIR/render_python_videos.sh" \
      "$REPO_ROOT/$script_path" \
      "$REPO_ROOT/$(dirname "$script_path")/_config.py" \
      "$REPO_ROOT/$category_dir/config/defaults.env" \
      "$REPO_ROOT/$category_dir/config/local.env"; do
      if [[ -f "$dependency" ]]; then
        printf '%s\0' "$dependency"
        sha256sum "$dependency"
      fi
    done
  } | sha256sum | awk '{print $1}'
}

render_entry() {
  local key="$1"
  local cmd="$2"
  local tape_file="$TMP_DIR/${key}.tape"
  local output_file="$OUTPUT_DIR/${key}.${VHS_OUTPUT_FORMAT}"
  local state_file="$OUTPUT_DIR/.${key}.${VHS_OUTPUT_FORMAT}.sha256"
  local expected_fingerprint=""
  local recorded_fingerprint=""

  expected_fingerprint="$(recording_fingerprint "$cmd")"
  if [[ -f "$state_file" ]]; then
    recorded_fingerprint="$(<"$state_file")"
  fi

  if [[ "$FORCE_RENDER" -eq 0 && -s "$output_file" ]]; then
    if [[ "$recorded_fingerprint" == "$expected_fingerprint" ]]; then
      echo "Skipping $key (up to date: $output_file)"
      return 0
    fi
    echo "Rendering $key (stale recording) -> $output_file"
  else
    echo "Rendering $key -> $output_file"
  fi

  cat >"$tape_file" <<EOF
Output "$output_file"

Set Shell "bash"
Set FontSize $VHS_FONT_SIZE
Set Width $VHS_WIDTH
Set Height $VHS_HEIGHT
Set Theme "$VHS_THEME"
Set Padding $VHS_PADDING
Set WindowBar Colorful
Set CursorBlink false
Set TypingSpeed $VHS_TYPING_SPEED
Set WaitTimeout $VHS_WAIT_TIMEOUT

Hide
Type "cd $REPO_ROOT"
Enter
Type "export PS1='net-tools> '"
Enter
Type "clear"
Enter
Wait+Line /net-tools>$/
Show

Type "$cmd"
Enter
Wait+Line /net-tools>$/
Sleep $VHS_SLEEP_AFTER_COMMAND
EOF

  rm -f "$output_file" "$state_file"
  "$VHS_BIN" "$tape_file"
  if [[ ! -s "$output_file" ]]; then
    echo "VHS did not create a non-empty output file: $output_file" >&2
    return 1
  fi
  printf '%s\n' "$expected_fingerprint" >"$state_file"
}

render_one() {
  local selected="$1"
  local found=0
  while IFS='|' read -r key cmd; do
    [[ -z "${key//[[:space:]]/}" || "$key" =~ ^[[:space:]]*# ]] && continue
    if [[ "$key" == "$selected" ]]; then
      render_entry "$key" "$cmd"
      found=1
      break
    fi
  done <"$MANIFEST"

  if [[ "$found" -eq 0 ]]; then
    echo "Video key not found: $selected"
    echo
    list_videos
    exit 1
  fi
}

render_all() {
  while IFS='|' read -r key cmd; do
    [[ -z "${key//[[:space:]]/}" || "$key" =~ ^[[:space:]]*# ]] && continue
    render_entry "$key" "$cmd"
  done <"$MANIFEST"
}

main() {
  mkdir -p "$OUTPUT_DIR" "$TMP_DIR"

  local mode=""
  local one_key=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --validate)
        mode="validate"
        shift
        ;;
      --list)
        mode="list"
        shift
        ;;
      --all)
        mode="all"
        shift
        ;;
      --force)
        FORCE_RENDER=1
        shift
        ;;
      --one)
        if [[ $# -lt 2 || -z "$2" || "$2" == -* ]]; then
          echo "Missing key for --one" >&2
          usage >&2
          exit 1
        fi
        mode="one"
        one_key="$2"
        shift 2
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        echo "Unknown argument: $1"
        usage
        exit 1
        ;;
    esac
  done

  case "$mode" in
    validate)
      validate_manifest
      ;;
    list)
      validate_manifest >/dev/null
      list_videos
      ;;
    one)
      validate_manifest >/dev/null
      require_deps
      render_one "$one_key"
      ;;
    all|"")
      validate_manifest >/dev/null
      require_deps
      render_all
      ;;
  esac
}

main "$@"
