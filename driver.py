"""
driver.py  
入口脚本：  
  1. 初测覆盖率：根据是否存在已有测试决定 slipcover_json 或实际执行  
  2. 并行生成测试，写入 ./tests/  
  3. 最终测覆盖率：执行全部 tests 并汇总  
  4. 可选 --show-prompt 打印 LLM 对话
"""

from __future__ import annotations
import asyncio
import sys
from pathlib import Path
import argparse
import litellm

from coverage_utils import slipcover_json, run_test_and_get_cov
from segment import get_missing_coverage
from gen_test import improve

async def _close_llm():
    if hasattr(litellm, "aclose"):
        try:
            await litellm.aclose()
        except Exception:
            pass

async def main(src_dir: Path, show_prompt: bool):
    root = Path.cwd()
    empty_dir = root / "__empty_tests__"
    empty_dir.mkdir(exist_ok=True)

    test_dir = root / "tests"
    test_dir.mkdir(exist_ok=True)

    try:
        if not any(test_dir.glob("*.py")):
            # ✅ tests 目录为空：用 slipcover_json 初测
            print("🧪 tests 为空，使用 slipcover_json 分析初始覆盖率…")
            init_cov = slipcover_json(src_root=src_dir, tests_dir=empty_dir, branch=True)
            init_pct = init_cov["summary"]["percent_covered"]
            print(f"\n🧪 初始覆盖率为 {init_pct:.1f} %")
            missing = get_missing_coverage(init_cov, line_limit=50)

        else:
            # ✅ tests 存在：实际执行测试收集初测覆盖率
            print("🧪 检测到已有测试，实际运行测试收集初始覆盖率…")
            init_cov = {"files": {}}
            total_lines = 0
            total_executed = 0

            for f in test_dir.glob("*.py"):
                test_code = f.read_text(encoding="utf-8")
                cov, err = run_test_and_get_cov(test_code, src_root=src_dir)

                if err:
                    print(f"⚠️ 测试 {f.name} 执行失败，跳过")
                    continue

                for path, data in cov.get("files", {}).items():
                    try:
                        Path(path).relative_to(src_dir)
                    except ValueError:
                        continue
                    if path not in init_cov["files"]:
                        init_cov["files"][path] = data
                    else:
                        existing = init_cov["files"][path]
                        existing["executed_lines"] = list(set(existing["executed_lines"]) | set(data["executed_lines"]))
                        existing["executed_branches"] = list(
                            set(map(tuple, existing.get("executed_branches", []))) |
                            set(map(tuple, data.get("executed_branches", [])))
                        )

            for file_cov in init_cov["files"].values():
                total_lines += len(file_cov.get("executed_lines", [])) + len(file_cov.get("missing_lines", []))
                total_executed += len(file_cov.get("executed_lines", []))
            init_pct = (100 * total_executed / total_lines) if total_lines else 0
            print(f"\n🧪 初始覆盖率为 {init_pct:.1f} %")

            # 分析缺失
            missing = get_missing_coverage(init_cov, line_limit=50)

            # ⚠️ 排除误判
            def is_still_missing(seg):
                file_cov = init_cov["files"].get(str(seg.path))
                if not file_cov:
                    return True
                if seg.missing_lines and all(l in file_cov["executed_lines"] for l in seg.missing_lines):
                    executed_branches = set(map(tuple, file_cov.get("executed_branches", [])))
                    if all(b in executed_branches for b in seg.missing_branches):
                        return False
                return True

            missing = [seg for seg in missing if is_still_missing(seg)]

        if not missing:
            print("🎉 100% 覆盖，无需生成测试。")
            return

        print(f"⚡ 待生成 {len(missing)} 个测试…")

        # （2）并发生成测试
        async def worker(seg):
            ok = await improve(seg, src_root=src_dir, print_prompt=show_prompt)
            print(("✓" if ok else "×"), seg.identify())

        await asyncio.gather(*(worker(s) for s in missing))

        # （3）终测：运行所有生成测试，合并覆盖率
        combined_coverage = {"files": {}}
        total_lines = 0
        total_executed = 0

        for f in test_dir.glob("*.py"):
            test_code = f.read_text(encoding="utf-8")
            cov, err = run_test_and_get_cov(test_code, src_root=src_dir)
            if err:
                # print(f"❌ 测试 {f.name} 执行失败：\n{err}")
                continue

            for path, data in cov.get("files", {}).items():
                if path not in combined_coverage["files"]:
                    combined_coverage["files"][path] = data
                else:
                    existing = combined_coverage["files"][path]
                    existing["executed_lines"] = list(set(existing["executed_lines"]) | set(data["executed_lines"]))
                    existing["executed_branches"] = list(
                        set(map(tuple, existing.get("executed_branches", []))) |
                        set(map(tuple, data.get("executed_branches", [])))
                    )

        for file_cov in combined_coverage["files"].values():
            total_lines += len(file_cov.get("executed_lines", [])) + len(file_cov.get("missing_lines", []))
            total_executed += len(file_cov.get("executed_lines", []))
        final_pct = (100 * total_executed / total_lines) if total_lines else 0
        print(f"\n🔚 最终覆盖率估计为 {final_pct:.1f} %")

    except RuntimeError as e:
        print(f"❌ 运行终止：{e}")
    finally:
        await _close_llm()

def parse_args():
    ap = argparse.ArgumentParser(description="CoverUp-ZH Lite driver")
    ap.add_argument("src_dir", type=Path, help="源码所在目录")
    ap.add_argument("--show-prompt", action="store_true",
                    help="调试：打印与 DeepSeek 的对话内容")
    return ap.parse_args()

if __name__ == "__main__":
    args = parse_args()
    if not args.src_dir.is_dir():
        print("src_dir 必须是目录")
        sys.exit(1)
    asyncio.run(main(args.src_dir.resolve(), args.show_prompt))
