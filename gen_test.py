from __future__ import annotations
from pathlib import Path
from typing import List
import re, uuid

from deepseek_llm import chat
from prompt_zh import INITIAL, ON_ERROR, ON_NO_GAIN
from coverage_utils import run_test_and_get_cov
from segment import CodeSegment


def _extract_code(txt: str) -> str | None:
    """从 LLM 回复中提取 ```python``` 代码块"""
    m = re.search(r"```python\n(.*?)(?:```|\Z)", txt, re.S)
    return m.group(1) if m else None


def _module_fqn(src_root: Path, f: Path) -> str:
    """根据文件路径生成模块全名，例如 src/complex_math.py → 'complex_math'"""
    return ".".join(f.relative_to(src_root).with_suffix("").parts)


async def improve(
    seg: CodeSegment,
    src_root: Path,
    *,
    print_prompt: bool = False,
    max_try: int = 5
) -> bool:
    root = Path.cwd()
    tests_dir = root / "tests"
    tests_dir.mkdir(exist_ok=True)

    excerpt = seg.get_excerpt(tag_lines=True, add_imports=True)
    module_fqn = _module_fqn(src_root, seg.path)
    func = seg.name
    file_stem = seg.path.stem

    # 初始 Prompt
    msgs: List[dict] = [{
        "role": "user",
        "content": INITIAL.format(
            excerpt=excerpt,
            module_fqn=module_fqn,
            file_path=seg.path.relative_to(src_root).as_posix()
        )
    }]

    for attempt in range(1, max_try + 1):
        reply = await chat(msgs, show=print_prompt)
        test_code = _extract_code(reply) or reply

        # 修复嵌套模块导入
        pattern = rf"from\s+{re.escape(module_fqn)}(?:\.{re.escape(file_stem)})+\s+import\s+{re.escape(func)}"
        test_code = re.sub(pattern, f"from {module_fqn} import {func}", test_code)

        # 执行测试并获取覆盖率
        cov, err = run_test_and_get_cov(test_code, src_root)

        file_cov = cov.get("files", {}).get(str(seg.path), {})
        exec_lns = set(file_cov.get("executed_lines", []))
        exec_br = {tuple(b) for b in file_cov.get("executed_branches", [])}

        gained = (seg.missing_lines & exec_lns) or (seg.missing_branches & exec_br)
        passed = (err is None) and bool(gained)

        # 保存测试文件
        status = "passed" if passed else "failed"
        filename = f"{file_stem}_{func}_{status}_{attempt}.py"
        out_path = tests_dir / filename

        if err is not None:
            # 将错误信息逐行转为注释
            err_comment = "\n".join(f"# {line}" for line in err.strip().splitlines())
            content = f"{err_comment}\n\n{test_code}"
        else:
            content = test_code

        out_path.write_text(content, encoding="utf-8")

        # 成功则终止
        if passed:
            return True

        # 准备下一轮提示
        if err is not None:
            next_prompt = ON_ERROR.format(error=err[:800])
        else:
            uncovered_lines = sorted(seg.missing_lines - exec_lns)
            uncovered_branches = sorted(seg.missing_branches - exec_br)
            next_prompt = ON_NO_GAIN.format(
                lines=uncovered_lines,
                branches=", ".join(f"{b[0]}->{b[1]}" for b in uncovered_branches)
            )

        msgs += [
            {"role": "assistant", "content": reply},
            {"role": "user", "content": next_prompt}
        ]

    return False
