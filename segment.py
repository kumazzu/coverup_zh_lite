"""
Code-segment extraction (original CoverUp logic)

修改点：
* 为兼容 “脚本直跑”，导入 utils / codeinfo 时先尝试相对导入，
  失败则回退到绝对导入。
"""
from __future__ import annotations
try:
    # 当作为包导入时（coverup_zh_lite.segment）
    from .utils import *
    from .codeinfo import get_global_imports, parse_file
except ImportError:                     # 直接 python segment.py ...
    from utils import *
    from codeinfo import get_global_imports, parse_file
# ------- 下面原封不动 -------
import typing as T
from pathlib import Path
import ast


"""
（前略 … 全部原 CoverUp 代码保持不变 …）
"""
import typing as T
from pathlib import Path
import ast

# -- 省略若干原始函数 / 类定义 --

class CodeSegment:
    """Represents a section of code that is missing coverage."""

    def __init__(self, filename: Path, name: str, begin: int, end: int,
                 lines_of_interest: T.Set[int],
                 missing_lines: T.Set[int],
                 executed_lines: T.Set[int],
                 missing_branches: T.Set[T.Tuple[int, int]],
                 context: T.List[T.Tuple[int, int]],
                 imports: T.List[str]):
        self.path = Path(filename).resolve()          # ★ 绝对路径
        self.filename = filename                      # 可能是相对字符串
        self.name = name
        self.begin = begin
        self.end = end
        self.lines_of_interest = lines_of_interest
        self.missing_lines = missing_lines
        self.executed_lines = executed_lines
        self.missing_branches = missing_branches
        self.context = context
        self.imports = imports

    # ---- 其余方法保持 ----

    def get_excerpt(self, *, tag_lines=True, add_imports=True):
        """
        Returns a string with the code excerpt for this segment.
        若 add_imports=True，会把全局 import 语句也一并加入片段。
        """
        excerpt = []

        # ★ 改动：用 self.path（绝对）而非 self.filename
        with self.path.open("r") as src:
            code = src.readlines()

            if add_imports:
                for imp in self.imports:
                    excerpt.extend([f"{'':10}  {imp}\n"])

            for b, e in self.context:
                for i in range(b, e):
                    excerpt.extend([f"{'':10}  ", code[i-1]])

            for i in range(self.begin, self.end):
                if tag_lines and (i in self.lines_of_interest):
                    excerpt.extend([f"{i:10}: ", code[i-1]])
                else:
                    excerpt.extend([f"{'':10}  ", code[i-1]])

        return ''.join(excerpt)

# ---- 文件末尾其它函数（get_missing_coverage 等）保持原样 ----


    def __repr__(self):
        return f"CodeSegment(\"{self.filename}\", \"{self.name}\", {self.begin}, {self.end}, " + \
               f"{self.missing_lines}, {self.executed_lines}, {self.missing_branches}, {self.context})"

    def identify(self) -> str:
        return f"{self.filename}:{self.begin}-{self.end-1}"

    def __str__(self) -> str:
        return self.identify()

    # def get_excerpt(self, *, tag_lines=True, add_imports=True):
    #     excerpt = []
    #     with open(self.filename, "r") as src:
    #         code = src.readlines()

    #         if add_imports:
    #             for imp in self.imports:
    #                 excerpt.extend([f"{'':10}  {imp}\n"])

    #         for b, e in self.context:
    #             for i in range(b, e):
    #                 excerpt.extend([f"{'':10}  ", code[i-1]])

    #         for i in range(self.begin, self.end):
    #             if tag_lines and (i in self.lines_of_interest):
    #                 excerpt.extend([f"{i:10}: ", code[i-1]])
    #             else:
    #                 excerpt.extend([f"{'':10}  ", code[i-1]])

    #     return ''.join(excerpt)


    def lines_branches_missing_do(self):
        return lines_branches_do(self.missing_lines, self.executed_lines, self.missing_branches)


    def missing_count(self) -> int:
        return len(self.missing_lines)+len(self.missing_branches)


def get_missing_coverage(coverage, line_limit: int = 100) -> T.List[CodeSegment]:
    """Processes a JSON SlipCover output and generates a list of Python code segments,
    such as functions or classes, which have less than 100% coverage.
    """

    code_segs = []

    def find_first_line(node):
        # skip back to include decorators, as they are really part of the definition
        return min([node.lineno] + [d.lineno for d in node.decorator_list])

    def find_enclosing(root, line):
        for node in ast.walk(root):
            if node is root:
                continue

            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and hasattr(node, "lineno"):
                begin = find_first_line(node)
                if begin <= line <= node.end_lineno:
                    return (node, begin, node.end_lineno+1) # +1 for range() style

    for fname, fcov in coverage['files'].items():
        path = Path(fname)

        # 🛡️ 忽略临时生成但已经被删除的测试文件（如 test_tmp_xxx.py）
        if not path.exists():
            continue
            
        tree = parse_file(Path(fname))

        missing_lines = set(fcov['missing_lines'])
        executed_lines = set(fcov['executed_lines'])
        missing_branches = fcov.get('missing_branches', set())

        line_ranges = dict()

        lines_of_interest = missing_lines.union(set(sum(missing_branches,[])))
        lines_of_interest.discard(0)  # may result from N->0 branches

        # TODO remove from missing lines with load-time statements?
        #   - directly under ModuleDef, ClassDef
        # note that docstring don't generate code, so can't be missing within functions
        # But then: how to capture missing coverage if a module was never loaded?

        lines_in_segments = set()

        for line in sorted(lines_of_interest):   # sorted() simplifies tests
            if line in lines_in_segments:
                # already in a segment
                continue

            # FIXME add segments for top-level elements (under ModuleDef)
            if element := find_enclosing(tree, line):
                node, begin, end = element
                context = []

                # If a class is above the line limit, look for enclosing element
                # that might allow us to obey the limit
                while isinstance(node, ast.ClassDef) and end - begin > line_limit and \
                      (element := find_enclosing(node, line)):
                    context.append((begin, node.lineno+1)) # +1 for range() style
                    node, begin, end = element

                # Don't create a segment for a class that's too large... if we did, we
                # might create a segment for a class after creating segments for its contents.
                if isinstance(node, ast.ClassDef) and end - begin > line_limit:
                    continue

                assert line < end
                assert (begin, end) not in line_ranges

                line_ranges[(begin, end)] = (
                    node, context, [ast.unparse(x) for x in get_global_imports(tree, node)]
                )
                lines_in_segments.update({*range(begin, end)})

        if line_ranges:
            for (begin, end), (node, context, imports) in line_ranges.items():
                line_range_set = {*range(begin, end)}
                code_segs.append(CodeSegment(
                    fname, node.name, begin, end,
                    lines_of_interest=lines_of_interest.intersection(line_range_set),
                    missing_lines=missing_lines.intersection(line_range_set),
                    executed_lines=executed_lines.intersection(line_range_set),
                    missing_branches={tuple(b) for b in missing_branches if b[0] in line_range_set},
                    context=context,
                    imports=imports)
                )

    return code_segs
