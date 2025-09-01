"""
complex_math.py
一个稍微“复杂”一点的示例模块，供自动化测试工具（如 CoverUp）用来生成或补全测试。
"""

from __future__ import annotations
import math
from functools import reduce
from typing import List, Tuple


# ===== 基础数值函数 =====
def gcd(a: int, b: int) -> int:
    """欧几里得算法求最大公约数。"""
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def lcm(a: int, b: int) -> int:
    """最小公倍数；0 会抛 ValueError。"""
    if a == 0 or b == 0:
        raise ValueError("lcm() arguments must be non-zero")
    return abs(a // gcd(a, b) * b)


def is_prime(n: int) -> bool:
    """判断素数，n<2 返回 False。"""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    k, step = 5, 2
    while k * k <= n:
        if n % k == 0:
            return False
        k += step
        step = 6 - step
    return True


def prime_factors(n: int) -> List[int]:
    """返回从小到大排列的素因子列表。"""
    if n == 0:
        raise ValueError("0 has infinite prime factors")
    n = abs(n)
    factors, k = [], 2
    while k * k <= n:
        while n % k == 0:
            factors.append(k)
            n //= k
        k += 1 if k == 2 else 2  # 跳过偶数
    if n > 1:
        factors.append(n)
    return factors or [1]


# ===== 一元多项式 =====
def poly_eval(coeffs: List[float], x: float) -> float:
    """霍纳法则计算多项式值，coeffs[0] 为最高次。"""
    return reduce(lambda acc, c: acc * x + c, coeffs, 0.0)


# ===== infix 表达式字符串解析 =====
_ALLOWED = {"+", "-", "*", "/", "(", ")"}


def _tokenize(expr: str) -> List[str]:
    """把 1+2*(3-4.5) 之类拆成 token 列表。"""
    num, tokens = "", []
    for ch in expr.replace(" ", ""):
        if ch.isdigit() or ch == ".":
            num += ch
        else:
            if num:
                tokens.append(num)
                num = ""
            if ch in _ALLOWED:
                tokens.append(ch)
            else:
                raise SyntaxError(f"Invalid char: {ch!r}")
    if num:
        tokens.append(num)
    return tokens


def _precedence(op: str) -> int:
    return 1 if op in {"+", "-"} else 2


def _apply(op: str, b: float, a: float) -> float:
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        if b == 0:
            raise ZeroDivisionError("division by zero")
        return a / b
    raise ValueError(op)


def eval_infix(expr: str) -> float:
    """使用调度场算法计算中缀表达式的值。"""
    tokens = _tokenize(expr)
    output = []  # 输出队列
    operators = []  # 操作符栈
    
    for token in tokens:
        if token.replace(".", "").isdigit():  # 数字
            output.append(float(token))
        elif token == "(":
            operators.append(token)
        elif token == ")":
            while operators and operators[-1] != "(":
                op = operators.pop()
                b, a = output.pop(), output.pop()
                output.append(_apply(op, b, a))
            if operators and operators[-1] == "(":
                operators.pop()  # 移除左括号
        elif token in {"+", "-", "*", "/"}:
            while (operators and operators[-1] != "(" and
                   operators[-1] in {"+", "-", "*", "/"} and
                   _precedence(operators[-1]) >= _precedence(token)):
                op = operators.pop()
                b, a = output.pop(), output.pop()
                output.append(_apply(op, b, a))
            operators.append(token)
    
    # 处理剩余的操作符
    while operators:
        op = operators.pop()
        b, a = output.pop(), output.pop()
        output.append(_apply(op, b, a))
    
    return output[0] if output else 0.0

# ===== 简易矩阵类 =====
class Matrix:
    """支持加法、乘法、行列式的简易矩阵（仅二维列表实现）。"""

    def __init__(self, data: List[List[float]]):
        if not data or any(len(r) != len(data[0]) for r in data):
            raise ValueError("All rows must be same non-zero length")
        self._data = [list(map(float, row)) for row in data]
        self.m, self.n = len(data), len(data[0])

    def __getitem__(self, idx: int) -> List[float]:
        return self._data[idx]

    def __add__(self, other: "Matrix") -> "Matrix":
        if (self.m, self.n) != (other.m, other.n):
            raise ValueError("dimension mismatch for add")
        return Matrix(
            [[self[i][j] + other[i][j] for j in range(self.n)] for i in range(self.m)]
        )

    def __matmul__(self, other: "Matrix") -> "Matrix":
        if self.n != other.m:
            raise ValueError("dimension mismatch for matmul")
        return Matrix(
            [
                [
                    sum(self[i][k] * other[k][j] for k in range(self.n))
                    for j in range(other.n)
                ]
                for i in range(self.m)
            ]
        )

    def det(self) -> float:
        if self.m != self.n:
            raise ValueError("determinant requires square matrix")
        # 递归展开（行列式）
        if self.m == 1:
            return self[0][0]
        if self.m == 2:
            return self[0][0] * self[1][1] - self[0][1] * self[1][0]
        res = 0.0
        for j in range(self.n):
            sub = Matrix(
                [row[:j] + row[j + 1 :] for row in self._data[1:]]
            )
            res += ((-1) ** j) * self[0][j] * sub.det()
        return res

    # 方便打印
    def __repr__(self) -> str:
        return f"Matrix({self._data})"


# ========= 如果直接运行，做简单自测 =========
if __name__ == "__main__":
    print("gcd(48,18) =", gcd(48, 18))
    print("lcm(4,6)  =", lcm(4, 6))
    print("is_prime(97) =", is_prime(97))
    print("prime_factors(360) =", prime_factors(360))
    print("poly_eval([1, -3, 2], 5) =", poly_eval([1, -3, 2], 5))  # 5^2 -3*5 +2

    expr = "1 + 2*(3 - 4 / 2)"
    print(f"eval_infix({expr!r}) =", eval_infix(expr))

    A = Matrix([[1, 2], [3, 4]])
    B = Matrix([[2, 0], [1, 2]])
    print("A + B =", A + B)
    print("A @ B =", A @ B)
    print("det(A) =", A.det())
