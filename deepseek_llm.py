"""
deepseek_llm.py
----------------------------------------------------------------
DeepSeek-Chat 极简封装。
环境变量 DEEPSEEK_API_KEY 必须设置。
"""
from __future__ import annotations
from typing import List, Dict, Any
import os, textwrap
import litellm
import litellm.exceptions as le

MODEL     = "deepseek/deepseek-chat"
API_BASE  = "https://api.deepseek.com"


def _pretty(msgs: List[Dict[str, str]]) -> str:
    """把 messages 美化为人类可读文本"""
    parts = []
    for m in msgs:
        role = m["role"].upper()
        parts.append(f"\n--- {role} {'-'*(60-len(role))}")
        parts.append(textwrap.indent(m["content"], "  "))
    return "\n".join(parts)


async def chat(messages: List[Dict[str, str]],
               temperature: float = 0.0,
               *,
               show: bool = False) -> str:
    """
    与 DeepSeek-Chat 对话。
    show=True 时打印 prompt / 回复；默认静默。
    """
    key = os.getenv("DEEPSEEK_API_KEY")
    if not key:
        raise RuntimeError("缺少环境变量 DEEPSEEK_API_KEY")

    if show:
        print("\n" + "="*70)
        print("📤 Prompt → DeepSeek-Chat")
        print(_pretty(messages))
        print("="*70 + "\n")

    try:
        rsp: Any = await litellm.acreate(
            model      = MODEL,
            api_base   = API_BASE,
            api_key    = key,
            messages   = messages,
            temperature= temperature,
        )
    except le.AuthenticationError:
        raise RuntimeError("DeepSeek-Chat 认证失败，检查 DEEPSEEK_API_KEY 是否有效")

    reply = rsp["choices"][0]["message"]["content"]

    if show:
        print("📥 DeepSeek-Chat 回复（截断 800 字）")
        print(textwrap.shorten(reply, width=800, placeholder=" ..."))
        print("="*70 + "\n")
    return reply
