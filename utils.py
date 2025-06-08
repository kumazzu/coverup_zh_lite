"""
utils.py
------------------------------------------
子进程执行小工具。支持自定义 env，避免与 coverage_utils 循环导入。
"""
from __future__ import annotations
from pathlib import Path
from typing import Sequence, Mapping, Tuple
import subprocess, os, shlex


def run(cmd: Sequence[str] | str,
        cwd: Path | None = None,
        timeout: int = 120,
        env: Mapping[str, str] | None = None) -> Tuple[int, str, str]:
    """
    同步执行子进程，返回 (returncode, stdout, stderr)
    """
    if isinstance(cmd, str):
        cmd = shlex.split(cmd)

    proc = subprocess.run(
        list(cmd),
        cwd=str(cwd) if cwd else None,
        text=True,
        timeout=timeout,
        capture_output=True,
        env=env if env is not None else os.environ.copy()
    )
    return proc.returncode, proc.stdout, proc.stderr
