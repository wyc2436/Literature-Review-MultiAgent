import os
from typing import List, Dict

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage


class WritingAgent:
    """
    Agent 3: 学术综述撰写
    综合解析 Agent 的论文摘要和推理 Agent 的 Gap 分析，生成中文 Markdown 格式的学术综述。
    """

    def __init__(self, llm: ChatOpenAI):
        self.llm = llm

    def generate_review(
        self,
        topic: str,
        paper_summaries: List[Dict[str, str]],
        gap_analysis: str,
        output_path: str,
    ):
        if not paper_summaries:
            print("\u274C 没有可用的论文摘要，无法生成综述。")
            return

        print(f"\U0001F4DD 撰写 Agent 启动：正在生成学术综述\n")

        # 构建上下文
        combined_context = f"# 研究主题\n{topic}\n\n# 论文摘要汇总\n\n"
        for idx, paper in enumerate(paper_summaries, start=1):
            combined_context += (
                f"## 论文 {idx}：{paper.get('filename', '未知')}\n\n"
                f"- **摘要与研究背景**：{paper.get('abstract', 'N/A')}\n"
                f"- **核心方法与模型**：{paper.get('method', 'N/A')}\n"
                f"- **主要实验数据与结论**：{paper.get('result', 'N/A')}\n\n"
            )

        combined_context += f"\n# 推理 Agent 的 Gap 分析报告\n\n{gap_analysis}\n"

        # 构建参考文献列表
        references = ""
        for idx, paper in enumerate(paper_summaries, start=1):
            references += f"[{idx}] {paper.get('filename', '未知文献')}\n"

        system_prompt = SystemMessage(content=(
            "你是一位学术写作专家，擅长撰写高质量的中文学术综述文章。\n\n"
            "请根据提供的论文摘要和 Research Gap 分析报告，撰写一篇完整的学术文献综述。"
            "输出必须严格使用 Markdown 格式，包含以下 5 个章节：\n\n"
            "1. **引言与背景**：介绍该研究主题的背景、意义和研究现状概述。\n"
            "2. **核心研究方法演进**：梳理各论文提出的方法/模型，分析技术路线的演进趋势。\n"
            "3. **主要实验成果对比**：横向对比各论文的实验设置、关键指标和核心结论。\n"
            "4. **当前研究空白与未来方向**：基于 Gap 分析，详细阐述尚未解决的问题和潜在研究方向。\n"
            "5. **参考文献**：列出所有引用论文的编号列表。\n\n"
            "要求：\n"
            "- 内容专业、深入，总字数不少于 2000 字。\n"
            "- 在正文中引用论文时使用 [1]、[2] 等编号标注。\n"
            "- 使用中文撰写，Markdown 格式规范美观。"
        ))

        human_prompt = HumanMessage(content=(
            f"请撰写一篇关于「{topic}」的学术文献综述。以下是所有参考资料：\n\n"
            f"{combined_context}\n\n"
            "请生成完整的综述内容，确保包含上述 5 个必要章节。"
        ))

        print("    \U0001F4AC 正在向大模型发送撰写请求...")
        response = self.llm.invoke([system_prompt, human_prompt])
        review_content = response.content.strip()

        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(review_content)

        print(f"    \u2705 综述已保存至: {output_path}\n")
        print(f"    \U0001F4CA 综述长度：{len(review_content)} 字符")
