"""Shared config loader for vpn-remote-access scripts."""
import os
from pathlib import Path

_CONFIG_DIR = Path(__file__).parent.parent / "config"

_DEFAULTS = {
    "VPN_INTERFACE": "tun1",
    "VPN_PING_TARGET": "1.0.0.1",
    "VPN_PING_COUNT": "4",
    "VPN_SSH_TARGET": "",
}


def get_config():
    cfg = dict(_DEFAULTS)

    def _load(path):
        try:
            for line in Path(path).read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, val = line.partition("=")
                cfg[key.strip()] = val.strip()
        except FileNotFoundError:
            pass

    _load(_CONFIG_DIR / "defaults.env")
    _load(_CONFIG_DIR / "local.env")
    external = os.environ.get("VPN_CONFIG", "")
    if external:
        _load(external)
    cfg.update({k: v for k, v in os.environ.items() if k in _DEFAULTS})
    return cfg
