"""
coverage_utils.py
--------------------------------------------------
SlipCover 封装 + pytest 调用
* run_test_and_get_cov 写临时文件 test_tmp_<uuid>.py
* pytest / SlipCover 均用 -k "not .fail" 跳过失败用例
"""
from __future__ import annotations
import json, sys, tempfile, os, uuid
from pathlib import Path
from typing import Dict, Tuple
from utils import run


# ──────────────────────────────────────────────
# SlipCover → JSON（路径绝对化）
# ──────────────────────────────────────────────
def slipcover_json(src_root: Path, tests_dir: Path, *, branch: bool = True) -> Dict:
    from utils import run  # 确保引用正确
    import tempfile, json, sys
    from pathlib import Path

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as jf:
        json_path = Path(jf.name)

    cmd = [
        sys.executable, "-m", "slipcover",
        *(("--branch",) if branch else ()),
        "--source", str(src_root),
        "--json", "--out", str(json_path),
        "-m", "pytest",
        "-qq", "--disable-warnings", "-x", str(tests_dir)
    ]

    # ✅ 修复点：在项目根目录运行 pytest，而不是 src_root 目录
    # project_root = src_root.parent
    # tmp_path: Path
    # if flag:
    #     tmp_path = src_root
    # else:
    #     tmp_path = tests_dir

    rc, _out, err = run(cmd, cwd=src_root)

    if rc not in (0, 5):  # 5 = NO_TESTS_COLLECTED
        raise RuntimeError(f"SlipCover 失败 (rc={rc}):\n{err}")

    data = json.load(open(json_path))
    json_path.unlink(missing_ok=True)

    # 绝对化路径
    data["files"] = {
        str((src_root / k).resolve()) if not Path(k).is_absolute() else k: v
        for k, v in data["files"].items()
    }
    return data



# ──────────────────────────────────────────────
# 写测试 → 试跑 → 取覆盖率
# ──────────────────────────────────────────────
def run_test_and_get_cov(test_code: str, src_root: Path) -> Tuple[Dict, str | None]:
    """返回 (coverage_json, error_txt|None)"""
    tmp = src_root / f"test_tmp_{uuid.uuid4().hex[:8]}.py"
    tmp.write_text(test_code, encoding="utf-8")

    env = os.environ.copy()
    env["PYTHONPATH"] = f"{src_root}:{env.get('PYTHONPATH', '')}"

    rc, _out, err = run(
        [sys.executable, "-m", "pytest", "-k", "not .fail", "-qq", tmp.name],
        cwd=src_root, env=env, timeout=120
    )

    cov = slipcover_json(src_root, src_root) if rc == 0 else {}
    tmp.unlink(missing_ok=True)
    return cov, (None if rc == 0 else _out)
