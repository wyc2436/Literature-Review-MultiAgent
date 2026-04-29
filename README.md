# 多 Agent 文献精读与综述生成系统

**Multi-Agent Literature Review System**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-%3E%3D0.3.0-green.svg)](https://www.langchain.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

一个基于 LangChain 和 DeepSeek 大模型构建的**多 Agent 协同文献精读与学术综述自动生成系统**。专为高校科研群体设计，将数周的文献梳理工作缩短至数分钟。

---

## 📌 痛点分析

大学生及研究生在进行课题开题或毕业论文时，通常需要阅读数十篇全英文 PDF 顶会论文。传统阅读方式存在以下痛点：

- **耗时长**：精读几十篇数十页的英文论文需花费数周时间。
- **难以横向对比**：在大量文献之间比较核心创新点、实验设置和量化指标极其困难。
- **信息遗漏**：手动梳理容易忽略不同论文之间的矛盾结论和研究空白（Research Gap）。
- **写作负担重**：整理成结构化的文献综述初稿又是一项繁重工作。

本系统通过 **3 个 Agent 协作闭环**，将这一流程自动化、高效化。

---

## 🏗️ 多 Agent 架构

```
┌──────────────────────────────────────────────────────────┐
│                     用户输入                              │
│         research_topic + 批量 PDF 论文                    │
└─────────────────────┬────────────────────────────────────┘
                      ▼
┌──────────────────────────────────────────────────────────┐
│            Agent 1: 解析 Agent (ParsingAgent)             │
│  • 遍历 papers/ 目录下所有 PDF                            │
│  • PyPDFLoader 提取全文                                   │
│  • LLM 提炼每篇的 Abstract / Method / Result              │
│  • 输出: List[dict] 结构化摘要列表                         │
└─────────────────────┬────────────────────────────────────┘
                      ▼
┌──────────────────────────────────────────────────────────┐
│          Agent 2: 推理 Agent (ReasoningAgent)             │
│  • 拼接所有论文的结构化摘要                                │
│  • LLM 扮演"资深学术博导"进行横向对比                       │
│  • 总结研究共识、比较方法优劣、挖掘 Research Gap            │
│  • 输出: 深度推理分析文本                                  │
└─────────────────────┬────────────────────────────────────┘
                      ▼
┌──────────────────────────────────────────────────────────┐
│           Agent 3: 撰写 Agent (WritingAgent)              │
│  • 综合摘要列表 + Gap 分析报告                             │
│  • LLM 生成中文 Markdown 格式学术综述                      │
│  • 严格包含 5 个规范章节                                   │
│  • 输出: output/*.md 综述文件                              │
└─────────────────────┬────────────────────────────────────┘
                      ▼
┌──────────────────────────────────────────────────────────┐
│                   输出 Markdown 综述                       │
│  1. 引言与背景                                            │
│  2. 核心研究方法演进                                       │
│  3. 主要实验成果对比                                       │
│  4. 当前研究空白与未来方向                                  │
│  5. 参考文献                                              │
└──────────────────────────────────────────────────────────┘
```

---

## ✨ 功能特点

- **全自动流水线**：放入 PDF → 一键运行 → 输出综述，无需人工干预。
- **三级 Agent 协作**：解析 → 推理 → 撰写，每个 Agent 职责清晰，可独立调试。
- **结构化输出**：每篇论文按 Abstract / Method / Result 三模块精确提炼。
- **Research Gap 自动挖掘**：推理 Agent 强制分析当前研究空白与未来方向。
- **Markdown 输出**：生成格式规范、可直接交付导师的中文学术综述。
- **DeepSeek 驱动**：默认使用 DeepSeek，兼容 OpenAI SDK 格式，可无缝切换其他模型。
- **进度可视化**：全程终端 emoji 打印，运行过程清晰可追踪。

---

## 🚀 快速开始

### 1. 环境要求

- Python 3.10+
- pip

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 API Key

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env，填入你的 DeepSeek API Key
# DEEPSEEK_API_KEY="sk-xxxxxxxxxxxxxxxx"
# DEEPSEEK_BASE_URL="https://api.deepseek.com"
```

获取 API Key：[DeepSeek 开放平台](https://platform.deepseek.com/)

### 4. 放入论文

将要分析的 PDF 论文文件放入 `papers/` 目录。

```bash
# 示例
cp ~/Downloads/attention_is_all_you_need.pdf papers/
cp ~/Downloads/bert_pretraining.pdf papers/
```

### 5. 运行系统

```bash
python main.py
```

根据终端提示输入研究主题，例如：

```
>>> 研究主题: Transformer 架构在自然语言处理中的演进
```

程序将自动依次执行解析 → 推理 → 撰写，最终综述保存至 `output/` 目录。

---

## 📂 项目结构

```
Literature-Review-MultiAgent/
├── papers/                  # 存放待分析的 PDF 论文 (留空)
├── output/                  # 存放生成的综述 Markdown (留空)
├── src/
│   ├── __init__.py
│   ├── parsing_agent.py     # Agent 1: PDF 文本提取与结构化摘要
│   ├── reasoning_agent.py   # Agent 2: 跨文献推理与 Gap 分析
│   └── writing_agent.py     # Agent 3: 学术综述撰写
├── .env.example             # 环境变量配置模板
├── requirements.txt         # 项目依赖列表
├── main.py                  # 程序入口
└── README.md                # 项目说明文档
```

---

## ⚠️ Token 消耗提示

本系统为**高 Token 消耗型应用**，每次运行将向大模型发送大量文本数据（包括 PDF 全文、多篇论文摘要拼接、深度推理分析等），预计单次完整流程 Token 消耗量级如下：

| 阶段 | 说明 | 预估 Token 消耗 |
|------|------|:---------:|
| 解析 Agent | 每篇 PDF 全文 + 摘要提取 | ~20K / 篇 |
| 推理 Agent | 多篇摘要拼接 + 深度对比推理 | ~15K-30K |
| 撰写 Agent | 上下文综合 + 长篇综述生成 | ~20K-40K |
| **合计** | **10 篇论文约** | **~200K-300K** |

> **建议**：
> - 使用 DeepSeek 等性价比高的大模型。
> - 单次分析论文数量建议控制在 10 篇以内，可获得最佳效果。
> - 该系统的 Token 消耗特性使其天然适合测试长文本大模型的上下文理解和推理能力。

---

## 🔧 自定义与扩展

### 切换模型

修改 `main.py` 中的 `ChatOpenAI` 配置：

```python
llm = ChatOpenAI(
    model="gpt-4o",                    # 替换为其他模型
    openai_api_key="sk-xxx",
    openai_api_base="https://api.openai.com/v1",
    temperature=0.3,
    max_tokens=8192,
)
```

### 调整文本截断长度

修改 `parsing_agent.py` 中 `ParsingAgent.__init__` 内的 `self.max_text_length` 变量。

---

## 📄 License

MIT License
