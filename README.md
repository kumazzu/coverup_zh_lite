# CoverUp ZH Lite

一个基于大语言模型的 Python 代码覆盖率自动提升工具，专为中文环境优化。

## 概述

CoverUp ZH Lite 是一个智能测试生成工具，它能够：

- 🔍 **自动分析代码覆盖率**：使用 slipcover 分析现有测试的覆盖情况
- 🤖 **智能生成测试用例**：利用大语言模型为未覆盖的代码段生成 pytest 测试
- 🔄 **迭代优化覆盖率**：持续改进测试直到达到理想的覆盖率
- 🇨🇳 **中文优化提示**：专门为中文代码注释和文档优化的 LLM 提示模板

## 功能特性

- **零配置启动**：自动检测项目结构，无需复杂配置
- **并行测试生成**：支持多个代码段同时生成测试用例
- **智能错误处理**：自动修复生成的测试中的错误
- **覆盖率可视化**：清晰展示覆盖率提升过程
- **支持复杂代码**：处理包含分支、异常处理等复杂逻辑的代码

## 安装要求

```bash
pip install slipcover pytest litellm
```

## 快速开始

### 基本用法

```bash
python driver.py <源代码目录>
```

### 查看详细提示信息

```bash
python driver.py <源代码目录> --show-prompt
```

### 示例

```bash
# 为 complex_math 目录生成测试
python driver.py complex_math

# 查看 LLM 交互过程
python driver.py complex_math --show-prompt
```

## 工作流程

1. **初始覆盖率分析**
   - 如果 `tests/` 目录为空，使用 slipcover 静态分析
   - 如果存在测试文件，执行现有测试获取覆盖率

2. **代码段分割**
   - 将源代码按函数、类等逻辑单元分割
   - 识别未覆盖的行和分支

3. **并行测试生成**
   - 为每个未覆盖的代码段调用 LLM 生成测试
   - 使用专门优化的中文提示模板

4. **测试验证与修复**
   - 执行生成的测试，验证语法和逻辑正确性
   - 自动修复常见错误（导入问题、断言错误等）

5. **覆盖率提升验证**
   - 确认新测试确实提升了覆盖率
   - 重新生成未达到预期效果的测试

## 项目结构

```
coverup_zh_lite/
├── driver.py           # 主入口脚本
├── gen_test.py         # 测试生成核心逻辑
├── coverage_utils.py   # 覆盖率分析工具
├── segment.py          # 代码分割和分析
├── prompt_zh.py        # 中文 LLM 提示模板
├── deepseek_llm.py     # LLM 接口封装
├── codeinfo.py         # 代码信息提取
├── utils.py            # 通用工具函数
├── complex_math/       # 示例项目
└── tests/              # 生成的测试文件目录
```

## 核心模块说明

### [driver.py](driver.py)
主入口脚本，协调整个测试生成流程：
- 初始覆盖率分析
- 并行测试生成
- 最终覆盖率统计

### [gen_test.py](gen_test.py)
测试生成的核心逻辑：
- LLM 交互管理
- 测试代码提取和验证
- 错误修复和重试机制

### [coverage_utils.py](coverage_utils.py)
覆盖率分析工具：
- slipcover 集成
- 测试执行和覆盖率收集
- 覆盖率数据处理

### [segment.py](segment.py)
代码分割和分析：
- 源代码解析和分割
- 未覆盖代码段识别
- 代码上下文提取

### [prompt_zh.py](prompt_zh.py)
中文优化的 LLM 提示模板：
- 初始测试生成提示
- 错误修复提示
- 覆盖率提升提示

## 配置说明

### LLM 配置

工具使用 [litellm](https://github.com/BerriAI/litellm) 库，支持多种 LLM 提供商。默认配置在 [`deepseek_llm.py`](deepseek_llm.py) 中。

### 覆盖率配置

覆盖率分析使用 [slipcover](https://github.com/plasma-umass/slipcover)，支持行覆盖率和分支覆盖率分析。

## 示例项目

[`complex_math/`](complex_math/) 目录包含一个示例项目，展示了工具的使用效果：

- 包含多种数学函数（GCD、LCM、素数判断等）
- 涵盖各种代码模式（循环、条件分支、异常处理）
- 适合测试工具的各种功能

## 输出示例

```
🧪 tests 为空，使用 slipcover_json 分析初始覆盖率…

🧪 初始覆盖率为 0.0 %
📊 找到 15 个代码段需要生成测试

🔄 并行生成测试中...
✅ complex_math.py:gcd - 测试生成成功
✅ complex_math.py:lcm - 测试生成成功
✅ complex_math.py:is_prime - 测试生成成功
...

🎉 最终覆盖率：95.2%
📈 覆盖率提升：95.2%
```

## 许可证

本项目采用 [MIT 许可证](LICENSE)。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个项目！

---

*CoverUp ZH Lite - 让测试覆盖率提升变得简单高效* 🚀