#!/usr/bin/env python3
import os
from pathlib import Path


def _parse_env_file(path):
    values = {}
    if not path.exists():
        return values

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            values[key] = value

    return values


def get_config():
    script_dir = Path(__file__).resolve().parent
    base_dir = script_dir.parent
    config_dir = base_dir / "config"

    merged = {}
    merged.update(_parse_env_file(config_dir / "defaults.env"))
    merged.update(_parse_env_file(config_dir / "local.env"))

    extra_path = os.getenv("CONNECTIVITY_CONFIG")
    if extra_path:
        merged.update(_parse_env_file(Path(extra_path).expanduser()))

    merged.update(os.environ)
    return merged
