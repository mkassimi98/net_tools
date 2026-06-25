# Python VHS GIF recordings

## Goal

Complete the existing VHS automation for all Python workshop demos in checklist
sections 3 through 7. The generated recordings must be GIF files, despite the
older MP4 wording in the runbook.

## Scope

- Cover every runnable Python demo under `scripts/*/python/`, excluding shared
  `_config.py` modules.
- Preserve the existing recording keys and use them as output basenames, for
  example `S03_01_interfaces.gif`.
- Keep `tools/vhs/python-videos.manifest` as the single source of truth for
  recording order, command, and output basename.
- Keep generated tapes and recordings below `captures/`.
- Update the runbook and README so their examples and instructions describe GIF
  output accurately.
- Do not change the behavior of the Python workshop scripts.

## Design

`tools/vhs/render_python_videos.sh` will continue to generate one temporary VHS
tape per manifest entry. GIF becomes the default output format while retaining
an environment-variable override for users who deliberately want another VHS
format.

The command-line interface remains:

- `--list`: show configured recording keys and commands without requiring VHS.
- `--one <key>`: render one configured recording.
- `--all`: render all configured recordings in manifest order.

Before rendering, the script will validate the complete manifest. Validation
will reject malformed or duplicate entries and report commands whose referenced
Python script does not exist. This prevents a long batch from starting with an
incomplete recording inventory.

The generated tape will:

1. Open a Bash shell with the configured dimensions and theme.
2. Change to the repository root while hidden.
3. Clear the terminal.
4. Show and type the manifest command.
5. Wait for the command to finish and pause briefly so the final output remains
   visible.

## Recording inventory and names

The existing 30 manifest entries are retained. Their keys map directly to GIF
filenames:

```text
captures/videos/python/<recording-key>.gif
```

Examples:

```text
captures/videos/python/S03_01_interfaces.gif
captures/videos/python/S05_03_port_owner_ss_lsof.gif
captures/videos/python/S07_08_realtime_traffic_iftop_nethogs_bmon.gif
```

## Privileged and environment-dependent demos

The automation will not bypass privileges or fabricate network results.
Recordings that use packet capture, link inspection, or real-time traffic tools
may require a refreshed sudo timestamp and suitable local configuration.
Documentation will tell the operator to run `sudo -v` before a batch containing
privileged demos.

Scripts that require external services or live targets, such as `iperf3`, keep
using their existing category configuration. Their recording commands remain
stable because parameters are supplied through the current defaults and local
override mechanism.

## Error handling

- Missing `vhs`, `ttyd`, or `ffmpeg` produces an actionable setup message.
- An unknown `--one` key prints the valid inventory and exits non-zero.
- Missing `--one` values and unknown arguments exit non-zero with usage.
- Invalid manifest entries prevent rendering and identify the offending line.
- VHS rendering failures stop the batch because partial success should be
  visible to the operator rather than silently skipped.

## Verification

Verification will avoid running all live network demos:

- Run Bash syntax checks on VHS helper scripts.
- Exercise help and list modes.
- Verify there are exactly as many manifest entries as runnable Python demos.
- Verify every manifest command points to an existing Python file.
- Verify all keys are unique and all default output names end in `.gif`.
- Generate or inspect a representative tape without requiring the complete
  privileged recording batch.

Actual rendering of all 30 GIFs remains an operator action because results
depend on the machine's interfaces, installed networking tools, sudo state, and
configured targets.

## Out of scope

- Recording Bash variants.
- Rewriting the Python demos.
- Embedding generated GIF binaries in Git.
- Creating one permanently tracked `.tape` file per recording.
- Automating external lab infrastructure such as an `iperf3` server.
